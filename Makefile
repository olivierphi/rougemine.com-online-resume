PYTHON_BINS ?= .venv/bin
PYTHON ?= ${PYTHON_BINS}/python
POETRY ?= ${PYTHON_BINS}/poetry
POETRY_INSTALL_OPTS ?=
DJANGO_SETTINGS_MODULE ?= project.settings.development
SUB_MAKE = ${MAKE} --no-print-directory

.DEFAULT_GOAL := help

help:
# @link https://github.com/marmelab/javascript-boilerplate/blob/master/makefile
	@grep -P '^[a-zA-Z/_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install: .venv python_deps ## Install the Python dependencies
	${PYTHON_BINS}/pre-commit install

.PHONY: dev
dev: address ?= 127.0.0.1
dev: port ?= 8000
dev: debug ?= true
dev: install # Start Django dev server, as well as Tailwind compilation in the background
	@DEBUG=${debug} ${PYTHON} manage.py tailwind runserver ${address}:${port}

.PHONY: build
build: debug ?= 0
build: ## Build the static assets (HTML files, CSS files, etc.)
	@DEBUG=${debug} ${PYTHON} manage.py build_resume

.PHONY: dist-serve
dist-serve: address ?= 127.0.0.1
dist-serve: port ?= 3000
dist-serve: build # Serve the built static assets from the "dist/" folder via HTTP
	@${PYTHON} -m http.server --directory dist/ --bind ${address} ${port}

.PHONY: create-colourised-tech-icons
create-colourised-tech-icons: ##  Create greyscaled-and-colourised versoins of the "tech" icons
	@${PYTHON} manage.py create_colourised_version_of_tech_icons

.PHONY: build-and-create-pdfs
build-and-create-pdfs: create-colourised-tech-icons build playwright_install ##  Build static assets and create PDF files from them
	@${PYTHON} manage.py resume_create_pdfs

.PHONY: code-quality/all
code-quality/all: code-quality/black code-quality/djlint code-quality/ruff code-quality/mypy  ## Run all our code quality tools

.PHONY: code-quality/black
code-quality/black: black_opts ?=
code-quality/black: ## Automated 'a la Prettier' code formatting
# @link https://black.readthedocs.io/en/stable/
	@${PYTHON_BINS}/black ${black_opts} myresume/

.PHONY: code-quality/djlint
code-quality/djlint: djlint_opts ?= --lint --reformat
code-quality/djlint: ## Automated 'a la Prettier' formatting for Django HTML templates
# @link https://djlint.com/
	@${PYTHON_BINS}/djlint ${djlint_opts} myresume/

.PHONY: code-quality/ruff
code-quality/ruff: ruff_opts ?= --fix
code-quality/ruff: ## Fast linting
# @link https://mypy.readthedocs.io/en/stable/
	@PYTHONPATH=${PYTHONPATH} ${PYTHON_BINS}/ruff myresume/ ${ruff_opts}

.PHONY: code-quality/mypy
code-quality/mypy: mypy_opts ?=
code-quality/mypy: ## Python's equivalent of TypeScript
# @link https://mypy.readthedocs.io/en/stable/
	@PYTHONPATH=${PYTHONPATH} ${PYTHON_BINS}/mypy myresume/ ${mypy_opts}

# Here starts the "misc util targets" stuff

.venv: poetry_version ?= 1.8.3
.venv: ## Initialises the Python virtual environment in a ".venv" folder
	@python -m venv .venv
	@${PYTHON_BINS}/pip install -U pip poetry==${poetry_version}

.PHONY: python_deps
python_deps: ## Installs the Python dependencies
	@${POETRY} install --no-root ${POETRY_INSTALL_OPTS}

.PHONY: playwright_install
playwright_install: browsers ?= chromium
playwright_install: python_deps ## Installs Playwright's browser binaries
	@${PYTHON_BINS}/playwright install ${browsers}
