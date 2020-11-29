from setuptools import setup, find_packages

setup(
    name='CdC-cognitoform-result-generator',
    version='0.1',
    packages=find_packages(),
    package_data={'CdcGenerator': ['data/*']},
    py_modules = [ 'cdcgenerator', 'fields', 'cli' ],

    install_requires=['pandas', 'setuptools', 'Click'],

    entry_points='''
        [console_scripts]
        cdcgenerator=CdcGenerator.cli:cli
    ''',

    # metadata to display on PyPI
    author='Scott Hamilton',
    author_email='sgn.hamilton+python@protonmail.com',
    description='Generates latex formatted output from an xlsx cognitoform excel sheet, made for classes councils preparation.',
    keywords='convert cdc cognitoform latex pdf',
    url='https://github.com/SCOTT-HAMILTON/CdC-cognitoform-result-generator/',
    project_urls={
        'Source Code': 'https://github.com/SCOTT-HAMILTON/CdC-cognitoform-result-generator/',
    },
    classifiers=[
        'License :: OSI Approved :: Python Software Foundation License'
    ]
)
