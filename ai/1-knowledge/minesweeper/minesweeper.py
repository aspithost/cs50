import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If number of cells equals the number of mines, return all cells
        if self.count == len(self.cells):
            return self.cells
        # Return empty set when not sure
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If there are no mines, return all cells
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        # Called when the Minesweeper board tells us, for a given
        # safe cell, how many neighboring cells have mines in them.

        # Add move to moves_made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Get neighboring cells for move made
        neighboring_cells = self.get_neighboring_cells(cell)

        # Filter safes and mines from neighboring cells
        for cell_to_check in set(neighboring_cells):
            # If neighboring cell is a mine, mark mine, remove cell and reduce count
            if cell_to_check in self.mines:
                self.mark_mine(cell_to_check)
                neighboring_cells.remove(cell_to_check)
                count -= 1
            # If neighboring cell is safe, remove cell
            elif cell_to_check in self.safes:
                self.mark_safe(cell_to_check)
                neighboring_cells.remove(cell_to_check)

        # Add sentence to knowledge base
        self.knowledge.append(Sentence(neighboring_cells, count))

        # After updating mines/safes, review existing knowledge
        self.review_knowledge()

    def get_neighboring_cells(self, cell):
        x, y = cell
        neighboring_cells = set()

        for i in range(max(0, x - 1), min(self.height, x + 2)):
            for j in range(max(0, y -1), min(self.width, y + 2)):
                if (i, j) != (x, y):
                    neighboring_cells.add((i, j))
        return neighboring_cells

    def review_knowledge(self):
        # 4) mark any additional cells as safe or as mines
        #    if it can be concluded based on the AI's knowledge base
        updated_knowledge = False
        knowledge_copy = list(self.knowledge)
        for sentence in knowledge_copy:
            # If empty sentence, remove sentence
            if not len(sentence.cells):
                self.knowledge.remove(sentence)
                continue

            # Check number of safes and number of mines
            safes = sentence.known_safes()
            mines = sentence.known_mines()

            # If no new information can be inferred, continue
            if not safes and not mines:
                continue

            for cell in set(sentence.cells):
                # If sentence consists of safes only, mark cells as safe
                if len(safes):
                    self.mark_safe(cell)

                # If sentence consists of mine only, mark cells as mine
                elif len(mines):
                    self.mark_mine(cell)

            # Remove empty sentence from knowledge
            self.knowledge.remove(sentence)
            updated_knowledge = True

        # After marking safes and mines, review knowledge again
        if updated_knowledge:
            self.review_knowledge()
            return

        # After updating knowledge, review sentences
        self.review_sentences()

    def review_sentences(self):
        # 5) add any new sentences to the AI's knowledge base
        #    if they can be inferred from existing knowledge

        # Only compare sentences when there are two or more sentences in the knowledge base
        if len(self.knowledge) <= 1:
            return

        # Compare all sentences in knowledge base with one another
        updated_sentences = False
        for sentence_i, sentence_j in itertools.combinations(self.knowledge, 2):
            new_sentence = None
            cells_i = sentence_i.cells
            count_i = sentence_i.count
            cells_j = sentence_j.cells
            count_j = sentence_j.count

            is_superset = cells_i.issuperset(cells_j)
            is_subset = cells_i.issubset(cells_j)

            # If sentences are identical sets of cells, remove duplicate
            if is_superset and is_subset:
                self.knowledge.remove(sentence_i)

            # If sentence i is a superset of sentence j, add sentence i - j
            if is_superset:
                new_cells = cells_i.difference(cells_j)
                if len(new_cells):
                    new_count = count_i - count_j
                    new_sentence = Sentence(new_cells, new_count)

            # If sentence i is a subset of sentence j, add sentence j - i
            elif is_subset:
                new_cells = cells_j.difference(cells_i)
                if len(new_cells):
                    new_count = count_j - count_i
                    new_sentence = Sentence(new_cells, new_count)

            # If there is a new inferred sentence, add sentence to knowledge base and re-evaluate knowledge
            if new_sentence:
                self.knowledge.append(new_sentence)
                updated_sentences = True

        # If any of the sentences were updated, review knowledge
        if updated_sentences:
            self.review_knowledge()

    def make_safe_move(self):
        # Iterate over safe cells
        for safe_cell in self.safes:
            # Return first cell that is safe and not already in moves_made
            if safe_cell not in self.moves_made:
                return safe_cell
        return None


    def make_random_move(self):
        # Iterate over all coordinates of board
        for i in range(self.height):
            for j in range(self.width):
                # Return first cell found that is not in mines or in moves already made
                cell = (i, j)
                if cell not in self.mines and cell not in self.moves_made:
                    return cell
        return None
