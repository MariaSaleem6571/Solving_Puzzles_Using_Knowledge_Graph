class Attr:
    u""" Атрибут вместе с его значениями, например 'дом (зеленый, красный, синий)' """
    def __init__(self, name, order, values):
        self.name = name
        self.order = order
        self.ordered_values = [AttrValue(self, idx, v) for (idx, v) in zip(range(len(values)), values)]
        self.values = {v.value: v for v in self.ordered_values }

    def value_at(self, index):
        u"""Значение атрибута по индексу"""
        if index >= 0 and index < len(self.ordered_values):
            return self.ordered_values[index]
        return None

    def __getattr__(self, name):
        u"""Вспомогательный метод, позволяет использовать форму 'attr.name', например 'дом.зеленый', возвращает 
        соответвующее значение атрибута"""
        if name in self.values:
            return self.values[name]
        raise AttributeError(name)

    def __getitem__(self, name):
        u"""Вспомогательный метод, позволяет использовать форму 'attr[name]', например 'дом[зеленый]', возвращает 
        соответвующее значение атрибута"""
        return self.values[name]

    def __hash__(self):
        return hash((self.name, self.order))

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)

class AttrValue:
    u""" Значение атрибута, например 'синий дом' """
    def __init__(self, attr, index, value):
        self.attr = attr
        self.index = index
        self.value = value

    def offset_value(self, offset):
        return self.attr.value_at(self.index + offset)

    def __hash__(self):
        return hash((self.attr, self.value))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.attr == other.attr and self.value == other.value

    def __str__(self):
        return str(self.attr) + ":" + str(self.value)

    def __repr__(self):
        return str(self)

class Relation:
    u"""Отношение между двумя значениями атрибутов, например 'синий дом, держит кошку'. Само по себе не содержит
    признака отношений (совпадает/не совпадает), и используется для адресации. В таблице отношений служит адрресом."""
    def __init__(self, atval1, atval2):
        assert(atval1.attr != atval2.attr)
        if atval1.attr.order < atval2.attr.order:
            self.atval1 = atval1
            self.atval2 = atval2
        else:
            self.atval1 = atval2
            self.atval2 = atval1

    def with_attr(self, attr):
        return self.atval1.attr == attr or self.atval2.attr == attr

    def with_atval(self, atval):
        return self.atval1 == atval or self.atval2 == atval

    def atval(self, attr):
        if self.atval1.attr == attr:
            return self.atval1
        if self.atval2.attr == attr:
            return self.atval2
        return None

    def __hash__(self) -> int:
        return hash((self.atval1, self.atval2))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        return self.atval1 == other.atval1 and self.atval2 == other.atval2
    
    def __str__(self):
        return str(self.atval1) + "<->" + str(self.atval2)
    
    def __repr__(self):
        return str(self)

class Solver:
    u"""Основной класс для решения логических задач, содержит набор знаний в таблице отношений. Знания включены как 
    исходно заданные, так и выведенные в процессе рассуждений. """
    def __init__(self, attrs):
        self.map = {}
        self.list = []
        self.attrs = attrs
        self.demonstrate = False

    def add(self, rule):
        rule.solver = self

        self.list.append(rule)
        if hasattr(rule, 'relation') and rule.relation != None:
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
        u"""Одна итерация рассуждений:
          1. Перебираются все отношения в таблице отношений, по которым еще не сделан вывод
          2. К ним применяются все известные на текущий момент знания с целью вывести дополнительные знания
          3. Если за время итерации появилось хоть одно новое знание, итерация считается успешной"""
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
                            if result == None:
                                continue
                            success = True
                            self.add(result)
                            if self.demonstrate:
                                print(result, "     <-  ", rule)
                            break

        return success

    def __contains__(self, relation):
        return relation in self.map

