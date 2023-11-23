from rdf_graph import create_rdf_graph
from reasoning import is_consistent, evaluate_statement
from itertools import product
from rdflib import Namespace, Literal

def main():
    # Create RDF graph
    rdf_graph = create_rdf_graph()

    # Define namespace
    ns = Namespace("http://example.org/")

    # SPARQL query to retrieve statements
    query = """
    PREFIX ex: <http://example.org/>

    SELECT ?character ?statement
    WHERE {
      ?character ex:says ?statement .
    }
    """

    # Execute SPARQL query
    results = rdf_graph.query(query)

    # Prepare data for reasoning
    characters = ["Hillary", "Samuel", "Vincent"]
    statements = {name: [] for name in characters}
    for row in results:
        character = str(row.character).split('/')[-1]  # Extract character name from URI
        statement = str(row.statement)
        statements[character].append(statement)

    # Generate all possible combinations of characters being Knights or Knaves
    possible_combinations = product(['Knight', 'Knave'], repeat=len(characters))

    # Iterate through all possible combinations to find a consistent one
    for combination in possible_combinations:
        if is_consistent(combination, statements):
            solution = dict(zip(characters, combination))
            print("Consistent combination found:", solution)
            break

if __name__ == "__main__":
    main()
