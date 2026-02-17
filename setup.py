'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''
from setuptools import find_packages, setup
from typing import List

def get_requirements()->List[str]:
    
    requirement_list:List[str] = []

    try:
        with open('requirements.txt', 'r') as file:
            for line in file:
                if line.strip() and '-e .' not in line:
                    requirement_list.append(line.strip())
    except FileNotFoundError:
        print('requirements file not found!')
    
    return requirement_list

setup(
    name='Network Security Machine Learning Project',
    version='0.0.1',
    author='Bijon Lahiri',
    author_email='bijonlahiri@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
)