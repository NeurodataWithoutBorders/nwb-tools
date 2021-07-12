from setuptools import setup, find_packages

# Get the long description from the README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='nwb_tools',
    version='0.1.0',
    description='Command-line tools for interacting with NWB files.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Ryan Ly',
    author_email='rly@lbl.gov',
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/NeurodataWithoutBorders/nwb-tools",
    install_requires=[
        'h5py'
    ],
    entry_points={
        'console_scripts': [
            'nwbls=nwb_tools.nwb_ls:main',
        ]
    }
)
