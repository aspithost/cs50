import sys
from copy import deepcopy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for key, values in self.domains.items():
            values_to_remove = set()
            word_length = key.length
            for value in values:
                if len(value) != word_length:
                    values_to_remove.add(value)
            for value in values_to_remove:
                self.domains[key].remove(value)

    def can_overlap(self, value_x, value_y, idx_x, idx_y):
        if value_x[idx_x] != value_y[idx_y]:
            return False
        return True

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False

        # Only check for arc consistency of words overlap
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            idx_x, idx_y = overlap
            for value_x in set(self.domains[x]):
                if not any(self.can_overlap(value_x, value_y, idx_x, idx_y) for value_y in self.domains[y]):
                    self.domains[x].remove(value_x)
                    revised = True

        return revised

    def initialize_arcs(self, domain_keys):
        arcs = []
        for x in domain_keys:
            for y in domain_keys:
                if x != y:
                    arcs.append((x, y))
        return arcs

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            arcs = self.initialize_arcs(self.domains.keys())

        while len(arcs):
            x, y = arcs.pop()
            if self.revise(x, y):
                if not self.domains[x]:
                    return False
                for neighbor in self.crossword.neighbors(x) - {y}:
                    new_tuple = (neighbor, x)
                    if new_tuple not in arcs:
                        arcs.append(new_tuple)

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        assignment_keys = assignment.keys()
        domains_keys = self.domains.keys()
        for key in domains_keys:
            if key not in assignment_keys:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Keep track of all values
        all_values = set()

        for key, value in assignment.items():
            # Check if values are distinct and if value has correct length
            if value in all_values or len(value) != key.length:
                return False
            all_values.add(value)

            # Check if neighbors do not have conflicting overlaps
            for neighbor in self.crossword.neighbors(key):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[key, neighbor]
                    if overlap:
                        idx_x, idx_y = overlap
                        if not self.can_overlap(value, assignment[neighbor], idx_x, idx_y):
                            return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        values = self.domains[var]
        ruled_out_values = {key: 0 for key in values}
        neighbors = self.crossword.neighbors(var)

        # Check neighbors of variable if those neighbors have a value in the assignment
        for neighbor in neighbors:
            if neighbor in assignment and assignment[neighbor]:
                continue

            # Check if neighboring values can overlap with value
            overlap = self.crossword.overlaps[var, neighbor]
            if overlap:
                # Check number of values for neighbor ruled out by value
                idx_x, idx_y = overlap
                values_neighbor = self.domains[neighbor]
                for value in values:
                    for value_neighbor in values_neighbor:
                        if not self.can_overlap(value, value_neighbor, idx_x, idx_y):
                            ruled_out_values[value] += 1

        return sorted(ruled_out_values, key=lambda x: ruled_out_values[x])

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Create set of unassigned keys
        keys_to_assign = set(self.domains.keys()) - set(assignment.keys())

        # Create dictionary of keys with corresponding length
        keys_by_length = {key: len(self.domains[key]) for key in keys_to_assign}

        # Sort keys by length. If tied, sort by key with highest number of neighbors
        sorted_keys = sorted(keys_by_length, key=lambda x: (keys_by_length[x], -len(self.crossword.neighbors(x))))

        # Return first key
        return sorted_keys[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # If assignment complete, return assignment
        if self.assignment_complete(assignment):
            return assignment

        # Select unassigned variable
        variable = self.select_unassigned_variable(assignment)

        # Sorted domain values of a variable
        sorted_domain_values = self.order_domain_values(variable, assignment)

        # Copy original domains in case ac3 alters domains when no solution possible
        domains_copy = deepcopy(self.domains)

        for value in sorted_domain_values:
            assignment[variable] = value
            # Check if assignment is consistent
            if self.consistent(assignment):
                # Check if all domains are arc consistent after adding assignment
                keys_in_arcs = {variable} | self.crossword.neighbors(variable)
                if self.ac3(self.initialize_arcs(keys_in_arcs)):
                    completed_assignment = self.backtrack(assignment)
                    if completed_assignment:
                        return completed_assignment

                # If arcs not consistent or backtrack does not return a solution, remove assignment and reset domains
                del assignment[variable]
                self.domains = domains_copy
            del assignment[variable]

        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
