<%inherit file="/base.mako" />

<h1>Funding Review ${ c.review.id }</h1>

<h2>#${ c.review.funding.id } - ${ c.review.funding.person.fullname() } - ${ c.review.funding.type.name }</h2>

<p>
<b>Review by:</b> ${ c.review.reviewer.fullname() }
</p>

<br />
<p><b>Score:</b> ${ c.review.score | h }</p>

<p><b>Reviewer Comment:</b></p>
<blockquote>
<p>${ c.review.comment | h}</p>
</blockquote>

${ h.link_to('Edit', url=h.url_for(action='edit')) } - ${ h.link_to('Delete', url=h.url_for(action='delete')) }

