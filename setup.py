from setuptools import setup

setup(
    name="chesse",
    version="0.1.0",
    py_modules=["bin.encode", "bin.pgn_to_json"],
    install_requires=[
        "chess==1.8.0",
        "click==8.0.3",
        "elasticsearch==8.1.0",
        "google-api-python-client==2.39.0",
        "grpcio==1.44.0",
        "grpcio-tools==1.44.0",
        "grpcio-reflection==1.44.0",
    ],
    entry_points={
        "console_scripts": ["encode = bin.encode:cli", "pgn-to-json = bin.pgn_to_json:cli"],
    },
)
