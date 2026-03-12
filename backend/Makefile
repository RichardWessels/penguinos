.PHONY: lint format check

PYTHON_DIRS := dopios_backend mainApp scripts

lint:
	ruff format $(PYTHON_DIRS)
	pylint $(PYTHON_DIRS)
