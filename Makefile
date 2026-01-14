VENV := venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
GUNICORN := $(VENV)/bin/gunicorn

.PHONY: help venv install run wsgi test clean

help:
	@echo "Targets:"
	@echo "  make venv         Create virtual environment"
	@echo "  make install      Install dependencies"
	@echo "  make install-dev  Install development dependencies"
	@echo "  make run          Run Flask dev server (debug)"
	@echo "  make wsgi         Run production WSGI server locally (gunicorn)"
	@echo "  make test         Run tests"
	@echo "  make clean        Remove venv and caches"

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install -r requirements.txt

install-dev: install
	$(PIP) install -r requirements-dev.txt

run: install
	$(PYTHON) main.py

# Production-like local run (Linux/macOS). Binds to http://127.0.0.1:8000
wsgi: install
	$(GUNICORN) -w 2 -b 127.0.0.1:8000 wsgi:app

test: install-dev
	$(PYTHON) -m pytest

clean:
	rm -rf $(VENV) __pycache__ .pytest_cache .coverage htmlcov
