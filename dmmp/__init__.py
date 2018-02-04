#!/usr/bin/python
# vim: noet sw=4 ts=4

import	sys
import	os
import	shlex
import	argparse

try:
	from version import	Version
except:
	Version = 'W.T.F.'

class	DMMP():

	def	__init__( self ):
		self.input = list()
		return

	def	do_section( self, name = '.TOP' ):
		attrs = dict()
		while len(self.input):
			tokens = self.input.pop(0)
			N = len( tokens )
			if N == 2 and tokens[ 1 ] == '{':
				section_name = tokens[ 0 ]
				attrs[ section_name ] = attrs.get( section_name, list() ) + [
					self.do_section( section_name )
				]
			elif N == 1 and tokens[ 0 ] == '}':
				break
			elif N == 2:
				attrs[ tokens[ 0 ] ] = tokens[ 1 ]
			elif N > 2:
				attrs[ tokens[ 0 ] ] = ''.join( tokens[ 1: ] )
			else:
				print 'ignoring {0}'.format( tokens )
		return attrs

	def	indent( self, depth ):
		return (' ' * 4) * depth

	def	quote( self, s ):
		return s if s.isdigit() else '"{0}"'.format( s )

	def	show( self, title, attrs, depth = 0 ):
		if title:
			print '{0}{1}  {{'.format( self.indent( depth ), title )
			depth += 1
		width = max(
			map(
				len,
				attrs.keys()
			)
		)
		fmt = self.indent( depth ) + '{{0:{0}{1}}}  {{1}}'.format(
			'>' if False else '',
			width
		)
		for key in sorted( attrs ):
			node = attrs[ key ]
			if isinstance( node, str ):
				print fmt.format(
					key,
					self.quote( node )
				)
			elif isinstance( node, dict ):
				self.show( key, node, depth )
			elif isinstance( node, list ):
				for item in node:
					self.show( key, item, depth )
			else:
				print '*** What is a {0}:{1}:{2}?'.format(
					name,
					type( node ),
					node
				)
		if title:
			depth -= 1
			print '{0}}}'.format( self.indent( depth ) )
		return

	def	do_open_file( self, f = sys.stdin ):
		self.input = list()
		for line in f:
			tokens = [x for x in shlex.shlex(line,posix=True)]
			if len(tokens):
				self.input.append( tokens )
		# print 'input={0}'.format( input )
		name = 'TOP LEVEL'
		attrs = self.do_section( name )
		self.show( None, attrs )
		return

	def	do_name( self, name ):
		with open( name ) as f:
			self.do_open_file( f )
		return

	def	main( self ):
		p = argparse.ArgumentParser(
			description = '''Show /etc/multipath.conf in a canonical
				format.''',
			epilog = '''Neat, sweet, petite'''
		)
		p.add_argument(
			'-o',
			'--out',
			metavar = 'FILE',
			dest = 'ofile',
			help = 'write here instead of stdout',
		)
		p.add_argument(
			'-v',
			'--version',
			action  = 'version',
			version = Version,
			help    = 'Version {0}'.format( Version ),
		)
		p.add_argument(
			dest    = 'files',
			metavar = 'FILE',
			nargs   = '*',
			default = None,
			help    = 'multipath configuration files',
		)
		self.opts = p.parse_args()
		if self.opts.ofile:
			sys.stdout = open( self.opts.ofile, 'wt' )
		if self.opts.files:
			for name in self.opts.files:
				self.do_name( files )
		else:
			self.do_open_file( sys.stdin )
		return 0

if __name__ == '__main__':
	dmmp = DMMP()
	exit( dmmp.main() )
