# Define the prior probabilities for each hypothesis (each adjacent cell)
priors = [1/8] * 8

# Define the likelihoods for the evidence given each hypothesis
likelihoods = [1] * 8

# Calculate the total probability of the evidence (normalizing constant)
total_evidence_probability = sum([likelihood * prior for likelihood, prior in zip(likelihoods, priors)])

# Calculate the posterior probabilities using Bayes' Rule
posteriors = [(likelihood * prior) / total_evidence_probability for likelihood, prior in zip(likelihoods, priors)]

# Output the posterior probabilities
for i, posterior in enumerate(posteriors, 1):
    print(f"Posterior probability of poison being in cell {i}: {posterior:.3f}")

# Additionally, for clarity, define the coordinates of the adjacent cells around the center
center_x, center_y = 4, 4  # Center of a 9x9 grid
adjacent_cells = [
    (center_x - 1, center_y - 1), (center_x, center_y - 1), (center_x + 1, center_y - 1),
    (center_x - 1, center_y),                             (center_x + 1, center_y),
    (center_x - 1, center_y + 1), (center_x, center_y + 1), (center_x + 1, center_y + 1)
]

# Output the posterior probabilities with coordinates of the adjacent cells
for (x, y), posterior in zip(adjacent_cells, posteriors):
    print(f"Posterior probability of poison being in cell ({x}, {y}): {posterior:.3f}")
