### JS commands

build:
	cd streamlit_searchbox/frontend && npm run build

### Python commands

py.install:
	pip install ".[dev,tests]"

types:
	pyright .

lint:
	ruff check .

format:
	ruff format .

pre-commit:
	pre-commit install
	pre-commit run --all-files

### Distribution

# NOTE: before building and publishing the wheel you should:
# 1. bump the versions in `setup.py` and `package.json`
# 2. rebuild the frontend (currently use node `v16.20.2` / npm `8.19.4`)
#       - npm install --force
#       - npm run build
# 3. build the new wheel

wheel:
	rm -rf build dist *.egg-info
	python -m pip install --upgrade setuptools wheel twine
	python setup.py sdist bdist_wheel

# NOTE: publish to testpypi with __token__ user first
#       in new repo install:
#       pip install -i https://test.pypi.org/simple/ streamlit-searchbox==0.0.X
publish:
	python -m twine upload --repository testpypi dist/*

# NOTE: make sure you removed old dist files before. also see:
#       https://docs.streamlit.io/library/components/publish
#       https://packaging.python.org/en/latest/tutorials/packaging-projects/#next-steps
publish.real:
	python -m twine upload dist/*
