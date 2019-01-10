from setuptools import setup

def readme():
    with open('README.md', encoding='utf-8') as f:
        return f.read()

setup(name='uropa',
      version='2.0.3',
      description='UROPA is a command line based tool, intended for genomic region annotation',
      long_description=readme(),
      url='https://github.molgen.mpg.de/loosolab/UROPA',
      author='Jens Preussner',
      author_email='jens.preussner@mpi-bn.mpg.de',
      license='MIT',
      packages=['uropa'],
      entry_points = {
        'console_scripts': ['uropa = uropa.uropa:main']
      },
      scripts = ['utils/uropa_summary.R', 'utils/uropa_reformat_output.R', 'utils/uropa2gtf.R'],
      install_requires=[
        'numpy',
        'pysam'
      ],
      classifiers = [
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3.4'
      ],
      zip_safe=False,
      include_package_data=True)
