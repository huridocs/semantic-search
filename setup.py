from setuptools import setup

setup(
        name="semantic_search",
        version="0.1.0",

        url="https://github.com/Tilana/semantic-search",
        description="search for semantically related sentences",
        long_description=open("README.md").read(),

        packages=["semantic_search"],
        include_package_data=True,

        install_requires=[
            "fasttext==0.9.1",
            "mypy==0.641",
            "nltk==3.4",
            "mypy-extensions==0.4.1",
            "numpy==1.22.0",
            "pybind11==2.3.0",
            "typed-ast==1.1.0"
            ],
        )


