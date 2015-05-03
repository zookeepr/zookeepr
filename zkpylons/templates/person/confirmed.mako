<%inherit file="/base.mako" />
<h2>
Thanks for confirming your account!
</h2>

<p>
You can now ${ h.link_to('sign in', url=h.url_for(controller='/person', action='signin')) } to your account.
</p>

<p>
Don't forget to sign up to the <a href="${ c.config.get('mailing_list_announce_url') }">${ c.config.get('mailing_list_announce_addr') }</a> mailing list!
</p>
