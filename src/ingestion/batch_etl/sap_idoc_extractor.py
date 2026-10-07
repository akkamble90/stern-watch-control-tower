import pandas as pd
from datetime import datetime
from src.common.logger import logger

def extract_sap_idoc_batch() -> pd.DataFrame:
    logger.info("Executing batch extract for SAP iDoc inventory records...")
    data = [
        {"idoc_number": "000000109283", "part_number": "MCU-A32-S", "plant": "Sindelfingen", "stock_qty": 450, "extract_time": datetime.utcnow()},
        {"idoc_number": "000000109284", "part_number": "ORIN-DRIVE-AGX", "plant": "Vance", "stock_qty": 120, "extract_time": datetime.utcnow()}
    ]
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = extract_sap_idoc_batch()
    print(df)