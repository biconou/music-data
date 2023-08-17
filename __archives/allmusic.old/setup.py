from setuptools import setup

setup(
   name='allmusic',
   version='0.2',
   description='A useful module',
   author='Man Foo',
   author_email='foomail@foo.example',
   packages=['allmusic'],  #same as name
   install_requires=['bs4'], #external packages as dependencies
)
