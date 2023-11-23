from itertools import product

def is_consistent(combination, statements):
    """
    Check if the given combination of characters as knights or knaves is consistent with their statements.
    """
    characters = list(statements.keys())  # Extract character names as a list

    for i, character in enumerate(characters):
        role = combination[i]
        for statement in statements[character]:  # Access statements by character name
            statement_is_true = evaluate_statement(character, statement, combination, characters)
            if (role == 'Knight' and not statement_is_true) or (role == 'Knave' and statement_is_true):
                return False
    return True

def evaluate_statement(character, statement, combination, characters):
    """
    Evaluate a statement based on the current combination of characters.
    """
    index_map = {characters[i]: i for i in range(len(characters))}

    # Logic to evaluate the statement
    if statement == "Vincent is a Knave":
        return combination[index_map["Vincent"]] == 'Knave'
    elif statement == "Hillary is a Knave":
        return combination[index_map["Hillary"]] == 'Knave'
    elif statement == "Samuel is a Knight and I am a Knave":
        # Vincent's statement about Samuel and himself
        return combination[index_map["Samuel"]] == 'Knight' and combination[index_map["Vincent"]] == 'Knave'
    else:
        raise ValueError("Unknown statement: " + statement)
