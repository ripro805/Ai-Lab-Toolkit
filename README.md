# AI Lab Algorithms

A collection of classic Artificial Intelligence algorithms implemented in Python as part of an AI lab course. Covers **search**, **local search**, and **knowledge-based reasoning** with PIL-based grid visualizations.

---

## 📂 Repository Structure

| File | Topic | Algorithm |
|------|-------|-----------|
| `fire.py` | Fire Station Placement | Search with weighted cost (Manhattan) |
| `hospital_sa.py` | Hospital Placement | Simulated Annealing |
| `hospitals (1) (1).py` | Hospital Placement | Hill Climbing (Local Search) |
| `puzzle.py` | Hogwarts Logic Puzzle | Propositional Logic + Inference |
| `truefalse.py` | Knights & Knaves | Propositional Logic |
| `truefalse_1.py` | Knights & Knaves (variant) | Propositional Logic |
| `logic.py` | Logic helpers | Symbol, And, Or, Not, Implication |
| `assets/` | Images & fonts | Used for grid visualization |

---

## 🧠 Algorithms Covered

### 1. Local Search — Hill Climbing
- File: `hospitals (1) (1).py`
- Optimizes hospital locations on a grid to minimize total distance to houses.
- May get stuck in local minima.

### 2. Local Search — Simulated Annealing
- File: `hospital_sa.py`
- Improves over hill climbing by accepting worse states with a decreasing probability.
- Escapes local minima using a temperature schedule.

### 3. Weighted Search
- File: `fire.py`
- Places fire stations considering building weights and obstacles.
- Uses Manhattan distance with PIL-based grid output.

### 4. Propositional Logic & Inference
- File: `logic.py` + `puzzle.py` + `truefalse.py`
- Builds a knowledge base of logical statements.
- Uses model checking to find the unique solution.

---

## ⚙️ Setup & Requirements

- Python **3.8+**
- Pillow (PIL)

```bash
pip install pillow
```

---

## ▶️ How to Run

Each file is self-contained. Run from the project root:

```bash
# Hill Climbing — Hospital placement
python "hospitals (1) (1).py"

# Simulated Annealing — Hospital placement
python hospital_sa.py

# Weighted Search — Fire station placement (outputs PNG grids)
python fire.py

# Logic Puzzle — Hogwarts sorting
python puzzle.py

# Knights and Knaves
python truefalse.py
```

> Note: `fire.py` uses an absolute Windows path under `assets/`. Edit `asset_dir` in the file if running on another machine.

---

## 📊 Sample Visualizations

The `assets/images/` folder contains `House.png`, `Hospital.png`, and `obstacle.png` used by the grid visualizers in `fire.py`.

---

## 🎯 Learning Goals

- Implement uninformed / informed search from scratch.
- Compare greedy local search vs. simulated annealing.
- Express real puzzles as propositional logic and solve via inference.
- Visualize state spaces using `PIL`.

---

## 📝 License

Educational use — feel free to fork and learn.
