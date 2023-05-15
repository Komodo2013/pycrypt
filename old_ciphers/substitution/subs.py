import random
import re
import string
import nltk
from nltk.lm import MLE
from nltk.lm.preprocessing import pad_sequence
from nltk.util import ngrams
from collections import Counter

# Constants
POPULATION_SIZE = 100
MUTATION_RATE = 0.01
GENERATIONS = 1000

# Load English language model
nltk.download('brown')
corpus = nltk.corpus.brown.sents()
ngram_order = 3
ngrams_data = [ngram for sent in corpus for ngram in ngrams(pad_sequence(sent, ngram_order), n=ngram_order)]
vocabulary = set([ngram[-1] for ngram in ngrams_data])
language_model = MLE(ngram_order)
language_model.fit([ngrams_data], vocabulary_text=vocabulary)

def create_initial_population():
    population = []
    for _ in range(POPULATION_SIZE):
        mapping = list(string.ascii_lowercase + string.digits + " ")
        random.shuffle(mapping)
        population.append(mapping)
    return population

def calculate_fitness(ciphertext, mapping):
    plaintext = ciphertext.lower().translate(str.maketrans(string.ascii_lowercase + string.digits + " ", ''.join(mapping)))
    perplexity = language_model.perplexity(plaintext.split())
    fitness = 1 / perplexity
    return fitness

# Rest of the code remains unchanged...


def selection(population, ciphertext):
    fitness_scores = [calculate_fitness(ciphertext, mapping) for mapping in population]
    selected_indices = random.choices(range(POPULATION_SIZE), weights=fitness_scores, k=POPULATION_SIZE)
    return [population[i] for i in selected_indices]

def crossover(parent1, parent2):
    child = [''] * 37
    start = random.randint(0, 36)
    end = random.randint(start, 37)
    child[start:end] = parent1[start:end]
    for i in range(37):
        if child[i] == '':
            for gene in parent2:
                if gene not in child:
                    child[i] = gene
                    break
    return child

def mutate(child):
    for i in range(37):
        if random.random() < MUTATION_RATE:
            swap_index = random.randint(0, 36)
            child[i], child[swap_index] = child[swap_index], child[i]
    return child

def evolve(population, ciphertext):
    next_generation = []
    elites = int(POPULATION_SIZE * 0.1)
    next_generation.extend(population[:elites])

    while len(next_generation) < POPULATION_SIZE:
        parent1 = random.choice(population)
        parent2 = random.choice(population)
        child = crossover(parent1, parent2)
        child = mutate(child)
        next_generation.append(child)

    return next_generation

def break_substitution_cipher(ciphertext):
    population = create_initial_population()

    for _ in range(GENERATIONS):
        population = evolve(population, ciphertext)

    best_mapping = population[0]
    best_fitness = calculate_fitness(ciphertext, best_mapping)

    for mapping in population[1:]:
        fitness = calculate_fitness(ciphertext, mapping)
        if fitness > best_fitness:
            best_mapping = mapping
            best_fitness = fitness

    plaintext = ciphertext.lower().translate(str.maketrans(string.ascii_lowercase + string.digits + " ", ''.join(best_mapping)))
    return plaintext

# Example usage:
ciphertext = "Xli wsjxlx, xs hehitlw mw, rsx, xsx xli xsmrk Xszmrk, qiwweki, xli jveqwx xli mtlivwwmsr 1,2,3"
plaintext = break_substitution_cipher(ciphertext)
print(plaintext)
