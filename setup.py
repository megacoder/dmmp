#!/usr/bin/env python
# vim: nonu noet ai sm ts=4 sw=4

from setuptools import setup, find_packages

Name    = 'dmmp'
Runtime	= 'dmmp'
Version = '1.0.0'

with open( '{0}/version.py'.format( Name ), 'wt' ) as f:
    print >>f, 'Version = "{0}"'.format( Version )

setup(
    name				= Name,
    version				= Version,
    description			= 'Canonical display of /etc/multipath.conf',
	long_description	= open( 'README.md' ).read(),
    url					= 'http://www.megacoder.com',
    author				= 'Tommy Reynolds',
    author_email		= 'oldest.software.guy@gmail.com',
    packages			= [ Name ],
    scripts				= [
        '{0}/scripts/{1}'.format(
			Name,
			Runtime
		),
    ]
)

