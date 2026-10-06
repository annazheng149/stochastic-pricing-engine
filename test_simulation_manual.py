from src.simulation import MonteCarloSimulator


simulator = MonteCarloSimulator(
    num_simulations=10_000,
    num_steps=60
)

paths = simulator.simulate(
    current_price=254.00,
    drift=0.00001,
    volatility=0.0003
)

results = simulator.summarize(paths)

print("Simulations:", paths.shape[0])
print("Steps:", paths.shape[1])

print()

print(f"Expected Price: ${results['expected_price']:.2f}")
print(f"Median Price:   ${results['median_price']:.2f}")

print()

print(f"5th Percentile: ${results['lower_bound']:.2f}")
print(f"95th Percentile: ${results['upper_bound']:.2f}")

print()

print(f"Minimum: ${results['min_price']:.2f}")
print(f"Maximum: ${results['max_price']:.2f}")