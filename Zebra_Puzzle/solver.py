

class Attr:
    """ Attribute with its values, e.g., 'house (green, red, blue)' """
    def __init__(self, name, order, values):
        self.name = name
        self.order = order
        self.ordered_values = [AttrValue(self, idx, v) for (idx, v) in enumerate(values)]
        self.values = {v.value: v for v in self.ordered_values}

    def value_at(self, index):
        """ Returns attribute value at a given index """
        if 0 <= index < len(self.ordered_values):
            return self.ordered_values[index]
        return None

    def __getattr__(self, name):
        """ Returns corresponding attribute value, e.g., 'house.green' """
        if name in self.values:
            return self.values[name]
        raise AttributeError(name)

    def __getitem__(self, name):
        """ Returns corresponding attribute value, e.g., 'house["green"]' """
        return self.values[name]

    def __hash__(self):
        return hash((self.name, self.order))

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

class AttrValue:
    """ Attribute value, e.g., 'blue house' """
    def __init__(self, attr, index, value):
        self.attr = attr
        self.index = index
        self.value = value

    def offset_value(self, offset):
        """ Returns attribute value at a given offset from current value """
        return self.attr.value_at(self.index + offset)

    def __hash__(self):
        return hash((self.attr, self.value))

    def __eq__(self, other):
        return isinstance(other, AttrValue) and self.attr == other.attr and self.value == other.value

    def __str__(self):
        return f"{self.attr.name}: {self.value}"

    def __repr__(self):
        return str(self)

class Relation:
    """ Relationship between two attribute values, e.g., 'blue house, owns cat' """
    def __init__(self, atval1, atval2):
        assert atval1.attr != atval2.attr
        self.atval1, self.atval2 = sorted([atval1, atval2], key=lambda x: x.attr.order)

    def with_attr(self, attr):
        return self.atval1.attr == attr or self.atval2.attr == attr

    def with_atval(self, atval):
        return self.atval1 == atval or self.atval2 == atval

    def atval(self, attr):
        return self.atval1 if self.atval1.attr == attr else (self.atval2 if self.atval2.attr == attr else None)

    def __hash__(self):
        return hash((self.atval1, self.atval2))

    def __eq__(self, other):
        return isinstance(other, Relation) and self.atval1 == other.atval1 and self.atval2 == other.atval2

    def __str__(self):
        return f"{self.atval1} <-> {self.atval2}"

    def __repr__(self):
        return str(self)

class Different:
    """ Represents knowledge that two attribute values do not relate in a specific way. """
    def __init__(self, relation):
        self.solver = None
        self.relation = relation

    def evaluate(self, relation):
        return None

    def __str__(self):
        return "Different " + str(self.relation)

    @classmethod
    def of(cls, atval1, atval2):
        return cls(Relation(atval1, atval2))

class Same:
    """ Represents knowledge that two attribute values are related or represent the same entity. """
    def __init__(self, relation):
        self.relation = relation
        self.solver = None

    def evaluate(self, relation):
        a1 = self.relation.atval1
        a2 = self.relation.atval2
        if relation == self.relation:
            return None  # Already evaluated
        if relation.with_attr(a1.attr) and relation.with_attr(a2.attr):
            if relation.with_atval(a1) or relation.with_atval(a2):
                return Different(relation)
        return None


    def __str__(self):
        return "Same " + str(self.relation)

    @classmethod
    def of(cls, atval1, atval2):
        return cls(Relation(atval1, atval2))

class AtLeastOnce:
    """ Ensures each attribute value is used at least once. """
    def __init__(self):
        self.solver = None

    def evaluate(self, relation):
        for attr in self.solver.attrs:
            all_values = set(attr.ordered_values)
            for value in all_values:
                related_values = {r.atval(attr) for r in self.solver.map if r.with_attr(attr) and self.solver.is_same(r)}
                if len(all_values - related_values) == 1:
                    missing_value = (all_values - related_values).pop()
                    return Same(Relation(value, missing_value))
        return None


    def __str__(self):
        return "AtLeastOnce"

class Offset:
    """ Represents knowledge about the relative position of attribute values. """
    def __init__(self, atval1, atval2, offset_attr, offset):
        assert(offset != 0)
        self.solver = None
        self.atval1 = atval1
        self.atval2 = atval2
        self.offset_attr = offset_attr
        self.offset = offset

    def evaluate(self, relation):
        if not relation.with_attr(self.offset_attr):
            return None
        offset_val = relation.atval(self.offset_attr).offset_value(self.offset)
        if offset_val is None:
            return Different(relation)
        if relation.with_atval(self.atval1):
            return Same(Relation(offset_val, self.atval2)) if offset_val == self.atval2 else Different(relation)
        if relation.with_atval(self.atval2):
            return Same(Relation(offset_val, self.atval1)) if offset_val == self.atval1 else Different(relation)
        return None


    def __str__(self):
        return f"Offset {self.atval1}:{self.offset_attr}({self.offset}):{self.atval2}"

