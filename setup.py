from setuptools import setup
import stallion
import sys

req = ['Flask>=0.8',
       'setuptools>=0.6c11',
       'docutils>=0.8.1',
       'jinja2>=2.6',
       'simplejson>=2.3.0']

if sys.platform == 'win32': req += ['pywin32']

setup(
    name='Stallion',
    version=stallion.__version__,
    url='https://github.com/perone/stallion/',
    license='Apache License 2.0',
    author=stallion.__author__,
    author_email='christian.perone@gmail.com',
    description='A Python Package Manager interface.',
    long_description=open("README.rst", "r").read(),
    packages=['stallion'],
    keywords='package manager, distribution tool, stallion',
    platforms='Any',
    zip_safe=False,
    include_package_data=True,
    package_data={
      'stallion': ['static/*.*', 'templates/*.*', 'scripts/*.*'],
    },
    entry_points={
        'console_scripts': [
            'stallion-service = stallion.scripts.stallion_service:run'
        ]
    },
    install_requires=req,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
