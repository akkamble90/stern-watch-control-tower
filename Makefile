
# ==============================================================================
# MERCEDES-BENZ CONTROL TOWER PLATFORM - MAKEFILE
# ==============================================================================

.PHONY: help install db-init run-producer run-spark run-ui test clean

# Default Python & Environment configuration
PYTHON = venv/bin/python
PIP = venv/bin/pip
STREAMLIT = venv/bin/streamlit

help:
	@echo "Available commands:"
	@echo "  make install      : Create virtual environment and install dependencies"
	@echo "  make db-init      : Initialize PostgreSQL database tables and static seed data"
	@echo "  make run-producer : Launch Kafka telemetry stream producer"
	@echo "  make run-spark    : Launch PySpark Structured Streaming consumer pipeline"
	@echo "  make run-ui       : Launch Streamlit Control Tower dashboard UI"
	@echo "  make clean        : Remove Python bytecode and temporary cache directories"

install:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "Dependencies successfully installed."

db-init:
	$(PYTHON) -c "import sqlalchemy; engine = sqlalchemy.create_engine('postgresql://postgres:password123@localhost:5432/control_tower_db'); conn = engine.connect(); conn.execute(sqlalchemy.text(''' \
	CREATE TABLE IF NOT EXISTS telemetry_events ( \
		event_id VARCHAR(64) PRIMARY KEY, \
		vehicle_id VARCHAR(32) NOT NULL, \
		latitude DOUBLE PRECISION NOT NULL, \
		longitude DOUBLE PRECISION NOT NULL, \
		speed DOUBLE PRECISION, \
		temperature DOUBLE PRECISION, \
		timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP \
	); \
	CREATE TABLE IF NOT EXISTS warehouse_facilities ( \
		warehouse_id VARCHAR(32) PRIMARY KEY, \
		warehouse_name VARCHAR(128) NOT NULL, \
		location VARCHAR(128) NOT NULL, \
		total_capacity_pallets INT NOT NULL, \
		current_stock INT NOT NULL, \
		utilization_pct DOUBLE PRECISION NOT NULL, \
		dispatched_today INT NOT NULL, \
		delayed_orders INT NOT NULL \
	); \
	INSERT INTO warehouse_facilities VALUES \
	('WH-01', 'Stuttgart Central Hub', 'Stuttgart, Germany', 50000, 43500, 87.0, 2400, 120), \
	('WH-02', 'Bremen Distribution Center', 'Bremen, Germany', 35000, 31200, 89.1, 1850, 95), \
	('WH-03', 'Sindelfingen Logistics Depot', 'Sindelfingen, Germany', 42000, 34000, 81.0, 2100, 45), \
	('WH-04', 'Tuscaloosa Assembly Hub', 'Tuscaloosa, USA', 30000, 22500, 75.0, 1200, 110), \
	('WH-05', 'Beijing Supply Depot', 'Beijing, China', 45000, 41400, 92.0, 2900, 230) \
	ON CONFLICT (warehouse_id) DO NOTHING; \
	CREATE TABLE IF NOT EXISTS fulfillment_kpis ( \
		metric_id VARCHAR(32) PRIMARY KEY, \
		metric_name VARCHAR(64) NOT NULL, \
		order_volume INT NOT NULL, \
		percentage DOUBLE PRECISION NOT NULL \
	); \
	INSERT INTO fulfillment_kpis VALUES \
	('M-01', 'On-Time Delivered', 136240, 88.0), \
	('M-02', 'Delayed Shipments', 12380, 8.0), \
	('M-03', 'Returned Orders', 6200, 4.0) \
	ON CONFLICT (metric_id) DO NOTHING; \
	''')); conn.commit(); print('Database schema and seed data successfully initialized!')"

run-producer:
	$(PYTHON) src/ingestion/kafka_producers/telemetry_producer.py

run-spark:
	$(PYTHON) src/ingestion/spark_streaming/telemetry_geofence_stream.py

run-ui:
	$(STREAMLIT) run src/ui/main.py

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__ */*/*/__pycache__ .pytest_cache
	@echo "Cleaned temporary cache files.