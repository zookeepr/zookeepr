<%inherit file="/base.mako" />
<h2>
Thanks for confirming your account!
</h2>

<p>
You can now ${ h.link_to('sign in', url=h.url_for(controller='/person', action='signin')) } to your account.
</p>

<p>
Don't forget to sign up to the <a href="http://lists.linux.org.au/listinfo/lca-announce">lca-announce@linux.org.au</a> and <a href="http://lists.lca2010.org.nz/mailman/listinfo/lca2010-chat.lca2010.org.nz">lca2010-chat@lists.lca2010.org.nz</a> mailing list!
</p>
