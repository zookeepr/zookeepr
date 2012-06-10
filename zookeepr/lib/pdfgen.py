
import libxml2, libxslt
import os
import tempfile

from pylons.controllers.util import Response, redirect

def generate_pdf(xml_s, xsl_f):
    '''given xml as a string and a path to xsl style sheet, create a pdf file
    and return the data. '''

    xsl_s = libxml2.parseFile(xsl_f)
    xsl = libxslt.parseStylesheetDoc(xsl_s)

    xml = libxml2.parseDoc(xml_s)
    svg_s = xsl.applyStylesheet(xml, None)

    (svg_fd, svg) = tempfile.mkstemp('.svg')
    xsl.saveResultToFilename(svg, svg_s, 0)

    xsl.freeStylesheet()
    xml.freeDoc()
    svg_s.freeDoc()

    (pdf_fd, pdf_path) = tempfile.mkstemp('.pdf')

    os.close(svg_fd); os.close(pdf_fd)

    os.system('inkscape -z -f %s -A %s' % (svg, pdf_path))

    pdf_f = file(pdf_path)
    pdf_data = pdf_f.read()
    pdf_f.close()
    
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    return pdf_data
    

def wrap_pdf_response(pdf_data, filename):
    '''given pdf data, wrap and create a reponse '''
        
    res = Response(pdf_data)
    res.headers['Content-type']='application/pdf'
    #res.headers['Content-type']='application/octet-stream'
    #res.headers['Content-type']='text/plain; charset=utf-8'
    res.headers['Content-Disposition']=( 'attachment; filename=%s' % filename )
    
    return res