#! /usr/bin/env python
"""AsciiDoc filter script which uses the websequencediagrams API
to convert websequencediagrams definitions into a PNG or SVG image
file.

Requires Internet access when used.

Copyright (C) 2012 Dag Wieers, based on websequencediagrams.com API
example code. Free use of this software is granted under the terms
of the GNU General Public License (GPL).
"""

usage = "%prog [options] inputfile"
__version__ = '1.1'

import os, sys
from optparse import *
import urllib
import re

### Configuration constants
URL = "http://www.websequencediagrams.com/"

### Global data
verbose = False

### Helper functions and classes
class AppError(Exception):
    """Application specific exception."""
    pass


def print_verbose(line):
    if verbose:
        sys.stderr.write(line + os.linesep)


### Application init and logic
class Application():
    """Application class"""

    def __init__(self):
        """Process commandline arguments"""
        global verbose
        parser = OptionParser(usage, version="%%prog %s" % __version__)
        parser.add_option("-v", "--verbose", action="store_true",
                          help="verbose output to stderr")
        parser.add_option("-o", "--outfile", help="file name of the output file")
        parser.add_option("-f", "--format", default="png", help="output format (img, png, svg or pdf)")
        parser.add_option("-s", "--style", default="default", help="image style (default, earth, modern-blue, mscgen, omegapple, qsd, rose, roundgreen, napkin)")

        self.options, args = parser.parse_args()
        verbose = self.options.verbose
        print_verbose("Runing filter script %s" % os.path.realpath(sys.argv[0]))
        if len(args) != 1:
            parser.error("Invalid number of arguments")
        self.infile = args[0]
        if self.options.outfile is None:
            if self.infile == '-':
                parser.error("OUTFILE option must be specified")
            self.options.outfile = "%s.%s" % (os.path.splitext(self.infile)[0], self.options.format)
            print_verbose("Output file is %s" % self.options.outfile)

    def run(self):
        """Core logic of the application"""
        outfile = os.path.abspath(self.options.outfile)
        outdir = os.path.dirname(outfile)

        if not os.path.isdir(outdir):
            raise AppError, 'directory does not exist: %s' % outdir

        if self.infile == '-':
            text = sys.stdin.read()
        else:
            f = open(self.infile)
            text = f.read()
            f.close()

        request = {
            'message': text,
            'style': self.options.style,
            'format': self.options.format,
            'apiVersion': '1',
        }

        url = urllib.urlencode(request)

        f = urllib.urlopen(URL, url)
        line = f.readline()
        f.close()

        expr = re.compile("(\?(img|pdf|png|svg)=[a-zA-Z0-9]+)")
        m = expr.search(line)

        if m == None:
            print "Invalid response from server."
            return False

        # To suppress asciidoc 'no output from filter' warnings.
        if self.infile == '-':
            sys.stdout.write(' ')

        urllib.urlretrieve(URL + m.group(0), outfile )

        return True

#
# Main program
#
if __name__ == "__main__":
    """Main program, called when run as a script."""
    try:
        app = Application()
        app.run()
    except KeyboardInterrupt:
        sys.exit("Ouch!")
    except Exception, e:
        sys.exit("%s: %s\n" % (os.path.basename(sys.argv[0]), e))
