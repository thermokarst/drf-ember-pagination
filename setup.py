from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='drf_ember_pagination',
    version='0.1.0',
    description='Custom pagination class for ember applications',
    long_description=readme,
    author='Matthew Ryan Dillon',
    author_email='matthewrdillon@gmail.com',
    url='https://github.com/thermokarst/drf-ember-pagination',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
