from setuptools import setup, find_packages


install_requires = [
      'matplotlib==3.3.4', 'numpy==1.20.1', 'pandas>= 0.25.3', 'scikit-learn==0.24.1',
      'scipy==1.6.1', 'seaborn==0.11.1', 'py-rouge>=1.1', 'flask==1.1.2'
]

tests_require = [
      'pytest==6.2.3', 'pytest-cov==2.11.1', 'hypothesis==6.10.0', 'coverage==5.5'
    ]

setup(name='mylib',
      version='0.1.3',
      url='https://gitlab.com/se_ml_course/2021/sotnikov.ad/mylib',
      author='Anton Sotnikov',
      author_email='sotnikov.ad@phystech.edu',
      description='Lib for working with AMES dataset',
      install_requires=install_requires,
      tests_require=tests_require,
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      zip_safe=False)
