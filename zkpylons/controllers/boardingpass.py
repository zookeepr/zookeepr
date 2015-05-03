import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.pdfgen import wrap_pdf_response
from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema
import zkpylons.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import Role

from reportlab.lib.units import mm
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart
from io import BytesIO
from reportlab.pdfgen import canvas



log = logging.getLogger(__name__)


class BoardingpassController(BaseController): 

    def pdf(self, id):

        
        buffer = BytesIO()

        # Create the PDF object, using the BytesIO object as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.drawString(100, 800, "Hello world.")
        
        
        
        barcode = createBarcodeDrawing('Code128', value=id,  barHeight=10*mm, humanReadable=True)
        barcode.drawOn(p, 100, 700)

        # Close the PDF object cleanly.
        p.showPage()
        p.save()

        # Get the value of the BytesIO buffer and write it to the response.
        pdf_data = buffer.getvalue()
        buffer.close()
        
        return wrap_pdf_response(pdf_data, "boarding_pass.pdf")
