import os
import re
import setuptools
from setuptools import setup

#Path of setup file to establish version
setupdir = os.path.abspath(os.path.dirname(__file__))

def find_version(init_file):
  version_file = open(init_file).read()
  version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
  if version_match:
    return version_match.group(1)
  else:
    raise RuntimeError("Unable to find version string.")

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='uropa',
      version=find_version(os.path.join(setupdir, "uropa", "__init__.py")),
      description='UROPA is a command line based tool, intended for genomic region annotation',
      long_description=readme(),
      long_description_content_type='text/markdown',
      url='https://github.molgen.mpg.de/loosolab/UROPA',
      author='Jens Preussner',
      author_email='jens.preussner@mpi-bn.mpg.de',
      license='MIT',
      packages=['uropa'],
      entry_points = {
        'console_scripts': ['uropa = uropa.uropa:main']
      },
      scripts = ['utils/uropa_summary.R','utils/uropa2gtf.R'],
      install_requires=[
        'numpy',
        'pysam',
      ],
      classifiers = [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python '
      ],
      zip_safe=False,
      include_package_data=True)
