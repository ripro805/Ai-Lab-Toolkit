from logic import *

people = ["X", "Y"]

symbols = []

knowledge = And()

for person in people:
    symbols.append(Symbol(f"{person}Knight"))
    symbols.append(Symbol(f"{person}Knave"))

# Each person is either Knight or Knave
for person in people:
    knowledge.add(
        Or(
            Symbol(f"{person}Knight"),
            Symbol(f"{person}Knave")
        )
    )

# A person cannot be both Knight and Knave
for person in people:
    knowledge.add(
        Implication(
            Symbol(f"{person}Knight"),
            Not(Symbol(f"{person}Knave"))
        )
    )

    knowledge.add(
        Implication(
            Symbol(f"{person}Knave"),
            Not(Symbol(f"{person}Knight"))
        )
    )

# X says: "Y is a Knave"

knowledge.add(
    Biconditional(
        Symbol("XKnight"),
        Symbol("YKnave")
    )
)

for symbol in symbols:
    if model_check(knowledge, symbol):
        print(symbol)