#!/usr/bin/env python

from setuptools import setup

setup(
    name='Xadmin Demo',
    version='1.0',
    description='OpenShift Xadmin Demo',
    author='TM',
    author_email='sshwsfc@gmail.com',
    url='http://github.com/sshwsfc/xadmin-demo',
    install_requires=['greenlet', 'gevent', 'MySQL-python', 'django-mptt'],
)
