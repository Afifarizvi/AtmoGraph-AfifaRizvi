import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


class Neo4jClient:
    """Reusable Neo4j connection handler for AtmoGraph backend."""

    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

    def close(self):
        self.driver.close()

    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]

    # ---- Helper methods ----

    def get_node_counts(self):
        query = """
        MATCH (n)
        RETURN labels(n)[0] AS type, count(*) AS count
        ORDER BY type
        """
        return self.run_query(query)

    def get_relationship_counts(self):
        query = """
        MATCH ()-[r]->()
        RETURN type(r) AS relationship, count(*) AS count
        ORDER BY relationship
        """
        return self.run_query(query)

    def get_all_suppliers(self):
        query = "MATCH (s:Supplier) RETURN s.name AS name, s.country AS country, s.industry AS industry"
        return self.run_query(query)

    def get_downstream_path(self, node_name, max_hops=4):
        """Trace the ripple path from a given node (e.g. a Supplier) downstream to Retailers."""
        query = f"""
        MATCH path = (start {{name: $node_name}})-[*1..{max_hops}]->(end:Retailer)
        RETURN [n IN nodes(path) | n.name] AS path_nodes
        """
        return self.run_query(query, {"node_name": node_name})

    def update_node_risk(self, node_name, risk_level):
        """Update the risk_level property of a node identified by its name."""
        query = """
        MATCH (n {name: $node_name})
        SET n.risk_level = $risk_level
        RETURN n.name AS name, n.risk_level AS risk_level, labels(n)[0] AS type
        """
        return self.run_query(query, {"node_name": node_name, "risk_level": risk_level})

    def update_predicted_risk(self, node_name, predicted_score):
        """Store the GNN's predicted risk score on a node, separate from the manually-set risk_level."""
        query = """
        MATCH (n {name: $node_name})
        SET n.predicted_risk_score = $predicted_score
        RETURN n.name AS name, n.predicted_risk_score AS predicted_risk_score
        """
        return self.run_query(query, {"node_name": node_name, "predicted_score": predicted_score})
    
    def get_node_risk(self, node_name):
        """Fetch the current risk_level of a node."""
        query = "MATCH (n {name: $node_name}) RETURN n.risk_level AS risk_level"
        result = self.run_query(query, {"node_name": node_name})
        return result[0]["risk_level"] if result else None

if __name__ == "__main__":
    client = Neo4jClient()

    print("=== Node Counts ===")
    for row in client.get_node_counts():
        print(row)

    print("\n=== Relationship Counts ===")
    for row in client.get_relationship_counts():
        print(row)

    print("\n=== All Suppliers ===")
    for row in client.get_all_suppliers():
        print(row)

    print("\n=== Sample Ripple Path: Congo Cobalt Mines -> Retailer ===")
    for row in client.get_downstream_path("Congo Cobalt Mines"):
        print(" -> ".join(row["path_nodes"]))

    client.close()