from setuptools import setup, find_packages

setup(name='mylib',
      version='0.1.3',
      url='https://gitlab.com/se_ml_course/2021/sotnikov.ad/mylib',
      license='MIT',
      author='Anton Sotnikov',
      author_email='sotnikov.ad@phystech.edu',
      description='Lib for working with AMES dataset',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)
