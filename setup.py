from setuptools import setup, find_packages
import os
import sys
from setuptools.command.install import install
import site

# Custom command to ensure the .pth file is placed correctly if data_files fails in some envs
class PostInstallCommand(install):
    def run(self):
        install.run(self)
        try:
            # Determine site-packages destination
            if self.user:
                dest = site.getusersitepackages()
            else:
                dest = site.getsitepackages()[0]
            
            src_pth = os.path.join(os.path.dirname(__file__), 'src', 'zzz_guardian.pth')
            dest_pth = os.path.join(dest, 'zzz_guardian.pth')
            
            print(f"Deploying hook to {dest_pth}")
            with open(src_pth, 'r') as f:
                content = f.read()
            with open(dest_pth, 'w') as f:
                f.write(content)
        except Exception as e:
            print(f"Warning: Could not auto-deploy .pth hook: {e}")

setup(
    name="guardian-pth",
    version="0.2.1",
    description="Stealth environment hydration via .pth hooks",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Shuvro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # On Windows, data_files [('', ['...'])] usually drops into the venv root or site-packages
    # but behaviors vary. We'll use this AND the PostInstallCommand for redundancy.
    data_files=[('..', ['src/zzz_guardian.pth'])],
    cmdclass={
        'install': PostInstallCommand,
    },
    install_requires=[
        "cryptography>=42.0.0",
    ],
    python_requires=">=3.8",
)
