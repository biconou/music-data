import setuptools
from allmusicgrabber.version import Version


setuptools.setup(name='allmusicgrabber',
                 version=Version('0.1').number,
                 description='Python Package Boilerplate',
                 long_description=open('README.md').read().strip(),
                 author='Package Author',
                 author_email='you@youremail.com',
                 url='http://path-to-my-packagename',
                 py_modules=['globals','artist'],
                 install_requires=[],
                 license='MIT License',
                 zip_safe=False,
                 keywords='boilerplate package',
                 classifiers=['Packages', 'Boilerplate'])
