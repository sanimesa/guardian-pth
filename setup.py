from setuptools import setup, find_packages
import os
import sys
from setuptools.command.install import install
import site

# Custom command to ensure the .pth file is placed correctly
class PostInstallCommand(install):
    def run(self):
        # We need to run the standard install first
        install.run(self)
        
        try:
            import os
            import site
            import shutil
            
            # 1. Determine the actual site-packages root for this install
            # If it is a venv, it should be in Lib/site-packages
            # If it is a user install, it uses site.getusersitepackages()
            
            if self.user:
                dest_dir = site.getusersitepackages()
            else:
                # Standard way to find site-packages in the current environment
                # We prioritize the one actually used by the current interpreter
                dest_dir = next((p for p in sys.path if 'site-packages' in p and 'dist-packages' not in p), None)
            
            if dest_dir and os.path.exists(dest_dir):
                src_pth = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'zzz_guardian.pth'))
                dest_pth = os.path.join(dest_dir, 'zzz_guardian.pth')
                
                print(f"DEBUG: Deploying hook to {dest_pth}")
                shutil.copyfile(src_pth, dest_pth)
                print(f"SUCCESS: Hook deployed to {dest_pth}")
            else:
                print(f"ERROR: Could not find a valid site-packages directory. sys.path was: {sys.path}")
        except Exception as e:
            print(f"CRITICAL ERROR during .pth deployment: {e}")

setup(
    name="guardian-pth",
    version="0.2.1",
    description="Stealth environment hydration via .pth hooks",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Shuvro",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    # We use a post-install hook to place the .pth file instead of data_files
    # because data_files is unreliable across platforms for .pth injection.
    # data_files=[('..', ['src/zzz_guardian.pth'])],
    cmdclass={
        'install': PostInstallCommand,
    },
    install_requires=[
        "cryptography>=42.0.0",
    ],
    python_requires=">=3.8",
)
