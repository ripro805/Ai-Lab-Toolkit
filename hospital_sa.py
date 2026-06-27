import sys
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
import random
import math


class Space():

    def __init__(self, height, width, num_hospitals):
        self.height = height
        self.width = width
        self.num_hospitals = num_hospitals
        self.houses = set()
        self.hospitals = set()

    def add_house(self, row, col):
        self.houses.add((row, col))

    def available_spaces(self):
        candidates = set(
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
        )
        for house in self.houses:
            candidates.discard(house)
        for hospital in self.hospitals:
            candidates.discard(hospital)
        return candidates

    def simulated_annealing(self, max_iterations=10000,
                             initial_temp=100, cooling_rate=0.995,
                             min_temp=0.1, log=False):

        self.hospitals = set()
        for i in range(self.num_hospitals):
            self.hospitals.add(random.choice(list(self.available_spaces())))

        current_cost = self.get_cost(self.hospitals)
        temperature  = initial_temp
        best_hospitals = self.hospitals.copy()
        best_cost      = current_cost

        if log:
            print(f"Initial cost: {current_cost}  |  Temp: {temperature:.2f}", flush=True)

        for iteration in range(1, max_iterations + 1):

            if temperature < min_temp:
                if log:
                    print(f"Stopped early at iteration {iteration}", flush=True)
                break

            hospital   = random.choice(list(self.hospitals))
            neighbours = self.get_neighbors(*hospital)

            if not neighbours:
                continue

            replacement = random.choice(neighbours)
            neighbour = self.hospitals.copy()
            neighbour.remove(hospital)
            neighbour.add(replacement)

            neighbour_cost = self.get_cost(neighbour)
            delta_E        = neighbour_cost - current_cost

            if delta_E < 0:
                self.hospitals = neighbour
                current_cost   = neighbour_cost
            else:
                acceptance_prob = math.exp(-delta_E / temperature)
                if random.random() < acceptance_prob:
                    self.hospitals = neighbour
                    current_cost   = neighbour_cost
                    if log:
                        print(f"  [iter {iteration}] Accepted worse move: "
                              f"dE={delta_E}, prob={acceptance_prob:.4f}, "
                              f"T={temperature:.2f}", flush=True)

            if current_cost < best_cost:
                best_cost      = current_cost
                best_hospitals = self.hospitals.copy()
                if log:
                    print(f"[iter {iteration}] New best cost: {best_cost}  "
                          f"| Temp: {temperature:.2f}", flush=True)

            temperature *= cooling_rate

        if log:
            print(f"\nFinal temperature : {temperature:.4f}", flush=True)
            print(f"Best cost found   : {best_cost}", flush=True)

        self.hospitals = best_hospitals
        return best_hospitals

    def get_cost(self, hospitals):
        cost = 0
        for house in self.houses:
            cost += min(
                abs(house[0] - hospital[0]) + abs(house[1] - hospital[1])
                for hospital in hospitals
            )
        return cost

    def get_neighbors(self, row, col):
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1)
        ]
        neighbors = []
        for r, c in candidates:
            if (r, c) in self.houses or (r, c) in self.hospitals:
                continue
            if 0 <= r < self.height and 0 <= c < self.width:
                neighbors.append((r, c))
        return neighbors


# Main
s = Space(height=10, width=20, num_hospitals=3)
for i in range(15):
    s.add_house(random.randrange(s.height), random.randrange(s.width))

hospitals = s.simulated_annealing(
    max_iterations=10000,
    initial_temp=100,
    cooling_rate=0.995,
    min_temp=0.1,
    log=True
)

print("\nBest Hospitals:", hospitals)
print("Best Cost     :", s.get_cost(hospitals))
