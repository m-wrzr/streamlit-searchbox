### JS commands

build:
	cd streamlit_searchbox/frontend && npm run build

### Python commands

run:
	uv run streamlit run example.py

types:
	uv run pyright .

lint:
	uv run ruff check .

format:
	uv run ruff format .

pre-commit:
	uv run pre-commit install
	uv run pre-commit run --all-files

### Distribution

setup:
	uv tool install build
	uv tool install twine

# NOTE: before building and publishing the wheel you should:
# 1. bump the versions in `setup.py` and `package.json`
# 2. rebuild the frontend (currently use node `v16.20.2` / npm `8.19.4`)
#       - npm install --force
#       - npm run build
# 3. build the new wheel

wheel:
	$(MAKE) setup
	rm -rf build dist *.egg-info
	rm -rf streamlit_searchbox/frontend/node_modules/flatted/python
	uv build

# NOTE: publish to testpypi / __token__
#       in new repo install:
#       pip install -i https://test.pypi.org/simple/ streamlit-searchbox==0.0.X
#
#       in pyproject.toml you can specify:
#       version = "0.1.23rc5"
publish:
	uv run twine upload --repository testpypi dist/*

# NOTE: make sure you removed old dist files before. also see:
#       https://docs.streamlit.io/library/components/publish
#       https://packaging.python.org/en/latest/tutorials/packaging-projects/#next-steps
publish.real:
	uv run twine upload dist/*
