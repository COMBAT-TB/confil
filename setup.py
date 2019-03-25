from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='confil',
    version='0.1.5',
    url='https://github.com/COMBAT-TB/confil',
    description='Contamination filter',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='contamination, filter',
    py_modules=['confil'],
    packages=find_packages(),
    include_package_data=True,
    license="GPLv3",
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Lavnguage :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires=[
        'click'
    ],
    entry_points={
        'console_scripts': ['confil=confil.confil:confil']
    },
)
