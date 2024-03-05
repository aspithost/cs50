import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | NP VP Conj VP
AP -> Adj AP | Adj
NP -> NP NP | P NP | Det N | Det AP N | N
VP -> NP VP | V NP | Adv VP | VP Adv | V
"""

# Sentence 1-10 structure
# n v
# n v d n
# n v d n p n
# n v p d adj n conj n v
# d n v d adj n
# n v p n
# n adv v d n conj n v p d n adv
# n v adv conj v d n
# n v d adj n p n conj v n p d adj n
# n v d adj adj adj n p d n p d n

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    tokenized_sentence = nltk.tokenize.word_tokenize(sentence)
    return [new_word.lower() for new_word in tokenized_sentence if new_word.isalpha()]


def noun_phrase_in_subtree(subtree):
    branches = subtree.subtrees()
    for branch in branches:
        if "NP" in str(branch[0:]):
            return True
    return False


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Keep list in same scope as iterate_tree function
    noun_phrase_chunks = []

    def iterate_tree(tree):
        # Iterate over subtrees
        for subtree in tree:
            # Check if subtree is not terminal
            if isinstance(subtree, nltk.tree.Tree):
                # Check if subtree is a Noun Phrase. If there are no nested Noun Phrases in subtree, append phrase to chunks and continue
                if subtree.label() == "NP" and not noun_phrase_in_subtree(subtree):
                    noun_phrase_chunks.append(subtree)
                    continue

                # Iterate over nested subtrees
                iterate_tree(subtree)

    # Initiate iteration over subtrees
    iterate_tree(tree)

    return noun_phrase_chunks


if __name__ == "__main__":
    main()