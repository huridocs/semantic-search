from setuptools import setup

setup(
        name="semantic_search",
        version="0.1.0",

        include_package_data=True,

        install_requires=[
            "fasttext==0.8.22",
            "mypy==0.641",
            "nltk==3.4",
            "mypy-extensions==0.4.1",
            "numpy==1.15.4",
            "pybind11==2.2.4",
            "typed-ast==1.1.0"
            ],
        )


