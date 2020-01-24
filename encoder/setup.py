from distutils.core import setup

setup(
    name='hf1',
    version='0.1poc',
    packages=setuptools.find_packages(),
    install_requires=[
        'flask',
        'sqlalchemy',
        'flask_sqlalchemy',
        'numpy',
        'pandas',
        'behave',
        'selenium',
        'splinter',
        'pyhamcrest'
    ],
)