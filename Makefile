PYTHON_FILES := $(shell find nfl_sacks_app -name '*.py')

ENV := poetry

.PHONY: install_env install_dev_env lint format check_format run clean

install_env:
	$(ENV) install --no-dev

install_dev_env:
	$(ENV) install

format:
	$(ENV) run poetry run ruff check --fix $(PYTHON_FILES)

check_format:
	$(ENV) run poetry run ruff check $(PYTHON_FILES)

run:
	streamlit run __main__.py

clean:
	rm -rf .mypy_cache .ruff_cache .qodo
