import os
from os.path import basename
from setuptools import setup, find_packages
from glob import glob


def get_transforms_data():
    # Installs the schema files in jwst/transforms
    # Because the path to the schemas includes "stsci.edu" they
    # can't be installed using setuptools.
    transforms_schemas = []
    root = os.path.join(NAME, 'transforms', 'schemas')
    for node, dirs, files in os.walk(root):
        for fname in files:
            if fname.endswith('.yaml'):
                transforms_schemas.append(
                    os.path.relpath(os.path.join(node, fname), root))
    # In the package directory, install to the subdirectory 'schemas'
    transforms_schemas = [os.path.join('schemas', s) for s in transforms_schemas]
    return transforms_schemas


NAME = 'jwst-test'
SCRIPTS = [s for s in glob('scripts/*') if basename(s) != '__pycache__']
PACKAGE_DATA = {
    '': [
        '*.fits',
        '*.txt',
        '*.inc',
        '*.cfg',
        '*.csv',
        '*.yaml',
        '*.json',
        '*.asdf'
    ]
}
DOCS_REQUIRE = [
    'matplotlib',
    'sphinx',
    'sphinx-automodapi',
    'sphinx-rtd-theme',
    'stsci-rtd-theme',
    'sphinx-astropy',
    'sphinx-asdf',
]
TESTS_REQUIRE = [
    'ci-watson>=0.3.0',
    'pytest>=4.6.0',
    'pytest-doctestplus',
    'requests_mock>=1.0',
    'pytest-openfiles>=0.5.0',
    'pytest-cov>=2.9.0',
    'codecov>=1.6.0',
]
AWS_REQUIRE = [
    'stsci-aws-utils>=0.1.2'
]
ENTRY_POINTS = dict(asdf_extensions=['jwst_pipeline = jwst.transforms.jwextension:JWSTExtension',
                                     'jwst_datamodel = jwst.datamodels.extension:DataModelExtension'])

transforms_schemas = get_transforms_data()
PACKAGE_DATA['jwst.transforms'] = transforms_schemas

setup(
    name=NAME,
    use_scm_version=True,
    author='JWST Pipeline developers',
    description='Python library for science observations from the James Webb Space Telescope',
    long_description=('The JWST Data Reduction Pipeline is a Python '
                      'software suite that automatically processes the '
                      'data taken by the JWST instruments NIRCam, NIRSpec, '
                      'NIRISS, MIRI, and FGS to remove instrumental signatures '
                      'from the observations.'),
    url='https://github.com/spacetelescope/jwst',
    license='BSD',
    classifiers=[
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: C',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',
    scripts=SCRIPTS,
    packages=find_packages(),
    package_data=PACKAGE_DATA,
    setup_requires=[
        'setuptools_scm',
    ],
    install_requires=[
        'asdf>=2.7.1',
        'astropy>=4.0',
        'crds>=7.4.1.3',
        'drizzle>=1.13',
        'gwcs>=0.14.0',
        'jsonschema>=3.0.2',
        'numpy>=1.16',
        'photutils>=0.7',
        'pyparsing>=2.2',
        'requests>=2.22',
        'scipy>=1.1.0',
        'spherical-geometry>=1.2.2',
        'stsci.image>=2.3.3',
        'tweakwcs>=0.6.4',
    ],
    extras_require={
        'docs': DOCS_REQUIRE,
        'ephem': ['pymssql-linux==2.1.6', 'jplephem==2.9'], # for timeconversion
        'test': TESTS_REQUIRE,
        'aws': AWS_REQUIRE,
    },
    tests_require=TESTS_REQUIRE,
    entry_points=ENTRY_POINTS,
)
