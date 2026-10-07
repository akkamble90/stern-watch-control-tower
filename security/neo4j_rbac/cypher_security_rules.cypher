
// NEO4J RBAC & ATTRIBUTE-BASED ACCESS CONTROL (ABAC) SCRIPT

// 1. Create Roles
CREATE ROLE ExecutiveIfNotExist;
CREATE ROLE PlantOperationsManagerIfNotExist;
CREATE ROLE DataEngineerIfNotExist;

// 2. Assign Node Read Permissions
// Executive has full read access to all graph nodes
GRANT READ {*} ON GRAPH * TO ExecutiveIfNotExist;

// Data Engineer has full graph read and write permissions
GRANT ALL GRAPH PRIVILEGES ON GRAPH * TO DataEngineerIfNotExist;

// 3. Attribute-Based Access Control (ABAC): Mask Sensitive Financial Margins
// Restrict access to confidential part cost attributes for Plant Operations Managers
DENY READ {unit_cost_eur, margin_impact_eur} ON GRAPH * ELEMENTS Parts TO PlantOperationsManagerIfNotExist;

// 4. Plant Operations Managers can only traverse Assembly Plant nodes
GRANT READ {assembly_plant_id, name, location} ON GRAPH * ELEMENTS AssemblyPlant TO PlantOperationsManagerIfNotExist;
GRANT READ ON GRAPH * ELEMENTS Supplier, Part, Shipment TO PlantOperationsManagerIfNotExist;