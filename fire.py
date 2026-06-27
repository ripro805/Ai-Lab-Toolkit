import random
import os
from PIL import Image, ImageDraw, ImageFont


cell_size = 100
cell_border = 2
cost_size = 40
padding = 10

asset_dir = r"D:\KnowledgeVault\Academic\3 2\LAB\Ai lab\assets"
house_img = os.path.join(asset_dir, "images", "House.png")
fire_img = os.path.join(asset_dir, "images", "Hospital.png")
obs_img  = os.path.join(asset_dir, "images", "obstacle.png")
font_path = os.path.join(asset_dir, "fonts", "OpenSans-Regular.ttf")


class Space():
    def __init__(self, height, width, num_stations):
        self.height = height
        self.width = width
        self.num_stations = num_stations
        self.buildings = set()
        self.weights = {}
        self.obstacles = set()
        self.stations = set()

    def add_building(self, row, col, weight=1):
        self.buildings.add((row, col))
        self.weights[(row, col)] = weight

    def add_obstacle(self, row, col):
        self.obstacles.add((row, col))

    def available_spaces(self):
        candidates = set(
            (row, col)
            for row in range(self.height)
            for col in range(self.width)
        )
        for house in self.buildings:
            candidates.remove(house)
        for fire in self.stations:
            candidates.remove(fire)
        for obstacle in self.obstacles:
            candidates.remove(obstacle)
        return candidates

    def get_cost(self, stations):
        cost = 0
        for house in self.buildings:
            cost += self.weights[house] * min(
                abs(house[0] - fire[0]) + abs(house[1] - fire[1])
                for fire in stations
            )
        return cost

    def get_neighbors(self, row, col):
        candidates = [
            (row - 1, col),
            (row + 1, col),
            (row, col - 1),
            (row, col + 1),
            (row - 1, col - 1),
            (row - 1, col + 1),
            (row + 1, col - 1),
            (row + 1, col + 1),
        ]
        neighbors = []
        for r, c in candidates:
            if (r, c) in self.buildings or (r, c) in self.stations or (r, c) in self.obstacles:
                continue
            if 0 <= r < self.height and 0 <= c < self.width:
                neighbors.append((r, c))
        return neighbors

    
    def hill_climb(self, maximum=None, image_prefix=None, log=False):
        count = 0
        self.stations = set()
        for i in range(self.num_stations):
            self.stations.add(random.choice(list(self.available_spaces())))
        if log:
            print("Initial state: cost", self.get_cost(self.stations))
        if image_prefix:
            self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")

        while maximum is None or count < maximum:
            count += 1
            best_neighbors = []
            best_neighbor_cost = None

            for station in self.stations:
                for replacement in self.get_neighbors(*station):
                    neighbor = self.stations.copy()
                    neighbor.remove(station)
                    neighbor.add(replacement)

                    cost = self.get_cost(neighbor)
                    if best_neighbor_cost is None or cost < best_neighbor_cost:
                        best_neighbor_cost = cost
                        best_neighbors = [neighbor]
                    elif best_neighbor_cost == cost:
                        best_neighbors.append(neighbor)

            if best_neighbor_cost >= self.get_cost(self.stations):
                return self.stations

            if log:
                print(f"Found better neighbor: cost {best_neighbor_cost}")
            self.stations = random.choice(best_neighbors)

            if image_prefix:
                self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")

    
    def random_restart(self, maximum, image_prefix=None, log=False):
        best_stations = None
        best_cost = None

        for i in range(maximum):
            stations = self.hill_climb()
            cost = self.get_cost(stations)
            if best_cost is None or cost < best_cost:
                best_cost = cost
                best_stations = stations
                if log:
                    print(f"{i}: Found new best state: cost {cost}")
            else:
                if log:
                    print(f"{i}: Found state: cost {cost}")

            if image_prefix:
                self.output_image(f"{image_prefix}{str(i).zfill(3)}.png")

        return best_stations


    def output_image(self, filename):
        img = Image.new(
            "RGBA",
            (self.width * cell_size,
             self.height * cell_size + cost_size + padding * 2),
            "white"
        )
        building_img = Image.open(house_img).resize((cell_size, cell_size))
        station_img  = Image.open(fire_img).resize((cell_size, cell_size))
        obstacle_img = Image.open(obs_img).resize((cell_size, cell_size))
        font = ImageFont.truetype(font_path, 30)
        draw = ImageDraw.Draw(img)

        for i in range(self.height):
            for j in range(self.width):
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if (i, j) in self.obstacles:
                    draw.rectangle(rect, fill="dimgray")
                    img.paste(obstacle_img, rect[0], obstacle_img)
                else:
                    draw.rectangle(rect, fill="black")

                if (i, j) in self.buildings:
                    img.paste(building_img, rect[0], building_img)
                if (i, j) in self.stations:
                    img.paste(station_img, rect[0], station_img)

        draw.rectangle(
            (0, self.height * cell_size, self.width * cell_size,
             self.height * cell_size + cost_size + padding * 2),
            "black"
        )
        draw.text(
            (padding, self.height * cell_size + padding),
            f"Cost: {self.get_cost(self.stations)}",
            fill="white",
            font=font
        )

        img.save(filename)


random.seed(42)

s = Space(height=10, width=20, num_stations=3)

for _ in range(15):
    r, c = random.randrange(s.height), random.randrange(s.width)
    while (r, c) in s.buildings or (r, c) in s.obstacles:
        r, c = random.randrange(s.height), random.randrange(s.width)
    s.add_building(r, c, weight=random.randint(1, 5))

for _ in range(5):
    r, c = random.randrange(s.height), random.randrange(s.width)
    while (r, c) in s.buildings or (r, c) in s.obstacles:
        r, c = random.randrange(s.height), random.randrange(s.width)
    s.add_obstacle(r, c)



print("Hill Climbing")
s.hill_climb(image_prefix="fires", log=True)
print(f"Final stations: {s.stations}  cost={s.get_cost(s.stations)}\n")

print("Random Restart Hill Climbing ")
best = s.random_restart(10, log=True)
print(f"Best stations: {best}  cost={s.get_cost(best)}")
