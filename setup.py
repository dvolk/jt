from setuptools import setup, find_packages

setup(
    name="jt",
    version="0.1.0",
    description="A tool to convert JSON/YAML/Helm data into tables",
    author="Denis Volk",
    author_email="dvolk@gmail.com",
    packages=find_packages(),
    install_requires=[
        "argh",
        "tabulate",
        "pyyaml",
    ],
    entry_points={
        "console_scripts": [
            "jt = jt.jt:cli",
        ],
    },
)
