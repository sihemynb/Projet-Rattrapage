from setuptools import setup, find_packages

setup(
    name="projet_rattrapage",
    version="0.1",
    author="Sihem YENBOU",
    description="Projet Python ISUP 2025 – Analyse NBA",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pandas",
        "matplotlib",
        "seaborn",
        "numpy"
    ],
    python_requires=">=3.8",
)
