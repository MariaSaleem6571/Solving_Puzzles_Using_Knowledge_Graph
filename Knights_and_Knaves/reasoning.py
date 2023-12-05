from itertools import product
from rdflib import Graph, Namespace, URIRef
from rdf_graph  import create_rdf_graph

def is_consistent(combination, graph, characters, ns):
    """
    Check if the given combination of characters as knights or knaves is consistent with their statements.
    """
    for i, character in enumerate(characters):
        role = combination[i]
        statements = [str(o) for _, _, o in graph.triples((character, ns.says, None))]
        for statement in statements:
            statement_is_true = evaluate_statement(character, statement, combination, characters, ns)
            if (role == 'Knight' and not statement_is_true) or (role == 'Knave' and statement_is_true):
                return False
    return True

def evaluate_statement(character, statement, combination, characters, ns):
    index_map = {characters[i]: i for i in range(len(characters))}

    # Parsing the statement
    parts = statement.split()
    target_name = parts[0]
    if "always tells the truth" in statement:
        target_character = URIRef(ns[target_name])
        return combination[index_map[target_character]] == 'Knight'
    elif "is a knave" in statement or "lies" in statement:
        target_character = URIRef(ns[target_name])
        return combination[index_map[target_character]] == 'Knave'
    elif "is truthful" in statement:
        target_character = URIRef(ns[target_name])
        return combination[index_map[target_character]] == 'Knight'
    elif "or I am a knave" in statement:
        first_part, second_part = statement.split(" or ")
        first_target_name, first_target_role = first_part.split()[0], 'Knight'
        first_target_character = URIRef(ns[first_target_name])
        first_condition = combination[index_map[first_target_character]] == first_target_role
        second_condition = combination[index_map[character]] == 'Knave'
        return first_condition or second_condition
    else:
        raise ValueError("Unknown statement: " + statement)
