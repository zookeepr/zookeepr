from formencode import htmlfill

def fill(m, defaults, errors):
    """Fill a form template with the defaults and errors from a validator."""
    def paragrify(error):
        return '<error>'+htmlfill.escape_formatter(error)+'</error>'
    form = m.content()
    form = htmlfill.render(form, defaults, errors,
                                            auto_error_formatter=paragrify)
    if form.startswith('<!--'):
        form=form.replace('<error>', '<p class="error-message">', 1)
        form=form.replace('</error>', '</p>', 1)
    form=form.replace('<error>', '<span class="error-message">')
    form=form.replace('</error>', '</span><br>')
    m.write(form)
