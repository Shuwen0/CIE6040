import pomegranate

from collections import Counter

from model import model

def generate_sample(model):

    # Mapping of random variable name to sample generated
    sample = {}

    # Mapping of distribution to sample generated
    parents = {}

    # Loop over all states, assuming topological order
    for state in model.states:

        # If we have a non-root node, sample conditional on parents
        if isinstance(state.distribution, pomegranate.ConditionalProbabilityTable):
            sample[state.name] = state.distribution.sample(parent_values=parents)

        # Otherwise, just sample from the distribution alone
        else:
            sample[state.name] = state.distribution.sample()

        # Keep track of the sampled value in the parents mapping
        parents[state.distribution] = sample[state.name]

    # Return generated sample
    return sample

def rejection_sampling(model, condition_function, variables_of_interest, N=10000):
    data = []
    for _ in range(N):
        sample = generate_sample(model)
        if condition_function(sample):
            data.append({var: sample[var] for var in variables_of_interest})
    return Counter(tuple(d.items()) for d in data)


def condition_for_d_given_c(sample):
    # This is the condition function for P(d | c)
    return sample['C'] == '+c'

def condition_for_d_given_not_a_and_b(sample):
    # This is the condition function for P(d | ¬a, b)
    return sample['A'] == '-a' and sample['B'] == '+b'

# Add a function to print the results according to the conditions (observations)
def print_results(counter, condition):
    print(f"Observation: {condition}:")
    print(counter)

# VCalculate conditional probability based on the requirements in pdf, i.e. P(d | c) and P(d | ¬a, b)
counter_d_given_c = rejection_sampling(model, condition_for_d_given_c, ['D'])
counter_d_given_not_a_and_b = rejection_sampling(model, condition_for_d_given_not_a_and_b, ['D'])

# Print the results
print_results(counter_d_given_c, "c")
print_results(counter_d_given_not_a_and_b, "(-a, b)")



