#encoding:utf-8
#/usr/bin/python3
from setuptools import setup
import os

if __name__ == '__main__':
	setup(	name = 'fbpred',
		version = '1.0.0',
		author = 'Júlio Álvares',
		author_email = 'juliocmalvares07@gmail.comm',
		license ='MIT',
		keywords = 'football prediction analysis',
		packages = ['fbpred',
			    'fbpred.equations'],
		install_requires = ['numpy']
	)
