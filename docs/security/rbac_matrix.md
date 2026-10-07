# Role-Based Access Control (RBAC) & Attribute Matrix

This document defines user access permissions and security controls across **Project Stern-Watch**.

## Role Hierarchy & Permission Matrix

| Permission String | Executive | Supply Chain Director | Plant Operations Manager | Data Engineer / Admin |
| :--- | :---: | :---: | :---: | :---: |
| `read:analytics` | ✅ | ✅ | ✅ | ✅ |
| `read:agent_reports` | ✅ | ✅ | ✅ | ❌ |
| `read:powerbi` | ✅ | ✅ | ✅ | ✅ |
| `execute:hitl_action` | ❌ | ✅ | ✅ (Plant Specific) | ❌ |
| `override:agent_decision`| ❌ | ✅ | ❌ | ❌ |
| `manage:pipeline_dags` | ❌ | ❌ | ❌ | ✅ |
| `read:raw_telemetry` | ❌ | ✅ | ✅ | ✅ |

## Attribute-Based Access Control (ABAC) Rules

1. **Assembly Plant Filtering:**
   * `PlantOperationsManager` accounts can only view Bill of Materials (BOM) stock, line runout metrics, and telemetry targeted for their explicitly assigned assembly plant (e.g., `Sindelfingen`, `Vance`, or `Bremen`).
2. **Financial Value Masking:**
   * Line stoppage monetary figures exceeding **€100,000,000** are visible only to users holding the `Executive` or `SupplyChainDirector` roles.