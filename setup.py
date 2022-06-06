from setuptools import setup

setup(
    name="chesse",
    version="0.0.1",
    py_modules=["encoding.encode", "scripts.pgn_to_json"],
    install_requires=["chess==1.8.0", "click==8.0.3"],
    entry_points={
        "console_scripts": [
            "encode = encoding.encode:cli",
            "pgn-to-json = scripts.pgn_to_json:cli",
        ],
    },
)
