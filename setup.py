from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="chesse",
    version="0.0.1",
    author="Mihai Ionut Deaconu",
    author_email="mihai.ionut.deaconu@gmail.com",
    description="CheSSE (Chess Similarity Search Engine) utility functions package",
    long_description=long_description,
    url="https://github.com/mideaconu/chesse",
    py_modules=["encoding.encode", "scripts.pgn_to_json"],
    install_requires=["chess==1.8.0", "click==8.0.3"],
    entry_points={
        "console_scripts": [
            "encode = encoding.encode:cli",
            "pgn-to-json = scripts.pgn_to_json:cli",
        ],
    },
)
