from setuptools import setup

setup(name = 'inspectpy',
      version = '0.1.0',
      description = 'inspectpd: Inspection, Comparison and Visualisation of Data Frames',
      url = 'http://github.com/alastairrushworth/inspectpd',
      author = 'Alastair Rushworth',
      author_email = 'alastairmrushworth@gmail.com',
      license = 'MIT',
      packages = ['inspectpd'],
      install_requires=['pandas', 'numpy', 'plotnine'],
      zip_safe = False, 
      test_suite='nose.collector',
      tests_require=['nose'])
