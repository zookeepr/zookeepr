<%inherit file="/base.mako" />
<p>
Your password has been updated!
</p>

<p>
Now you can ${ h.link_to('sign in', url=h.url_for(controller='/person',action='signin')) } to your account.
</p>
