from routes import url_for

def do_login(app, person_or_email_address, password=None):
    # Overload the function to allow just throwing a person object
    if password is None:
        email_address = person_or_email_address.email_address
        password = person_or_email_address.raw_password
    else:
        email_address = person_or_email_address

    # Disabling cookies makes login function reentrant
    resp = app.get(url_for(controller='person', action='signin'), headers={'Cookie':''})

    f = resp.forms['signin-form']
    f['person.email_address'] = email_address
    f['person.password'] = password
    return f.submit(extra_environ=dict(REMOTE_ADDR='0.0.0.0'))

def isSignedIn(app):
    return 'authkit' in app.cookies and len(app.cookies['authkit']) > 15
