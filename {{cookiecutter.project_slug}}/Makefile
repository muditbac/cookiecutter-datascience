.PHONY: clean lint requirements sync_data_to_s3 sync_data_from_s3 install uninstall


BUCKET = {{cookiecutter.s3_bucket}}
PROFILE = {{cookiecutter.aws_profile}}
PROJECT_NAME = {{cookiecutter.project_slug}}
PYTHON_INTERPRETER = {{cookiecutter.python_interpreter}}

## Install project requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt

## Lint using flake8
lint:
	flake8 $(PROJECT_NAME)

## Delete all compiled Python files
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf *.egg-info

## Install package in editable mode
install: requirements
	$(PYTHON_INTERPRETER) -m pip install --editable .

## Uninstalls only packages, not dependencies
uninstall:
	$(PYTHON_INTERPRETER) -m pip uninstall $(PROJECT_NAME) -y


## Upload Data to S3
sync_data_to_s3:
ifeq (default,$(PROFILE))
	aws s3 sync data/ s3://$(BUCKET)/data/
else
	aws s3 sync data/ s3://$(BUCKET)/data/ --profile $(PROFILE)
endif

## Download Data from S3
sync_data_from_s3:
ifeq (default,$(PROFILE))
	aws s3 sync s3://$(BUCKET)/data/ data/
else
	aws s3 sync s3://$(BUCKET)/data/ data/ --profile $(PROFILE)
endif

## Sacred infra up
sacred_up:
	mkdir -p data/mongodb
	docker-compose -f docker/docker-compose.yml up

## Sacred infra up
sacred_down:
	mkdir -p data/mongodb
	docker-compose -f docker/docker-compose.yml down -v
