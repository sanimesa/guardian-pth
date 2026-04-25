from setuptools import setup, find_packages
import os

setup(
    name="guardian-pth",
    version="0.3.0",
    description="Stealth environment hydration via sitecustomize/pth hooks",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Shuvro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # Option A: Install sitecustomize.py as a top-level module.
    # This is loaded automatically by the interpreter on startup.
    py_modules=["sitecustomize"],
    install_requires=[
        "cryptography>=42.0.0",
    ],
    python_requires=">=3.8",
)
