import random
import string

class WeaselProgram:
    """
    Implementation of Richard Dawkins' Weasel program.
    Demonstrates evolution through cumulative selection.
    """
    
    def __init__(self, target="METHINKS IT IS LIKE A WEASEL", mutation_rate=0.05):
        """
        Initialize the Weasel program.
        
        Args:
            target: Target phrase to evolve towards
            mutation_rate: Mutation rate (probability of a character changing)
        """
        self.target = target
        self.mutation_rate = mutation_rate
        self.charset = string.ascii_uppercase + " "
        self.generation = 0
        
    def random_string(self, length):
        """Generate a random string of specified length."""
        return ''.join(random.choice(self.charset) for _ in range(length))
    
    def fitness(self, candidate):
        """
        Calculate the fitness of a candidate string.
        Returns the number of correct characters in the correct position.
        """
        return sum(1 for c, t in zip(candidate, self.target) if c == t)
    
    def mutate(self, parent):
        """
        Create a mutated copy of the parent string.
        Each character has a chance to mutate based on mutation rate.
        """
        mutated = []
        for char in parent:
            if random.random() < self.mutation_rate:
                mutated.append(random.choice(self.charset))
            else:
                mutated.append(char)
        return ''.join(mutated)
    
    def evolve(self, offspring_count=100, verbose=True):
        """
        Run the evolutionary algorithm.
        
        Args:
            offspring_count: Number of offspring per generation
            verbose: If True, print progress
        
        Returns:
            Tuple with (final string, number of generations)
        """
        # Start with a random string
        current = self.random_string(len(self.target))
        self.generation = 0
        
        if verbose:
            print(f"Target:   {self.target}")
            print(f"Start:    {current} (Fitness: {self.fitness(current)}/{len(self.target)})")
            print("-" * 50)
        
        # Evolve until target is reached
        while current != self.target:
            self.generation += 1
            
            # Generate mutated offspring
            offspring = [self.mutate(current) for _ in range(offspring_count)]
            
            # Add parent to population for elitism
            offspring.append(current)
            
            # Select the best offspring
            current = max(offspring, key=self.fitness)
            
            # Display progress every 10 generations or when there's significant improvement
            if verbose and (self.generation % 10 == 0 or self.fitness(current) > self.fitness(offspring[-1])):
                print(f"Generation {self.generation:4d}: {current} (Fitness: {self.fitness(current)}/{len(self.target)})")
        
        if verbose:
            print("-" * 50)
            print(f"✓ Target reached in {self.generation} generations!")
            print(f"Final:    {current}")
        
        return current, self.generation


def run_experiments():
    """Run different experiments with the Weasel program."""
    
    print("=" * 60)
    print("RICHARD DAWKINS' WEASEL PROGRAM")
    print("=" * 60)
    
    # Experiment 1: Default configuration
    print("\n1. STANDARD EXPERIMENT")
    print("-" * 30)
    weasel = WeaselProgram()
    weasel.evolve()
    
    # Experiment 2: Different mutation rate
    print("\n2. EXPERIMENT WITH HIGH MUTATION RATE (10%)")
    print("-" * 30)
    weasel2 = WeaselProgram(mutation_rate=0.1)
    result, gens = weasel2.evolve(verbose=False)
    print(f"Converged in {gens} generations with 10% mutation rate")
    
    # Experiment 3: Low mutation rate
    print("\n3. EXPERIMENT WITH LOW MUTATION RATE (1%)")
    print("-" * 30)
    weasel3 = WeaselProgram(mutation_rate=0.01)
    result, gens = weasel3.evolve(verbose=False)
    print(f"Converged in {gens} generations with 1% mutation rate")
    
    # Experiment 4: Custom phrase
    print("\n4. EXPERIMENT WITH CUSTOM PHRASE")
    print("-" * 30)
    custom_target = "EVOLUTION WORKS"
    weasel4 = WeaselProgram(target=custom_target, mutation_rate=0.05)
    weasel4.evolve()
    
    # Comparative statistics
    print("\n" + "=" * 60)
    print("COMPARATIVE ANALYSIS")
    print("=" * 60)
    
    runs = 10
    rates = [0.01, 0.05, 0.1, 0.2]
    
    print(f"\nAverage generations to converge ({runs} runs each):")
    print("-" * 40)
    
    for rate in rates:
        total_gens = 0
        for _ in range(runs):
            w = WeaselProgram(mutation_rate=rate)
            _, gens = w.evolve(verbose=False)
            total_gens += gens
        avg = total_gens / runs
        print(f"Mutation rate {rate*100:5.1f}%: {avg:6.1f} generations")


if __name__ == "__main__":
    # Run main program
    run_experiments()
    
    print("\n" + "=" * 60)
    print("INTERACTIVE MODE")
    print("=" * 60)
    
    # Allow user to test with their own phrases
    while True:
        print("\nEnter a phrase to evolve (or 'quit' to exit):")
        user_input = input("> ").upper()
        
        if user_input.lower() == 'quit':
            break
        
        if user_input:
            # Remove unsupported characters
            cleaned = ''.join(c if c in string.ascii_uppercase + " " else ' ' for c in user_input)
            
            print(f"\nEvolving: '{cleaned}'")
            weasel_custom = WeaselProgram(target=cleaned, mutation_rate=0.05)
            weasel_custom.evolve()
    
    print("\nProgram terminated. Thank you!")