.PHONY: help init benchmark test dashboard visuals clean

help:
	@echo "🍿 Netflix SQL Analytics Command Suite"
	@echo "  make init       - Initialize database & load dataset"
	@echo "  make benchmark  - Run SQL benchmark suite on all queries"
	@echo "  make test       - Run automated test suite"
	@echo "  make visuals    - Regenerate SVG documentation charts"
	@echo "  make dashboard  - Launch interactive Streamlit dashboard"
	@echo "  make clean      - Clean local build & cache artifacts"

init:
	python3 src/db_manager.py

benchmark:
	python3 src/run_sql_benchmark.py

test:
	python3 -m unittest discover -s tests -v

visuals:
	python3 src/generate_visuals.py

dashboard:
	streamlit run app/dashboard.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf data/*.db
