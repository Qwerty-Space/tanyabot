from random import random

# Probability
def probability(percent):
    Probability = random() < percent
    print(Probability)
    return Probability
