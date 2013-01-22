
import os
import tempfile

from lxml import etree
from pylons.controllers.util import Response, redirect



def generate_pdf(xml_s, xsl_f):
    '''given xml as a string and a path to xsl style sheet, create a pdf file
    and return the data. '''

    styledoc = etree.parse(xsl_f)
    transform = etree.XSLT(styledoc)
    doc = etree.fromstring(xml_s)
    result = transform(doc)

    (svg_fd, svg_path) = tempfile.mkstemp('.svg')
    os.write(svg_fd, result)
    os.close(svg_fd)

    (pdf_fd, pdf_path) = tempfile.mkstemp('.pdf')
    os.close(pdf_fd)

    os.system('inkscape -z -f %s -A %s' % (svg_path, pdf_path))
    #os.system('/Applications/Inkscape.app/Contents/Resources/bin/inkscape -z -f %s -A %s' % (svg_path, pdf_path))
    #os.system('svg2pdf %s %s'%(svg_path, pdf_path)) # segmentation fault on osx
    #os.system('rsvg-convert -f pdf -o %s %s'%(pdf_path, svg_path))  # black boxes everywhere

    pdf_f = file(pdf_path)
    pdf_data = pdf_f.read()
    pdf_f.close()

    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    if os.path.exists(svg_path):
        os.remove(svg_path)

    return pdf_data


def wrap_pdf_response(pdf_data, filename):
    '''given pdf data, wrap and create a reponse '''

    res = Response(pdf_data)
    res.headers['Content-type']='application/pdf'
    #res.headers['Content-type']='application/octet-stream'
    #res.headers['Content-type']='text/plain; charset=utf-8'
    res.headers['Content-Disposition']=( 'attachment; filename=%s' % filename )

    return res
