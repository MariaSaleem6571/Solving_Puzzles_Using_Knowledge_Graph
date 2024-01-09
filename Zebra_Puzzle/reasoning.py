from constraint import Problem

def zebra_puzzle():
    problem = Problem()

    # Variables (houses 1 through 5)
    houses = range(1, 6)
    colors = ['Red', 'Green', 'Ivory', 'Yellow', 'Blue']
    nationalities = ['Englishman', 'Spaniard', 'Ukrainian', 'Norwegian', 'Japanese']
    drinks = ['Coffee', 'Tea', 'Milk', 'OrangeJuice', 'Water']
    cigars = ['OldGold', 'Kools', 'Chesterfields', 'LuckyStrike', 'Parliaments']
    pets = ['Dog', 'Snails', 'Fox', 'Horse', 'Zebra']

    problem.addVariables(colors + nationalities + drinks + cigars + pets, houses)

    # Each house number must be different
    for group in (colors, nationalities, drinks, cigars, pets):
        problem.addConstraint(lambda *args: len(set(args)) == 5, group)

    # Clue 2: The Englishman lives in the red house.
    problem.addConstraint(lambda e, r: e == r, ['Englishman', 'Red'])

    # Clue 3: The Spaniard owns the dog.
    problem.addConstraint(lambda s, d: s == d, ['Spaniard', 'Dog'])

    # Clue 4: Coffee is drunk in the green house.
    problem.addConstraint(lambda c, g: c == g, ['Coffee', 'Green'])

    # Clue 5: The Ukrainian drinks tea.
    problem.addConstraint(lambda u, t: u == t, ['Ukrainian', 'Tea'])

    # Clue 6: The green house is immediately to the right of the ivory house.
    problem.addConstraint(lambda g, i: g - i == 1, ['Green', 'Ivory'])

    # Clue 7: The Old Gold smoker owns snails.
    problem.addConstraint(lambda og, s: og == s, ['OldGold', 'Snails'])

    # Clue 8: Kools are smoked in the yellow house.
    problem.addConstraint(lambda k, y: k == y, ['Kools', 'Yellow'])

    # Clue 9: Milk is drunk in the middle house.
    problem.addConstraint(lambda m: m == 3, ['Milk'])

    # Clue 10: The Norwegian lives in the first house.
    problem.addConstraint(lambda n: n == 1, ['Norwegian'])

    # Clue 11: The Chesterfields smoker lives next to the fox owner.
    problem.addConstraint(lambda c, f: abs(c - f) == 1, ['Chesterfields', 'Fox'])

    # Clue 12: Kools are smoked in the house next to the horse owner.
    problem.addConstraint(lambda k, h: abs(k - h) == 1, ['Kools', 'Horse'])

    # Clue 13: The Lucky Strike smoker drinks orange juice.
    problem.addConstraint(lambda ls, oj: ls == oj, ['LuckyStrike', 'OrangeJuice'])

    # Clue 14: The Japanese smokes Parliaments.
    problem.addConstraint(lambda j, p: j == p, ['Japanese', 'Parliaments'])

    # Clue 15: The Norwegian lives next to the blue house.
    problem.addConstraint(lambda n, b: abs(n - b) == 1, ['Norwegian', 'Blue'])

    # Solving the puzzle
    solutions = problem.getSolutions()

    # Returning the first solution (if exists)
    return solutions[0] if solutions else None

# Solve the Zebra Puzzle
solution = zebra_puzzle()

if solution:
    for key, value in sorted(solution.items()):
        print(f"{key} is in house {value}")
    water_drinker = [key for key, value in solution.items() if value == solution["Water"]][0]
    zebra_owner = [key for key, value in solution.items() if value == solution["Zebra"]][0]
    print(f"\nThe {water_drinker} drinks water.")
    print(f"The {zebra_owner} owns the zebra.")
else:
    print("No solution found.")
