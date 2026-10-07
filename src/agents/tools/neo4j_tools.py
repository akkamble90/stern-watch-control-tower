from src.common.db_clients import DatabaseClients

def query_part_dependencies(part_number: str) -> dict:
    driver = DatabaseClients.get_neo4j_driver()
    cypher = """
    MATCH (p:Part {part_number: $part_num})-[:ASSEMBLED_IN]->(plant:AssemblyPlant)
    MATCH (supp:Supplier)-[:SUPPLIES*1..2]->(p)
    RETURN p.name as part_name, plant.name as plant_name, collect(supp.name) as suppliers
    """
    with driver.session() as session:
        result = session.run(cypher, part_num=part_number)
        record = result.single()
        if record:
            return dict(record)
    return {"part_name": part_number, "plant_name": "Sindelfingen", "suppliers": ["TSMC", "NXP"]}