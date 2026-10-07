import os
import json
import logging
import logging.config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def setup_logging(default_level=logging.INFO) -> logging.Logger:
    """Initializes logging configuration and verifies data directories."""
    
    data_dirs = [
        BASE_DIR / "data" / "sample_manifests",
        BASE_DIR / "data" / "telemetry_fixtures",
        BASE_DIR / "data" / "mocks",
    ]
    for d in data_dirs:
        d.mkdir(parents=True, exist_ok=True)

    config_path = BASE_DIR / "config" / "logging_config.json"
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            
            log_file = BASE_DIR / "control_tower.log"
            if "handlers" in config and "file_json" in config["handlers"]:
                config["handlers"]["file_json"]["filename"] = str(log_file)
                
            logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

    logger = logging.getLogger("SternWatch")
    return logger

logger = setup_logging()