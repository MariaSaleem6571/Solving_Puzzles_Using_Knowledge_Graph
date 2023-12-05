from rdf_graph import create_rdf_graph  
from reasoning import is_consistent
from itertools import product
from rdflib import Namespace, URIRef

def main():
    # Create RDF graph
    rdf_graph = create_rdf_graph()

    # Define namespace
    ns = Namespace("http://example.org/")

    # Update character names for the new scenario
    character_names = ["Justin", "Oberon", "Larry", "Xan", "Quentin", "Hillary"]
    characters = [URIRef(ns[char_name]) for char_name in character_names]

    # Collect statements from RDF graph
    statements_dict = {character: [] for character in characters}
    for character in characters:
        for _, _, statement in rdf_graph.triples((character, ns.says, None)):
            statements_dict[character].append(str(statement))

    # Generate all possible combinations of characters being Knights or Knaves
    possible_combinations = product(['Knight', 'Knave'], repeat=len(character_names))

    # Iterate through all possible combinations to find a consistent one
    for combination in possible_combinations:
        if is_consistent(combination, rdf_graph, characters, ns):
            solution = dict(zip(character_names, combination))
            print("Consistent combination found:", solution)
            break

if __name__ == "__main__":
    main()
