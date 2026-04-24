from setuptools import setup
import os

# Identify where site-packages is to place the .pth file
from setuptools.command.install import install
class PostInstallCommand(install):
    def run(self):
        install.run(self)
        # In a real setup, we'd copy guardian.pth to the site-packages root
        # and src/* to a 'guardian' subdirectory.

setup(
    name="guardian-pth",
    version="0.1.0",
    description="Stealth environment hydration via .pth hooks",
    packages=["guardian_pth"],
    package_dir={"": "src"},
    install_requires=[
        "cryptography",
    ],
)
