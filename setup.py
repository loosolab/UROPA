import os
import sys
import re
import setuptools
from setuptools import setup

#Requires minimum python 3.2
if sys.version_info[0] > 3 or (sys.version_info[0] == 3 and sys.version_info[1] >= 2):
  pass
else:
    sys.exit("ERROR: UROPA install requires python>=3.2")

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
      python_requires='>=3.2',
      install_requires=[
        'pysam',
        'psutil',
        'numpy'
      ],
      classifiers = [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python '
      ],
      zip_safe=False,
      include_package_data=True)
