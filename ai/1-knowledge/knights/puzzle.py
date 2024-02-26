from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

knowledgeA = And(
    # A is either a Knight or a Knave
    Or(AKnight, AKnave),
    # A cannot be both a Knight and a Knave
    Not(And(AKnight, AKnave)),
)

knowledgeB = And(
    knowledgeA,
    # B is either a Knight or a Knave
    Or(BKnight, BKnave),
    # B cannot be both a Knight and a Knave
    Not(And(BKnight, BKnave)),
)

knowledgeC = And(
    knowledgeB,
    # C is either a Knight or a Knave
    Or(CKnight, CKnave),
    # C cannot be both a Knight and a Knave
    Not(And(CKnight, CKnave)),
)

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    knowledgeA,
    # A is a Knight if A's statement is true
    Implication(AKnight, And(AKnight, AKnave)),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    knowledgeB,
    # A is a Knight if both A and B are Knaves
    Implication(AKnight, And(AKnave, BKnave)),
    # B is a Knave if A is a Knight
    Implication(BKnave, AKnight)
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    knowledgeB,
    # A is Knight if A and B are of the same type
    Implication(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(AKnave, Or(And(AKnight, BKnave), And(AKnave, BKnight))),

    # B is a Knight if A and B are of a different type
    Implication(BKnight, Or(And(AKnight, BKnave), And(AKnave, BKnight))),
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    knowledgeC,
    # A is a knight if A is a knight or a knave
    Implication(AKnight, Or(AKnight, AKnave)),
    Implication(AKnave, Not(Or(AKnight, AKnave))),
    # B is a knight if A and C are both Knaves
    Implication(BKnight, And(AKnave, CKnave)),
    Implication(BKnave, Or(AKnight, CKnight)),
    # C is a knight if A is a knight
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave)
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
