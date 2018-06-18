include Makefile.config
-include Makefile.custom.config

all: install lint check check-outdated

install:
	test -d $(VENV) || virtualenv $(VENV) -p $(PYTHON_VERSION)
	$(PIP) install --upgrade --upgrade-strategy eager pip setuptools -e .[test,docs] devcore

clean:
	rm -fr $(VENV)
	rm -fr *.egg-info

lint:
	$(PYTEST) --flake8 -m flake8 $(PROJECT_NAME)
	$(PYTEST) --isort -m isort $(PROJECT_NAME)

fix:
	$(VENV)/bin/yapf -p -i pygal/**/*.py

check:
	$(PYTEST) $(PROJECT_NAME) $(PYTEST_ARGS) --cov-report= --cov=pygal

check-outdated:
	$(PIP) list --outdated --format=columns

visual-check:
	$(PYTHON) demo/moulinrouge.py

.PHONY: docs
docs:
	cd docs && PYTHON_PATH=$(VENV) PATH=$(VENV)/bin:$(PATH) $(MAKE) rst html

release: docs
	git pull
	$(eval VERSION := $(shell PROJECT_NAME=$(PROJECT_NAME) $(VENV)/bin/devcore bump $(LEVEL)))
	git commit -am "Bump $(VERSION)"
	git tag $(VERSION)
	$(PYTHON) setup.py sdist bdist_wheel upload
	git push
	git push --tags
