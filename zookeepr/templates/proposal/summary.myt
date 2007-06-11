
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
    left:450px;
    padding:4px;
    position:absolute;
    top:250px;
    visibility:hidden;
    width:200px;
    font-family:Verdana,Arial,Helvetica,san-serif;
    font-size:8pt;
}

.biodiv {
    background-color:#F9F9F9;
    border:1px dashed Blue;
    left:450px;
    padding:4px;
    position:absolute;
    top:250px;
    visibility:hidden;
    width:400px;
    font-family:Verdana,Arial,Helvetica,san-serif;
    font-size:8pt;

</style>


<h2>Review Summary</h2>

<p>
<ul>
<li>Mouse over reviewers name for their comments
<li>Mouse over scores for score from each reviewer
<li>Mouse over reviewer name for Bio and Experience
<li>Mouse over stream for Stream Stats
</ul>

% for pt in c.proposal_types:
% 	collection = getattr(c, '%s_collection' % pt.name)

<h2><% pt.name %>s (<% len(collection) %>)</h2>

<table>
<tr>
<th>#</th>
<th>Proposal</th>
<th>Submitters</th>
<th>Avg Score</th>
<th>Reviewers</th>
<th>Winning Stream</th>
</tr>

% 	for proposal in collection:
<tr class="<% h.cycle('even', 'odd') %>">

<td>
<% h.link_to(proposal.id, url=h.url(controller='proposal', action='view', id=proposal.id)) %>
</td>

<td>
<% h.link_to(proposal.title, url=h.url(controller='proposal', action='view', id=proposal.id)) %>
</td>

<td>
% 		for person in proposal.people:
<div onMouseOver="toggleDiv('<% "bio%s" % person.id | h%>',1)" onMouseOut="toggleDiv('<% "bio%s" % person.id | h%>',0)">
<% person.firstname %>
<% person.lastname %>, 
</div>
<div id="<% "bio%s" % person.id | h%>" class="biodiv"><% person.firstname + " " + person.lastname |h%><br><strong>Bio:</strong><p><% person.bio |h %></p><strong>Experience:</strong><p> <%person.experience |h%></p></div>
% 		#endfor
</td>


% 		streams = {}
% 		total_score = 0
% 		num_reviewers = 0
% 		scores = ""
% 		for review in proposal.reviews:
% 			num_reviewers += 1
% 			total_score += review.score
% 			scores += review.reviewer.handle + ": %s " % review.score
% 			if review.stream.name in streams:
% 				streams[review.stream.name] += 1
% 			else:
% 				streams[review.stream.name] = 1
% 			# endif
% 		# endfor
% 		avg_score = total_score/num_reviewers
<td>
<div onMouseOver="toggleDiv('<% "score%s" % review.id | h%>',1)" onMouseOut="toggleDiv('<% "score%s" % review.id | h%>',0)">
<% avg_score |h %>
</div>
<div id="<% "score%s" % review.id | h%>" class="commentdiv"><% scores %></div>

</td>




<td>
% 		for review in proposal.reviews:
<!--
link_to doesn't let us pass javascript tags
-->
% 			if review.comment:
<a href="/review/<%review.id%>" onMouseOver="toggleDiv('<% "%s%s" % (review.id, review.reviewer.handle) | h%>',1)" onMouseOut="toggleDiv('<% "%s%s" % (review.id, review.reviewer.handle) | h%>',0)"><% review.reviewer.handle | h%></a>
<div id="<% "%s%s" % (review.id, review.reviewer.handle) | h%>" class="commentdiv"><% review.reviewer.handle + ": " + review.comment |h%></div>
% 			else:
<% h.link_to(review.reviewer.handle, url=h.url(controller='review', action='view', id=review.id)) %>
% 			#endif
% 		# endfor
</td>

% 		stream = ""
% 		stream_stats = ""
% 		stream_score = 0
% 		for s in streams:
% 			stream_stats += s + ": %s<br>" % streams[s]
% 			if streams[s] > stream_score:
% 				stream = s
% 				stream_score = streams[s]
% 			# endif
% 		#endfor

<td>
<div onMouseOver="toggleDiv('<% "stream%s" % review.id | h%>',1)" onMouseOut="toggleDiv('<% "stream%s" % review.id | h%>',0)">
<% stream %> (<% stream_score %>)
</div>
<div id="<% "stream%s" % review.id | h%>" class="biodiv"><% stream_stats %></div>
</td>

</tr>

% 	#endfor
</table>
% # endfor proposal_tyes


<%method title>
Reviews - <& PARENT:title &>
</%method>
