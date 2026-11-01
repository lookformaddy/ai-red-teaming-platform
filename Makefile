test:
	python3 -m pytest -q
demo:
	python3 demo.py
run:
	PYTHONPATH=src python3 -m red_teaming.cli --run
