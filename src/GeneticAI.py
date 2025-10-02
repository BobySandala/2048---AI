from src.HeurisiticAI import HeuristicAI
from src.game import Game2048
import numpy as np
import random

#  [0.7864211  0.57165049 0.33741794]

class GeneticAI:
    def __init__(self, population_size=50, mutation_rate=0.1, generations=50, number_of_games=5):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        # starts with random weights for each heuristic
        self.population = [np.random.rand(3) for _ in range(population_size)]  # random set of 3 weights between 0 and 1
        self.number_of_games = number_of_games

    def fitness(self, weights):
        scores = []
        for _ in range(self.number_of_games):  # average over 5 games
            Game = Game2048()
            ai = HeuristicAI(Game, weights=weights)
            while True:
                move = ai.get_best_move()
                if move is not None:
                    changed, reward, done = Game.move(move)
                    if done:
                        break
                scores.append(Game.score)
        return np.mean(scores)
    

    def evolve(self):
        best_weights = []
        best_fitness = -1
        for gen in range(self.generations):
            fitnesses = [self.fitness(weights) for weights in self.population]
            ranked = sorted(zip(fitnesses, self.population), reverse=True)
            best = [w for _, w in ranked[:self.population_size // 2]]  # select top half

            new_population = [w for w in best[:len(best)//2]]  # carry over the best directly
            while len(new_population) < self.population_size:
                p1, p2 = random.sample(best, 2) # select two parents
                child = self.crossover(p1, p2)
                child = self.mutate(child)
                new_population.append(child)

            self.population = new_population
            print(f"Generation {gen+1}, Best fitness: {ranked[0][0]}, Weights: {ranked[0][1]}, Best: {best}")
            best_weights = ranked[0][1] if ranked[0][0] > best_fitness else best_weights
            best_fitness = max(best_fitness, ranked[0][0])
        return best_weights

    def crossover(self, parent1, parent2):
        alpha = np.random.rand()
        return alpha * parent1 + (1 - alpha) * parent2
    
    def mutate(self, weights, rate=0.1):
        if np.random.rand() < rate:
            i = np.random.randint(len(weights))
            weights[i] += np.random.normal(0, 0.1)
        return weights
            
def start_genetic_ai(population_size=50, generations=100):
    if population_size < 4:
        raise ValueError("Population size must be at least 4.")
    ga = GeneticAI(population_size=population_size, generations=generations)
    best_weights = ga.evolve()
    print("Best weights found:", best_weights)
    return best_weights

if __name__ == "__main__":
    start_genetic_ai(population_size=5, generations=5)