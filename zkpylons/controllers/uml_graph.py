# as per http://bel-epa.com/posts/elixir-dot-model.xml
# requires dot (from graphviz)

import sqlalchemy as sa
from pylons import request, response, tmpl_context as c
from zkpylons.lib.base import BaseController, render
import zkpylons.model as model
from zkpylons.model import *
from zkpylons.model.meta import Base

import inspect
from sqlalchemy.orm.attributes import InstrumentedAttribute
import os
import tempfile
import commands

class UmlGraphController(BaseController):

    def dotmodel(self, format='png'):
        classes = [m for m in model.__dict__.values() 
                        if inspect.isclass(m) 
                            and issubclass(m, Base) 
                            and m.__name__ != 'Base' ]
        op = 'digraph G {\n'
        op += 'node [shape=plaintext fontsize=14 ]\n'
        op += 'edge [arrowsize=0.75 fontsize=14 fontcolor=blue]\n'
        
        for c in classes:
            #manytoones = [f for f in c._descriptor.relationships
            #                if f.__class__ == elixir.relationships.ManyToOne]
            #onetomanys = [f for f in c._descriptor.relationships
            #                if f.__class__ == elixir.relationships.OneToMany]
            #onetoones = [f for f in c._descriptor.relationships
            #                if f.__class__ == elixir.relationships.OneToOne]
            #manytomanys = [f for f in c._descriptor.relationships
            #                if f.__class__ == elixir.relationships.ManyToMany]

            # SQLAlchemy makes this too hard to work out the exact relations. Just put everything as manytoones
            manytoones = [f.target for f in c.__mapper__._init_properties.itervalues()
                            if f.__class__ == sa.orm.properties.RelationProperty]
            onetomanys = []
            onetoones = []
            manytomanys = []

            inheritsfrom = [bc for bc in c.__bases__ if bc != Base]
            fields = [f for f in c.__dict__.values() 
                            if f.__class__ == InstrumentedAttribute]
            fieldstr = '<tr><td align="left">' + \
                            '</td></tr><tr><td align="left">'.join(
                             ["+%s"%(f.key) for f in fields]) + '</td></tr>\n'
            relstr = ''.join(
                ['<tr class="relstr">' + \
                 '<td align="left" port="%s">%s</td></tr>\n' % \
                    (f.name, f.name) 
                        for f in manytoones + onetomanys + \
                                 onetoones + manytomanys])
            if relstr == '':
                relstr = '<tr class="relstr"><td></td></tr>'
            op += '%s [label=< \
<table border="0" cellborder="1" cellspacing="0" cellpadding="0"> \
<tr cellborder="1" cellspacing="0" cellpadding="0" border="1"> \
<td border="1" bgcolor="lightblue"><font face="Courier">%s</font></td></tr> \
<tr><td> <table border="0" cellborder="0" >%s</table> </td></tr> \
<tr><td> <table border="0" cellborder="0" >%s</table> </td></tr> \
</table>>];\n' % (c.__tablename__, c.__tablename__, fieldstr, relstr)
            
            for c2 in manytoones:
                op += '%s : %s -> %s [headlabel="%s" taillabel="%s"]\n'% \
                                (c.__tablename__, c2.name ,  c2.name, '', '') # TODO: add '*', '1'
            for c2 in onetomanys:
                op += '%s : %s -> %s [headlabel="%s" taillabel="%s"]\n' % \
                                (c.__tablename__, c2.name ,  c2.name, '*', '1')
            for c2 in onetoones:
                op += '%s : %s -> %s [headlabel="%s" taillabel="%s"]\n' % \
                                (c.__tablename__, c2.name ,  c2.name, '1', '1')
            for c2 in manytomanys:
                op += '%s : %s -> %s [headlabel="%s" taillabel="%s"]\n'% \
                                (c.__tablename__, c2.name ,  c2.name, '*', '*')
            for c2 in inheritsfrom:
                op += '%s -> %s [headlabel="%s" taillabel="%s"]\n' % \
                                (c.__tablename__, c2.name, '1', '1')
        op += '}\n'
        # Render dot graph with /usr/bin/dot or return it directly
        if format == 'dot':
            response.headers['Content-Type'] = 'text/plain'
            return op
        else:
            import os
            import tempfile
            import commands
            f1, fn = tempfile.mkstemp(suffix='.dot')
            open(fn,'w').write(op)
            data = commands.getoutput('dot -Gratio="0.65" -T%s %s' % (format, fn))
            os.unlink(fn)
            response.headers['Content-Type'] = \
                {'png':'image/png',
                 'jpg': 'image/jpg',
                 'jpeg':'image/jpeg',
                 'svg':'image/svg+xml'
                 }[format]
            return data
