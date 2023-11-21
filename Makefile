include Makefile.config
-include Makefile.custom.config

all: install lint check check-outdated

install:
	test -d $(VENV) || $(PYTHON_VERSION) -m venv $(VENV)
	$(PIP) install --upgrade --upgrade-strategy eager \
		pip setuptools twine -e .[test,docs] devcore

clean:
	rm -fr $(VENV)
	rm -fr *.egg-info

lint:
	$(RUFF) $(PROJECT_NAME)

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
	$(PYTHON) setup.py sdist bdist_wheel
	$(TWINE) upload dist/*
	git push
	git push --tags
