from logic import *


people = ["A", "B", "C"]

symbols = []

knowledge0 = And()
knowledge1 = And()
knowledge2 = And()
knowledge3 = And()


for person in people:
    symbols.append(Symbol(f"{person}Knight"))
    symbols.append(Symbol(f"{person}Knave"))


for k in [knowledge0, knowledge1, knowledge2, knowledge3]:
    for person in people:
        k.add(Or(
            Symbol(f"{person}Knight"),
            Symbol(f"{person}Knave")
        ))
        k.add(Implication(
            Symbol(f"{person}Knight"),
            Not(Symbol(f"{person}Knave"))
        ))
        k.add(Implication(
            Symbol(f"{person}Knave"),
            Not(Symbol(f"{person}Knight"))
        ))


def said_by(speaker, statement):
    return Biconditional(Symbol(f"{speaker}Knight"), statement)



knowledge0.add(said_by())

knowledge1.add(said_by("A", And(Symbol("AKnave"), Symbol("BKnave"))))


same_kind = Or(
    And(Symbol("AKnight"), Symbol("BKnight")),
    And(Symbol("AKnave"),  Symbol("BKnave")),
)
different_kind = Or(
    And(Symbol("AKnight"), Symbol("BKnave")),
    And(Symbol("AKnave"),  Symbol("BKnight")),
)
knowledge2.add(said_by("A", same_kind))
knowledge2.add(said_by("B", different_kind))


knowledge3.add(said_by("A", Or(Symbol("AKnight"), Symbol("AKnave"))))
knowledge3.add(said_by("B", And(Symbol("BKnave"), Symbol("CKnave"))))
knowledge3.add(said_by("C", Symbol("AKnight")))


print(" Puzzle 0")
for symbol in symbols:
    if model_check(knowledge0, symbol):
        print(symbol)

print()
print(" Puzzle 1")
for symbol in symbols:
    if model_check(knowledge1, symbol):
        print(symbol)

print()
print("Puzzle 2")
for symbol in symbols:
    if model_check(knowledge2, symbol):
        print(symbol)

print()
print("Puzzle 3")
for symbol in symbols:
    if model_check(knowledge3, symbol):
        print(symbol)
