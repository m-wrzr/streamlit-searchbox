import setuptools

setuptools.setup(
    name="streamlit-searchbox",
    version="0.1.1",
    author="m-wrzr",
    description="Autocomplete Searchbox",
    long_description="Streamlit searchbox that dynamically updates "
    + "and provides a list of suggestions based on a provided function",
    long_description_content_type="text/plain",
    url="https://github.com/m-wrzr/streamlit-searchbox",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.7, !=3.9.7",
    install_requires=[
        "streamlit >= 0.63",
    ],
    extras_require={
        "tests": ["wikipedia"],
        "dev": ["black", "isort", "ruff"],
    },
)
