from random import random

# Probability
def probability(percent):
    outcome = random() < percent
    print(outcome)
    return outcome
