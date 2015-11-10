<div id="funding">

<p class="submitted">
Funding request for a
${ c.funding.type.name } 
submitted by
${ c.funding.person.fullname }
&lt;${ c.funding.person.email_address }&gt;
at
${ c.funding.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") | n}<br />
(last updated at ${ c.funding.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") | n})

%   if h.url_for().endswith('review') is True and ('funding_reviewer' in [x.name for x in c.signed_in_person.roles]) or ('organiser' in [x.name for x in c.signed_in_person.roles]):
<p class="submitted">
${ c.funding.person.fullname } &lt;${ c.funding.person.email_address }&gt;
%if c.funding.person.url and len(c.funding.person.url) > 0:
<a href="${ c.funding.person.url}">Submitters Homepage</a>
%endif
<br>
${ h.link_to('(view details)', url=h.url_for(controller='person', action='view', id=c.funding.person.id)) }
${ h.link_to('(stalk on Google)', url='http://google.com/search?q=%s+%s' % (c.funding.person.fullname, c.funding.person.email_address)) }
${ h.link_to('(linux specific stalk)', url='http://google.com/linux?q=%s+%s' % (c.funding.person.fullname, c.funding.person.email_address)) }
${ h.link_to('(email address only stalk)', url='http://google.com/search?q=%s' % c.funding.person.email_address) }
</p>
%   endif

</p>

<h2>Funding Programme</h2>

<em>What funding programme are you applying for?</em>
<p><blockquote>${ c.funding.type.name }</blockquote></p>

<em>In what way to you enhance the diversity of the Open Source community?</em>
<p>
<blockquote>
${ h.line_break(h.util.html_escape(c.funding.diverse_groups)) | n}
</blockquote></p>

<em>How do you contribute to the Open Source community?</em>
<p><blockquote>
${ h.line_break(h.util.html_escape(c.funding.how_contribute)) | n}
</blockquote></p>

<em>What assistance would you need to be able to attend the conference?</em>
<p><blockquote>
${ h.line_break(h.util.html_escape(c.funding.financial_circumstances)) | n}
</blockquote></p>

<em>Any other supporting information?</em>
<p><blockquote>
${ h.line_break(h.util.html_escape(c.funding.supporting_information)) | n}
</blockquote></p>

<em>Why would you like to attend linux.conf.au 2016?</em>
<p><blockquote>
${ h.line_break(h.util.html_escape(c.funding.why_attend)) | n}
</blockquote></p>

<em>Have you attended linux.conf.au before?</em>
<p class="entries">
<table>
  <tr>
    <td>
% for (year, desc) in h.lca_rego['past_confs']:
${ h.yesno(year in (c.funding.prevlca or [])) |n }
${ desc }<br />
% endfor
    </td>
  </tr>
</table>
</p>

<h2>References</h2>

<p class="label">Attachments:</p>

% if len(c.funding.attachments) > 0:
<table>
<tr>
<th>Filename</th>
<th>Size</th>
<th>Date uploaded</th>
<th>&nbsp;</th>
</tr>

%   for a in c.funding.attachments:
<tr class="${ h.cycle('even', 'odd') }">

<td>
${ h.link_to(h.util.html_escape(a.filename), url=h.url_for(controller='funding_attachment', action='view', id=a.id)) }
</td>

<td>
${ len(a.content)/1024/1024 }MB
</td>

<td>
${ a.creation_timestamp.strftime("%Y-%m-%d %H:%M") }
</td>

<td>
${ h.link_to('delete', url=h.url_for(controller='funding_attachment', action='delete', id=a.id)) }
</tr>
%   endfor

</table>
% else:
<table>
  <tr><td>No attachments</td></tr>
</table>
% endif
% if c.signed_in_person == c.funding.person or h.auth.authorized(h.auth.has_organiser_role):
<p>
${ h.link_to('Add an attachment', url=h.url_for(action='attach')) }
</p>
% endif
</div>

<%def name="title()">
${ c.funding.type.name } Application - ${ c.funding.person.firstname } ${ c.funding.person.lastname } - ${ parent.title() }
</%def>
