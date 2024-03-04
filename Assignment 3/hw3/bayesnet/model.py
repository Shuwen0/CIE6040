# !pip install pomegranate==v0.14.9 (make sure to use the old version!)

from pomegranate import *

# Node A has no parents and is defined by a discrete distribution
A = Node(DiscreteDistribution({
    '+a': 0.1,
    '-a': 0.9
}), name="A")

# Node B has no parents and is defined by a discrete distribution
B = Node(DiscreteDistribution({
    '+b': 0.9,
    '-b': 0.1
}), name="B")

# Node C is conditional on A and B
C = Node(ConditionalProbabilityTable([
    ['+a', '+b', '+c', 0.2],
    ['+a', '+b', '-c', 0.8],
    ['+a', '-b', '+c', 0.6],
    ['+a', '-b', '-c', 0.4],
    ['-a', '+b', '+c', 0.5],
    ['-a', '+b', '-c', 0.5],
    ['-a', '-b', '+c', 0.0],
    ['-a', '-b', '-c', 1.0],
], [A.distribution, B.distribution]), name="C")

# Node D is conditional on B and C
D = Node(ConditionalProbabilityTable([
    ['+b', '+c', '+d', 0.75],
    ['+b', '+c', '-d', 0.25],
    ['+b', '-c', '+d', 0.1],
    ['+b', '-c', '-d', 0.9],
    ['-b', '+c', '+d', 0.5],
    ['-b', '+c', '-d', 0.5],
    ['-b', '-c', '+d', 0.2],
    ['-b', '-c', '-d', 0.8],
], [B.distribution, C.distribution]), name="D")

# Create a Bayesian Network and add states
model = BayesianNetwork()
model.add_states(A, B, C, D)

# Add edges connecting nodes
model.add_edge(A, C)
model.add_edge(B, C)
model.add_edge(B, D)
model.add_edge(C, D)

# Finalize model
model.bake()
