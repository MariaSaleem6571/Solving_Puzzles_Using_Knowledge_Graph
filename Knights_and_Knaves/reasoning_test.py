from py2neo import Graph, Node, Relationship

# Connect to your Neo4j instance
graph = Graph("bolt://localhost:7687", auth=("neo4j"))

# Define nodes and relationships
justin = Node("Person", name="Justin")
oberon = Node("Person", name="Oberon")
larry = Node("Person", name="Larry")
xan = Node("Person", name="Xan")
quentin = Node("Person", name="Quentin")
hillary = Node("Person", name="Hillary")

says1 = Relationship(justin, "SAYS", "Justin is a knave")
says2 = Relationship(oberon, "SAYS", "Larry is a knave")
# Define more nodes and relationships as needed

# Create nodes and relationships in Neo4j
graph.create(justin, oberon, larry, xan, quentin, hillary, says1, says2, ...)
