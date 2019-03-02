from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='confil',
    version='0.1.2',
    url='https://github.com/COMBAT-TB/confil',
    description='Contamination filter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='contamination, filter',
    py_modules=['confil'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click'
    ],
    entry_points={
        'console_scripts': ['confil=confil.confil:confil']
    },
)
