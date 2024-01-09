from rdf_graph import create_rdf_graph
from rdflib import Namespace, URIRef
import itertools

def is_valid_partial_combination(combination, ns):
    # Early checks based on fixed clues
    if combination['House1']['nationality'] != 'Norwegian':  # Clue 10
        return False
    if combination['House3']['drink'] != 'Milk':  # Clue 9
        return False
    return True

def is_valid_full_combination(combination, rdf_graph, ns):
    # Convert URIRefs to a list for index-based access
    houses = list(combination.keys())

    for house, attributes in combination.items():
        house_index = houses.index(house)

        # Clue 2: The Englishman lives in the red house.
        if attributes['nationality'] == 'Englishman' and attributes['color'] != 'Red':
            return False

        # Clue 3: The Spaniard owns the dog.
        if attributes['nationality'] == 'Spaniard' and attributes['pet'] != 'Dog':
            return False

        # Clue 4: Coffee is drunk in the green house.
        if attributes['drink'] == 'Coffee' and attributes['color'] != 'Green':
            return False

        # Clue 5: The Ukrainian drinks tea.
        if attributes['nationality'] == 'Ukrainian' and attributes['drink'] != 'Tea':
            return False

        # Clue 6: The green house is immediately to the right of the ivory house.
        if attributes['color'] == 'Green':
            if house_index == 0 or combination[houses[house_index - 1]]['color'] != 'Ivory':
                return False

        # Clue 7: The Old Gold smoker owns snails.
        if attributes['cigar'] == 'OldGold' and attributes['pet'] != 'Snails':
            return False

        # Clue 8: Kools are smoked in the yellow house.
        if attributes['cigar'] == 'Kools' and attributes['color'] != 'Yellow':
            return False

        # Clue 11: The Chesterfields smoker lives next to the man with the fox.
        if attributes['cigar'] == 'Chesterfields':
            if not ((house_index > 0 and combination[houses[house_index - 1]]['pet'] == 'Fox') or 
                    (house_index < 4 and combination[houses[house_index + 1]]['pet'] == 'Fox')):
                return False

        # Clue 12: Kools are smoked in the house next to the house where the horse is kept.
        if attributes['cigar'] == 'Kools':
            if not ((house_index > 0 and combination[houses[house_index - 1]]['pet'] == 'Horse') or 
                    (house_index < 4 and combination[houses[house_index + 1]]['pet'] == 'Horse')):
                return False

        # Clue 13: The Lucky Strike smoker drinks orange juice.
        if attributes['cigar'] == 'LuckyStrike' and attributes['drink'] != 'OrangeJuice':
            return False

        # Clue 14: The Japanese smokes Parliaments.
        if attributes['nationality'] == 'Japanese' and attributes['cigar'] != 'Parliaments':
            return False

        # Clue 15: The Norwegian lives next to the blue house.
        if attributes['nationality'] == 'Norwegian':
            if not ((house_index > 0 and combination[houses[house_index - 1]]['color'] == 'Blue') or 
                    (house_index < 4 and combination[houses[house_index + 1]]['color'] == 'Blue')):
                return False

    return True

def solve_zebra_puzzle(rdf_graph, ns):
    # Define possible attributes
    colors = ['Red', 'Green', 'Ivory', 'Yellow', 'Blue']
    nationalities = ['Englishman', 'Spaniard', 'Ukrainian', 'Norwegian', 'Japanese']
    drinks = ['Coffee', 'Tea', 'Milk', 'OrangeJuice', 'Water']
    cigars = ['OldGold', 'Kools', 'Chesterfields', 'LuckyStrike', 'Parliaments']
    pets = ['Dog', 'Snails', 'Fox', 'Horse', 'Zebra']

    # Generate all possible combinations
    for color_perm in itertools.permutations(colors):
        for nationality_perm in itertools.permutations(nationalities):
            for drink_perm in itertools.permutations(drinks):
                for cigar_perm in itertools.permutations(cigars):
                    for pet_perm in itertools.permutations(pets):
                        combination = {
                            "House" + str(i+1): {
                                'color': color, 
                                'nationality': nat,
                                'drink': drink,
                                'cigar': cigar,
                                'pet': pet
                            }
                            for i, (color, nat, drink, cigar, pet) in enumerate(zip(color_perm, nationality_perm, drink_perm, cigar_perm, pet_perm))
                        }

                        if is_valid_partial_combination(combination, ns) and \
                           is_valid_full_combination(combination, rdf_graph, ns):
                            return combination
    return None

def main():
    rdf_graph = create_rdf_graph()
    ns = Namespace("http://example.org/")

    solution = solve_zebra_puzzle(rdf_graph, ns)

    if solution:
        print("Solution found:")
        for house, attrs in solution.items():
            print(f"{house}: {attrs}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
