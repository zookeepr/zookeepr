<%inherit file="/base.mako" />

<script language="Javascript">
<!--
function toggleDiv(id,flagit) {
    if (flagit=="1"){
        if (document.layers) document.layers[''+id+''].visibility = "show"
        else if (document.all) document.all[''+id+''].style.visibility = "visible"
        else if (document.getElementById) document.getElementById(''+id+'').style.visibility = "visible"
    }
    else
        if (flagit=="0"){
            if (document.layers) document.layers[''+id+''].visibility = "hide"
            else if (document.all) document.all[''+id+''].style.visibility = "hidden"
            else if (document.getElementById) document.getElementById(''+id+'').style.visibility = "hidden"
        }
}
//-->
</script>
<style type="text/css">
.commentdiv {
    background-color:#F9F9F9;
    border:1px dashed Blue;
    padding:4px;
    position:absolute;
    visibility:hidden;
    width:200px;
    font-family:Verdana,Arial,Helvetica,san-serif;
    font-size:8pt;
}

.biodiv {
    background-color:#F9F9F9;
    border:1px dashed Blue;
    padding:4px;
    position:absolute;
    visibility:hidden;
    width:500px;
    font-family:Verdana,Arial,Helvetica,san-serif;
    font-size:8pt;
}

</style>


<h2>Application Funding Review Summary</h2>


<p>
<ul>
<li>Mouse over reviewers name for their comments
<li>Mouse over scores for score from each reviewer
</ul>


<% import re %>
% for ft in c.funding_types:
    <% collection = getattr(c, '%s_collection' % ft.name) %>
    <% i = 1 %>

    <% simple_title = re.compile('([^a-zA-Z0-9])').sub('', ft.name) %>

<a name="${ simple_title }"></a>
<h2>${ ft.name }s </h2>

<table>
<tr>
<th>&nbsp;</th>
<th>#</th>
<th>Submitter</th>
<th>Avg Score</th>
<th>Reviewers</th>
</tr>

% for funding in collection:
%    if not funding.reviews:
        <% continue %>
%    endif

<tr class="${ h.cycle('even', 'odd') }">

<td>${ i }</td>
<% i = i + 1 %>


<td>
${ h.link_to("%s (view)" % funding.id, url=h.url_for(controller='funding', action='review', id=funding.id)) }
</td>




<td>
${ h.link_to(funding.person.fullname, url=h.url_for(controller='person', action='view', id=funding.person.id)) }
</td>

<%
        total_score = 0
        num_reviewers = 0
        scores = ""
        for review in funding.reviews:
            if review.score is not None:
                num_reviewers += 1
                total_score += review.score
                scores += review.reviewer.fullname + ": %s " % review.score + "<br>"
            else:
                scores += review.reviewer.fullname + ": Abstain<br>"

        if num_reviewers == 0:
            avg_score = "No Reviews"
        else:
            avg_score = total_score*1.0/num_reviewers
%>
<td>
<div onMouseOver="toggleDiv('${ "score%s" % funding.id | h}',1)" onMouseOut="toggleDiv('${ "score%s" % funding.id | h}',0)">
${ avg_score |h }
</div>
<div id="${ "score%s" % funding.id | h}" class="commentdiv">${ scores | n}</div>

</td>




<td>
%       for review in funding.reviews:
<!--
link_to doesn't let us pass javascript tags
-->
%           if review.comment:
<a href="/funding_review/${review.id}" onMouseOver="toggleDiv('${ "%s%s" % (review.id, review.reviewer.id) | h}',1)" onMouseOut="toggleDiv('${ "%s%s" % (review.id, review.reviewer.id) | h}',0)">${ review.reviewer.fullname | h}</a>, 
<div id="${ "%s%s" % (review.id, review.reviewer.id) | h}" class="commentdiv">${ review.reviewer.fullname + ": " + review.comment |h}</div>
%           else:
${ h.link_to(review.reviewer.fullname, url=h.url_for(controller='funding_review', action='view', id=review.id)) }, 
%           endif
%       endfor
</td>

</tr>

%   endfor
</table>
% endfor #funding_types


<%def name="title()" >
Funding Application Reviews - ${ parent.title() }
</%def>

<%def name="contents()">
<%
  menu = ''

  import re

  for ft in c.funding_types:
    simple_title = re.compile('([^a-zA-Z0-9])').sub('', ft.name)
    menu += '<li><a href="#' + simple_title + '">' + ft.name + ' reviews</a></li>'
  return menu
%>
</%def>