class Distance:
    """ Represents knowledge about the distance between attribute values. """
    def __init__(self, atval1, atval2, distance_attr, distance):
        assert(distance > 0)
        self.solver = None
        self.atval1 = atval1
        self.atval2 = atval2
        self.distance_attr = distance_attr
        self.distance = distance

    def evaluate(self, relation):
        if not relation.with_attr(self.distance_attr):
            return None
        for dist in [-self.distance, self.distance]:
            dist_val = relation.atval(self.distance_attr).offset_value(dist)
            if dist_val is None:
                continue
            if relation.with_atval(self.atval1) and dist_val == self.atval2:
                return Same(relation)
            if relation.with_atval(self.atval2) and dist_val == self.atval1:
                return Same(relation)
        return Different(relation)


    def __str__(self):
        return f"Distance {self.atval1}:{self.distance_attr}({self.distance}):{self.atval2}"

# Solver class with implemented logic
class Solver:
    def __init__(self, attrs):
        self.map = {}
        self.list = []
        self.attrs = attrs
        self.demonstrate = False

    def add(self, rule):
        rule.solver = self
        self.list.append(rule)
        if hasattr(rule, 'relation') and rule.relation is not None:
            self.map[rule.relation] = rule
        return self

    def get(self, relation):
        if relation not in self.map:
            return None
        return self.map[relation]

    def is_same(self, relation):
        return relation in self.map and isinstance(self.map[relation], Same)

    def is_different(self, relation):
        return relation in self.map and isinstance(self.map[relation], Different)

    def solve(self):
        while self.iter():
            pass

    def iter(self):
        success = False
        for i in range(len(self.attrs)):
            attr1 = self.attrs[i]
            for j in range(i+1, len(self.attrs)):
                attr2 = self.attrs[j]
                for atval1 in attr1.ordered_values:
                    for atval2 in attr2.ordered_values:
                        relation = Relation(atval1, atval2)
                        if relation in self.map:
                            continue
                        for rule in self.list:
                            result = rule.evaluate(relation)
                            if result is not None:
                                success = True
                                self.add(result)
                                if self.demonstrate:
                                    print(f"{result} <- {rule}")
                            break
        return success

# Attributes initialization
house = Attr('house', 0, [1, 2, 3, 4, 5])
color = Attr('color', 1, ['red', 'green', 'white', 'yellow', 'blue'])
nation = Attr('nation', 2, ['english', 'spanish', 'ukrainian', 'norwegian', 'japanese'])
animal = Attr('animal', 3, ['dog', 'snail', 'fox', 'horse', 'zebra'])
drink = Attr('drink', 4, ['coffee', 'tea', 'milk', 'orangejuice', 'water'])
smoke = Attr('smoke', 5, ['oldgold', 'kool', 'chesterfield', 'luckystrike', 'parliament'])

# Solver setup
solver = Solver([house, color, nation, animal, drink, smoke])
solver.demonstrate = True

# Adding rules to the solver based on the puzzle's clues
solver.add(AtLeastOnce())

# Known relationships from the puzzle
solver.add(Same.of(color.red, nation.english))        # Englishman lives in the red house
solver.add(Same.of(nation.spanish, animal.dog))       # Spaniard owns the dog
solver.add(Same.of(color.green, drink.coffee))        # Coffee is drunk in the green house
solver.add(Same.of(nation.ukrainian, drink.tea))      # Ukrainian drinks tea
solver.add(Offset(color.green, color.white, house, -1)) # Green house is immediately to the right of the ivory house
solver.add(Same.of(smoke.oldgold, animal.snail))      # Old Gold smoker owns snails
solver.add(Same.of(color.yellow, smoke.kool))         # Kools are smoked in the yellow house
solver.add(Same.of(house[2], drink.milk))             # Milk is drunk in the middle house
solver.add(Same.of(nation.norwegian, house[0]))       # The Norwegian lives in the first house
solver.add(Distance(smoke.chesterfield, animal.fox, house, 1))  # Chesterfields smoked next to the house with the fox
solver.add(Distance(animal.horse, smoke.kool, house, 1))  # Kools smoked next to the house with the horse
solver.add(Same.of(smoke.luckystrike, drink.orangejuice))  # Lucky Strike smoker drinks orange juice
solver.add(Same.of(nation.japanese, smoke.parliament))   # The Japanese smokes Parliaments
solver.add(Distance(nation.norwegian, color.blue, house, 1))  # The Norwegian lives next to the blue house

# Running the solver
i = 1
while solver.iter():
    if solver.demonstrate:
        print(f"\nTurn {i}")
    i += 1

# Querying the solution
for man in nation.ordered_values:
    if solver.is_same(Relation(drink.water, man)):
        print(f"{man.value} drinks water.")
    if solver.is_same(Relation(animal.zebra, man)):
        print(f"{man.value} keeps zebra.")
