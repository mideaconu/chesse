from setuptools import setup

setup(
    name="encode",
    version="0.1.0",
    py_modules=["encode"],
    install_requires=[
        "Click",
    ],
    entry_points={
        "console_scripts": [
            "encode = encode:cli",
        ],
    },
)