class Different:
    u"""Знание о том, что отношение между двумя значениями двух атрибутов - отрицательное. Например, 'англичанин не живет в
    зеленом доме'. Знание-маркер, не содержит обработки данных и не может само по себе вывести другое знание."""
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
    u"""Знание о том, что два значения двух атрибутов представляют собой одну и ту же сущность. Например 
     'Англичанин живёт в красном доме', то есть нация - англичанин и тот, кто живет в красном доме - это один и тот же
     человек.
     Дополнительно обеспечивает эксклюзивность отношений, если в красном доме живет англичанин - в красном доме не живет
     больше никто, а англичанин не живет в других домах."""
    def __init__(self, relation):
        self.relation = relation
        self.solver = None

    def evaluate(self, relation):
        a1 = self.relation.atval1
        a2 = self.relation.atval2
        # same attributes
        if relation.with_attr(a1.attr) and relation.with_attr(a2.attr):
            # one attribute value is the same (another is not the same) - considered relation is negative
            if relation.with_atval(a1):
                return Different(relation)
            if relation.with_atval(a2):
                return Different(relation)
            
        if relation.with_atval(a1):
            rel_a2 = relation.atval2 if relation.atval1 == a1 else relation.atval1
            proxy_rel = Relation(a2, rel_a2)
            if self.solver.is_same(proxy_rel):
                return Same(relation)
            if self.solver.is_different(proxy_rel):
                return Different(relation)
        
        if relation.with_atval(a2):
            rel_a2 = relation.atval2 if relation.atval1 == a2 else relation.atval1
            proxy_rel = Relation(a1, rel_a2)
            if self.solver.is_same(proxy_rel):
                return Same(relation)
            if self.solver.is_different(proxy_rel):
                return Different(relation)

        return None

    def __str__(self):
        return "Same " + str(self.relation)
    
    @classmethod
    def of(cls, atval1, atval2):
        return cls(Relation(atval1, atval2))

class AtLeastOnce:
    u"""Знание: каждым значением атрибута должно обладать хотя бы одна сущность, т.е. хотя бы кто-то должен жить в синем доме, и т.п.
    Если значение атрибута Ax отрицательно связано со всеми значениями атрибута B, кроме Bx, то Ax и Bx связаны положительно.
    Наример, если тот, кто держит лошадь, не живет во всех домах, кроме красного, то он живет в красном доме"""
    def __init__(self):
        self.solver = None

    def evaluate(self, relation):
        a1 = relation.atval1
        a2 = relation.atval2
        if self.check_all_filled(a1, a2) or self.check_all_filled(a2, a1):
            return Same(relation)

    def check_all_filled(self, fixed: AttrValue, sliding: AttrValue):
        for slider in sliding.attr.values.values():
            if slider == sliding:
                continue
            if not self.solver.is_different(Relation(fixed, slider)):
                return False
        return True
    
    def __str__(self):
        return "Exclusive"

class Offset:
    u"""Знание о смещении (направление учитывается) одного значения атрибута относительно другого по третьему атрибуту.
     Например, 'зеленый дом стоит справа от белого', то есть зеленый дом смещен относительно белого дома на +1
     по порядковому номеру дома."""
    # дом не такой = дом не существует, или не такой

    # Зелёный дом стоит сразу справа от белого дома.
    # - если дом X-1 - не белый, то дом X - не зеленый| (X, зеленый): if ~(X-1, белый) -> Different
    # - если дом X+1 - не зеленый, то дом X - не белый| (X, белый): if ~(X+1, зеленый) -> Different
    # - если дом Х+1 - зеленый, то дом Х - белый
    # - если дом Х-1 - белый, то дом Х - зеленый

    # matrix - матрица связей
    # atval1 - значение атрибута первой сущности в паре (цвет:зеленый для загадки Эйнштейна)
    # atval2 - значение атрибута второй сущности в паре (цвет:белый для загадки Эйнштейна)
    # offset_attr - атрибут, по которому считается смещение (порядок_домов для загадки Эйнштейна)
    # offset - смещение atval1 от atval2 по offset_attr (+1 для загадки Эйнштейна), может быть отрицательным, не может быть 0
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

        cur_offset_val = relation.atval(self.offset_attr)
        
        if relation.with_atval(self.atval1):
            offset_val = cur_offset_val.offset_value(-self.offset)
            if (offset_val == None
                or self.solver.is_different(Relation(offset_val, self.atval2))):
                return Different(relation)
            if (offset_val != None
                and self.solver.is_same(Relation(offset_val, self.atval2))):
                return Same(relation)

        if relation.with_atval(self.atval2):
            offset_val = cur_offset_val.offset_value(+self.offset)
            if (offset_val == None
                or self.solver.is_different(Relation(offset_val, self.atval1))):
                return Different(relation)
            if (offset_val != None
                and self.solver.is_same(Relation(offset_val, self.atval1))):
                return Same(relation)
            
    def __str__(self):
        return "Offset " + str(self.atval1) + ":" + str(self.offset_attr) + "(" + str(self.offset) + "):" + str(self.atval2)

