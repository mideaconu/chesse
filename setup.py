from setuptools import setup

setup(
    name="duchess",
    version="0.1.0",
    py_modules=["bin.encode", "bin.pgn_to_json"],
    install_requires=[
        "chess==1.8.0",
        "click==8.0.3",
    ],
    entry_points={
        "console_scripts": ["encode = bin.encode:cli", "pgn-to-json = bin.pgn_to_json:cli"],
    },
)
