VENV = .venv
PYTHON = $(VENV)/bin/python3
PIP = $(VENV)/bin/pip3

# Load .env file and set environment variables
include .env
export $(shell sed 's/=.*//' .env)

# Need to use python 3.9 for aws lambda
$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt

# Find all *_config.py files in the current directory
CONFIG_FILES := $(wildcard *_config.py)

# Generate target names by removing _config.py suffix
TARGETS := $(patsubst %_config.py,%,$(CONFIG_FILES))

# Generic rule for running main.py with a config file
run_main = $(PYTHON) main.py $(1)

# Generate targets for each config file
$(TARGETS): %: $(VENV)/bin/activate
	$(call run_main,$@_config.py)

# Generic target for running any config
run-%: $(VENV)/bin/activate
	$(call run_main,$*.py)

clean:
	rm -rf __pycache__
	rm -rf $(VENV)