class Distance:
    u"""Знание о расстоянии (направление не учитывается) одного значения атрибута относительно другого по третьему атрибуту.
     Например, 'Сосед того, кто курит Chesterfield, держит лису', то есть расстояние между домом того, кто держит лису,
     и домом того, кто курит Chesterfield, по порядковому номеру дома равно 1."""
    # дом не такой = дом не существует, или не такой

    # Сосед того, кто курит Chesterfield, держит лису.
    # - если в доме Х-1 курят не честерфилд, и в доме Х+1 курят не честерфилд, то в доме Х не лиса
    # - если в доме Х-1 не лиса, и в доме Х+1 не лиса, то в доме Х курят не честерфилд
    # - если в доме X-1 курят честерфилд, и в доме Х-2 не лиса, то в доме Х лиса
    # - если в доме Х+1 курят честерфилд, и в доме Х+2 не лиса, то в доме Х лиса
    # - если в доме Х-1 держат лису, и в доме Х-2 курят не честерфилд, то в доме Х курят честерфилд
    # - если в доме Х+1 держат лису, и в доме Х+2 курят не честерфилд, то в доме Х курят честерфилд

    # matrix - матрица связей
    # atval1 - значение атрибута первой сущности в паре (курит:chesterfield для загадки Эйнштейна)
    # atval2 - значение атрибута второй сущности в паре (держит:лиса для загадки Эйнштейна)
    # distance_attr - атрибут, по которому считается расстояние (порядок_домов для загадки Эйнштейна)
    # distance - расстояние atval1 от atval2 по distance_attr (1 для загадки Эйнштейна), строго положительное число
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

        cur_distance_val = relation.atval(self.distance_attr)
        left_distance_val = cur_distance_val.offset_value(-self.distance)
        far_left_distance_val = cur_distance_val.offset_value(-2*self.distance)
        right_distance_val = cur_distance_val.offset_value(+self.distance)
        far_right_distance_val = cur_distance_val.offset_value(+2*self.distance)
        
        if relation.with_atval(self.atval1):
            if ((left_distance_val == None
                    or self.solver.is_different(Relation(left_distance_val, self.atval2)))
                and (right_distance_val == None
                    or self.solver.is_different(Relation(right_distance_val, self.atval2)))):
                return Different(relation)
            
            if (left_distance_val != None
                and self.solver.is_same(Relation(left_distance_val, self.atval2))
                and (far_left_distance_val == None
                    or self.solver.is_different(Relation(far_left_distance_val, self.atval1)))):
                return Same(relation)

            if (right_distance_val != None
                and self.solver.is_same(Relation(right_distance_val, self.atval2))
                and (far_right_distance_val == None
                    or self.solver.is_different(Relation(far_right_distance_val, self.atval1)))):
                return Same(relation)
            
        if relation.with_atval(self.atval2):
            if ((left_distance_val == None
                    or self.solver.is_different(Relation(left_distance_val, self.atval1)))
                and (right_distance_val == None
                    or self.solver.is_different(Relation(right_distance_val, self.atval1)))):
                return Different(relation)
            
            if (left_distance_val != None
                and self.solver.is_same(Relation(left_distance_val, self.atval1))
                and (far_left_distance_val == None
                    or self.solver.is_different(Relation(far_left_distance_val, self.atval2)))):
                return Same(relation)

            if (right_distance_val != None
                and self.solver.is_same(Relation(right_distance_val, self.atval1))
                and (far_right_distance_val == None
                    or self.solver.is_different(Relation(far_right_distance_val, self.atval2)))):
                return Same(relation)
            
    def __str__(self):
        return "Distance " + str(self.atval1) + ":" + str(self.distance_attr) + "(" + str(self.distance) + "):" + str(self.atval2)
