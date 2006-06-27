from formencode import htmlfill

def fill(m, defaults, errors):
    """Fill a form template with the defaults and errors from a validator."""
    form = m.content()
    m.write(htmlfill.render(form, defaults, errors))
