from pathlib import Path
from setuptools import find_packages, setup
from typing import List


REQUIREMENTS_FILE = Path('.') / 'requirements.txt'


def _read_requirements(file: Path) -> List[str]:
    with open(file) as req_file:
        lines = req_file.readlines()
    return [line.rstrip() for line in lines]


setup(
    name='cardazim',
    version='0.0.1',
    author='Ethan G',
    author_email='etgold05@gmail.com',
    description='Ethan\'s Cardazim project',
    long_description='''''',
    packages=find_packages('cardazim'),
    install_requires=_read_requirements(REQUIREMENTS_FILE)
)