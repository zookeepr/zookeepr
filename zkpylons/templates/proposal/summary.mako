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


<h2>Review Summary</h2>


<p>
  <ul>
    <li>Mouse over reviewers name for their comments
    <li>Mouse over scores for score from each reviewer
    <li>Mouse over reviewer name for Bio and Experience
    <li>Mouse over stream for Stream Stats
  </ul>
</p>


%for proposal_type in c.proposal_types:

  <a name="${ proposal_type.name }"></a>
  <h2>${ proposal_type.name }s </h2>

  <table id="${ proposal_type.name }">
    <tr>
      <th>#</th>
      <th>Proposal</th>
      <th>Submitters</th>
      <th>Avg Score</th>
      <th>Reviewers</th>
      <th>Winning Stream</th>
    </tr>

%   for result in c.proposal[proposal_type]:
<%    proposal = result.Proposal %>

    <tr class="${ h.cycle('even', 'odd') }">
      <td>
        <div onMouseOver="toggleDiv('${ "assistance%s" % proposal.id | h}',1)" onMouseOut="toggleDiv('${ "assistance%s" % proposal.id | h}',0)">
          ${ h.link_to(proposal.id, url=h.url_for(controller='proposal', action='review', id=proposal.id)) }
        </div>
      </td>
      <td>
        <div onMouseOver="toggleDiv('${ "proposal%s" % proposal.id | h}',1)" onMouseOut="toggleDiv('${ "proposal%s" % proposal.id | h}',0)">
          ${ h.link_to(proposal.title, url=h.url_for(controller='proposal', action='review', id=proposal.id)) }
        </div>
        <div id="${ "proposal%s" % proposal.id }" class="biodiv"><strong>Abstract:</strong><p>${ h.line_break(proposal.abstract) |n }</p></pre></div>
      </td>
      <td>
%     for person in proposal.people:
        <div onMouseOver="toggleDiv('${ "bio%s" % person.id | h}',1)" onMouseOut="toggleDiv('${ "bio%s" % person.id | h}',0)">
          ${ person.fullname }, 
        </div>
        <div id="${ "bio%s" % person.id | h}" class="biodiv">${ person.firstname + " " + person.lastname |h}<br><strong>Bio:</strong><p>${ person.bio |h }</p><strong>Experience:</strong><p> ${person.experience |h}</p></div>
%     endfor
      </td>
      <td>
        <div onMouseOver="toggleDiv('${ "score%s" % proposal.id | h}',1)" onMouseOut="toggleDiv('${ "score%s" % proposal.id | h}',0)">
%     if result.average is None:
          <b>No Reviews</b>
%     else:
          ${ "%0.2f" % result.average | h }
%     endif
        </div>
        <div id="${ "score%s" % proposal.id | h}" class="commentdiv">
%     for review in proposal.reviews:
          ${ review.reviewer.fullname }:  ${ review.score }<br />
%     endfor
        </div>
      </td>
      <td>
%     for review in proposal.reviews:
%       if review.comment or review.private_comment:
      <!--
      link_to doesn't let us pass javascript tags
      -->
        <a href="${ h.url_for(controller='review', action='view', id=review.id) }" onMouseOver="toggleDiv('${ "%s%s" % (review.id, review.reviewer.id) |h}',1)" onMouseOut="toggleDiv('${ "%s%s" % (review.id, review.reviewer.id) | h}',0)">${ review.reviewer.fullname | h}</a>, 
        <div id="${ "%s%s" % (review.id, review.reviewer.id) | h}" class="commentdiv">
          <b>${ review.reviewer.fullname |h } Comments:</b> ${ review.comment |h }<br />
          <br />
          <b>${ review.reviewer.fullname |h } Private Comments:</b> ${ review.private_comment |h }
        </div>
%       else:
        ${ h.link_to(review.reviewer.fullname , url=h.url_for(controller='review', action='view', id=review.id)) }, 
%       endif
%     endfor
      </td>

<%
        streams = {}
        for review in proposal.reviews:
            if review.stream is not None:
                if review.stream.name in streams:
                    streams[review.stream.name] += 1
                else:
                    streams[review.stream.name] = 1

        stream = ""
        stream_stats = ""
        stream_score = 0
        for s in streams:
            stream_stats += s + ": %s<br>" % streams[s]
            if streams[s] > stream_score:
                stream = s
                stream_score = streams[s]
            # endif
        endfor
%>

      <td>
        <div onMouseOver="toggleDiv('${ "stream%s" % proposal.id | h}',1)" onMouseOut="toggleDiv('${ "stream%s" % proposal.id | h}',0)">
          ${ stream } (${ stream_score })
        </div>
        <div id="${ "stream%s" % proposal.id | h}" class="biodiv">${ stream_stats | n}</div>
      </td>
    </tr>
%   endfor # proposals
  </table>
% endfor #proposal_types


<%def name="title()" >
Reviews - ${ parent.title() }
</%def>

<%def name="contents()">
<%
  menu = ''

  import re

  for proposal_type in c.proposal_types:
    proposal_type.name = re.compile('([^a-zA-Z0-9])').sub('', proposal_type.name)
    menu += '<li><a href="#' + proposal_type.name + '">' + proposal_type.name + ' proposals</a></li>'
  return menu
%>
</%def>
