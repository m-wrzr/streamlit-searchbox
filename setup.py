import setuptools

setuptools.setup(
    name="streamlit-searchbox",
    version="0.1.17",
    author="m-wrzr",
    description="Autocomplete Searchbox",
    long_description="Streamlit searchbox that dynamically updates "
    + "and provides a list of suggestions based on a provided function",
    long_description_content_type="text/plain",
    url="https://github.com/m-wrzr/streamlit-searchbox",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8, !=3.9.7",
    install_requires=[
        # version >1.37 reruns can lead to constant iFrame resets
        # version 1.35/1.36 also have reset issues but less frequent
        "streamlit >= 1.0",
    ],
    extras_require={
        "tests": [
            "wikipedia",
            "pytest",
            "pytest-playwright",
        ],
        "dev": [
            "pre-commit",
            "black",
            "isort",
            "ruff",
            "pyright",
        ],
    },
)
