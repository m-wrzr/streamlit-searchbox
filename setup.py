import setuptools

setuptools.setup(
    name="streamlit-searchbox",
    version="0.1.20",
    author="m-wrzr",
    description="Autocomplete Searchbox",
    long_description="Streamlit searchbox that dynamically updates "
    + "and provides a list of suggestions based on a provided function",
    long_description_content_type="text/plain",
    url="https://github.com/m-wrzr/streamlit-searchbox",
    packages=setuptools.find_packages(exclude=("tests",)),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.9, !=3.9.7",
    install_requires=[
        # version >1.37 reruns can lead to constant iFrame resets
        # version 1.35/1.36 also have reset issues but less frequent
        "streamlit >= 1.0",
    ],
    extras_require={
        "tests": [
            "wikipedia==1.4.0",
            "pytest==8.3.2",
            # NOTE: run `playwright install` to install the browser drivers
            "playwright==1.46.0",
            "pytest-playwright==0.5.1",
        ],
        "dev": [
            "pre-commit==4.0.1",
            "ruff==0.7.1",
            "pyright==1.1.377",
        ],
    },
)
