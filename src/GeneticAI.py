from .HeurisiticAI import HeuristicAI
from .game import Game2048
import numpy as np
import random
from . import globals
from . import read_write_json
from multiprocessing import Process, Queue
from queue import Empty   # <-- for multiprocessing.Queue too
#  [0.7864211  0.57165049 0.33741794]

progress = 0

class GeneticAI:
    def __init__(self, population_size=50, mutation_rate=0.1, generations=50, number_of_games=5):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        # starts with random weights for each heuristic
        self.population = [np.random.rand(3) for _ in range(population_size)]  # random set of 3 weights between 0 and 1
        self.number_of_games = number_of_games
        self.total_steps = generations * population_size * number_of_games
        self.current_step = 0

    def fitness(self, weights, queue, in_q):
        scores = []
        for _ in range(self.number_of_games):  # average over 5 games
            self.current_step += 1
            prog = self.current_step / self.total_steps
            try:
                msg = in_q.get(timeout=0.1)  # wait up to 0.1s
                print(f"MSG: {msg}")
                if msg == -1:
                    queue.put({"progress": -2})
                    return -1
            except Empty:
                # no message received in 0.1s
                pass
            queue.put({"progress": prog})
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
    

    def evolve(self, queue, in_q):
        best_weights = []
        best_fitness = -1
        for gen in range(self.generations):
            fitnesses = []
            for weights in self.population:
                fit = self.fitness(weights, queue, in_q)
                if fit == -1:
                    print("-1 gasit")
                    return ([0, 0, 0], -1)
                fitnesses.append(fit)
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
        return best_weights, best_fitness

    def crossover(self, parent1, parent2):
        alpha = np.random.rand()
        return alpha * parent1 + (1 - alpha) * parent2
    
    def mutate(self, weights, rate=0.1):
        if np.random.rand() < rate:
            i = np.random.randint(len(weights))
            weights[i] += np.random.normal(0, 0.1)
        return weights

def start_genetic_ai(queue, in_q, population_size=50, generations=100, games=5):
    if population_size < 4:
        raise ValueError("Population size must be at least 4.")
    print("Started")
    ga = GeneticAI(population_size=population_size, generations=generations, number_of_games=games)
    best_weights, best_fitness = ga.evolve(queue, in_q)
    print("Best weights found:", best_weights)
    save_to_json(best_weights)
    queue.put({"progress": -1})
    if best_fitness is not -1:
        read_write_json.save_value("best_score_genetic", best_fitness)
    return best_weights

def save_to_json(weights):
    read_write_json.save_value("genetic_ai_weights_w1", weights[0])
    read_write_json.save_value("genetic_ai_weights_w2", weights[1])
    read_write_json.save_value("genetic_ai_weights_w3", weights[2])
    print("Saved to data.json")

if __name__ == "__main__":
    result = start_genetic_ai(population_size=5, generations=5)

    print("Saved to data.json")