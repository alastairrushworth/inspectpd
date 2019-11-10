from setuptools import setup

setup(name = 'inspectpd',
      version = '0.1.0',
      description = 'inspectpd: Inspection, Comparison and Visualisation of Data Frames',
      url = 'http://github.com/alastairrushworth/inspectpd',
      author = 'Alastair Rushworth',
      author_email = 'alastairmrushworth@gmail.com',
      license = 'MIT',
      packages = ['inspectpd'],
      install_requires = ['numpy', 'pandas', 'plotnine', 'scipy'],
      zip_safe = False, 
      test_suite='nose.collector',
      tests_require=['nose'])
