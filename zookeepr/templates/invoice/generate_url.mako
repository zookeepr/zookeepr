<%inherit file="/base.mako" />
<h2>URL Hash for ${ c.id }</h2>

<blockquote><p>${ h.lca_info['event_url'] + h.url_for(action='view') + "?hash=" + c.hash.url_hash }</p></blockquote>

<p>This is a unique URL that you can give to your accountant to pay the invoice.</p>
