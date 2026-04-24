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
            # We import here to ensure site is available
            import site
            import shutil
            
            # Use sys.executable to find the current site-packages
            import sys
            import os
            
            # Find site-packages for the current environment
            # This is more robust than site.getsitepackages() in some venvs
            sp = [p for p in sys.path if 'site-packages' in p and 'venv' in p]
            if not sp:
                sp = site.getsitepackages()
            
            if sp:
                dest_dir = sp[0]
                src_pth = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src', 'zzz_guardian.pth'))
                dest_pth = os.path.join(dest_dir, 'zzz_guardian.pth')
                
                print(f"DEBUG: Deploying hook from {src_pth} to {dest_pth}")
                shutil.copyfile(src_pth, dest_pth)
                print(f"SUCCESS: Hook deployed to {dest_pth}")
            else:
                print("ERROR: Could not find site-packages directory.")
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
