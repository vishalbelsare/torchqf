PROJECT_NAME := torchqf

.PHONY: install
install:
	@poetry install

.PHONY: test
test:
	@poetry run pytest --doctest-modules $(PROJECT_NAME)
	@poetry run pytest --doctest-modules tests

.PHONY: lint
lint:
	@poetry run python3 -m black --check --quiet .
	@poetry run python3 -m isort --check --force-single-line-imports --quiet .

.PHONY: format
format:
	@poetry run python3 -m black --quiet .
	@poetry run python3 -m isort --force-single-line-imports --quiet .
