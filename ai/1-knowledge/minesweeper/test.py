import itertools

height = 4
width = 4


# def get_neighboring_cells_two(self, cell):
#     x, y = cell
#     neighboring_cells = set()

#     for i in range(max(0, x - 1), min(self.height, x + 2)):
#         for j in range(max(0, y -1), min(self.width, y + 2)):
#             if  (i, j) == (x, y):
#                 neighboring_cells.add((i, j))
#     return neighboring_cells

def review_sentences(self):
    updated_sentences = False
    for sentence1, sentence2 in itertools.combinations(self.knowledge, 2):
        new_sentence = sentence1 - sentence2
        if new_sentence:
            self.knowledge.append(new_sentence)
            updated_sentences = True

    if updated_sentences:
        self.review_knowledge()


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




def review_sentences(self):
    # 5) add any new sentences to the AI's knowledge base
    #    if they can be inferred from existing knowledge

    copy = list(self.knowledge)
    length = len(copy)

    # Only compare sentences when there are two or more sentences in the knowledge base
    if length <= 1:
        return

    # Compare all sentences in knowledge base with one another
    updated_sentences = False
    for i in range(length):
        j = i + 1
        while (j < length):
            new_sentence = None
            cells_i = copy[i].cells
            count_i = copy[i].count
            cells_j = copy[j].cells
            count_j = copy[j].count

            is_superset = cells_i.issuperset(cells_j)
            is_subset = cells_i.issubset(cells_j)

            # If sentences are identical sets of cells, remove duplicate
            if is_superset and is_subset:
                self.knowledge.remove(copy[i])

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
            j += 1

    # If any of the sentences were updated, review knowledge
    if updated_sentences:
        self.review_knowledge()
