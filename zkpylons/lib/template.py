from mako.lookup import TemplateLookup
import os, stat, posixpath, re
from mako import exceptions, util
from mako.template import Template

class ZookeeprTemplateLookup(TemplateLookup):
    def get_template(self, uri):
        """Return a :class:`.Template` object corresponding to the given
        URL.

        Note the "relativeto" argument is not supported here at the moment.

        """
 
        try:
            if self.filesystem_checks:
                return self._check(uri, self._collection[uri])
            else:
                return self._collection[uri]
        except KeyError:
            u = re.sub(r'^\/+', '', uri)
            print self.directories, uri, u
            for dir in self.directories:
                print dir
                srcfile = posixpath.normpath(posixpath.join(dir, u))
                if os.path.isfile(srcfile):
                    return self._load(srcfile, uri)
            else:
                raise exceptions.TopLevelLookupException(
                                    "Cant locate template for uri %r" % uri)
