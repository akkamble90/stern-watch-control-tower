def execute_sap_reorder_bapi(part_number: str, quantity: int, vendor_id: str) -> dict:
    return {
        "bapi_status": "SUCCESS",
        "purchase_order_id": f"PO-SAP-{quantity}-9901",
        "part_number": part_number,
        "quantity": quantity,
        "vendor": vendor_id
    }