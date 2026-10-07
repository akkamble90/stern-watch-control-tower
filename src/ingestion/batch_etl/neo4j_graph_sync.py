from src.common.logger import logger
from src.common.db_clients import DatabaseClients

SEED_CYPHER = """
// 1. Create Assembly Plants
MERGE (sindelfingen:AssemblyPlant {id: "PLANT-DE-SIND", name: "Sindelfingen Assembly Plant", country: "Germany"})
MERGE (vance:AssemblyPlant {id: "PLANT-US-VANCE", name: "Vance Assembly Plant", country: "USA"})

// 2. Create Suppliers
MERGE (tsmc:Supplier {id: "SUP-TSMC", name: "Taiwan Semiconductor Manufacturing Co", tier: 2})
MERGE (nxp:Supplier {id: "SUP-NXP", name: "NXP Semiconductors", tier: 1})
MERGE (catl:Supplier {id: "SUP-CATL", name: "CATL Battery Co", tier: 1})

// 3. Create Parts
MERGE (mcu:Part {id: "PART-MCU-A32", part_number: "MCU-A32-S", name: "ADAS Microcontroller Unit", daily_burn_rate: 100})
MERGE (batt:Part {id: "PART-NMC-90KW", part_number: "NMC-CELL-90KW", name: "90kWh Battery Pack", daily_burn_rate: 40})

// 4. Create Relationships
MERGE (tsmc)-[:SUPPLIES]->(nxp)
MERGE (nxp)-[:SUPPLIES]->(mcu)
MERGE (mcu)-[:ASSEMBLED_IN]->(sindelfingen)
MERGE (catl)-[:SUPPLIES]->(batt)
MERGE (batt)-[:ASSEMBLED_IN]->(vance)
"""

def sync_knowledge_graph():
    driver = DatabaseClients.get_neo4j_driver()
    logger.info("Synchronizing Neo4j Supply Chain Knowledge Graph (SCKG)...")
    with driver.session() as session:
        session.run(SEED_CYPHER)
    logger.info("SCKG Node Synchronization Complete.")

if __name__ == "__main__":
    sync_knowledge_graph()