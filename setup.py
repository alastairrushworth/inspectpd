from setuptools import setup

setup(name = 'inspectdf',
      version = '0.1.0',
      description = 'inspectdf: Inspection, Comparison and Visualisation of Data Frames',
      url = 'http://github.com/alastairrushworth/inspectdf/python/inspectdf',
      author = 'Alastair Rushworth',
      author_email = 'alastairmrushworth@gmail.com',
      license = 'MIT',
      packages = ['inspectdf'],
      install_requires=['pandas', 'numpy', 'plotnine'],
      zip_safe = False, 
      test_suite='nose.collector',
      tests_require=['nose'])
