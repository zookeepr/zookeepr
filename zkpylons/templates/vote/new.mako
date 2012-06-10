<%inherit file="/base.mako" />

<h2>Vote for your favourite event(s)</h2>
<style>
.votecard {
width: 150px; 
height: 180px;
float: left;
border: 1px solid #777; 
margin: 5px;
padding: 0px;
-moz-border-radius: 4px;
-webkit-border-radius: 4px;
border-radius: 4px; /* future proofing */
-khtml-border-radius: 4px; /* for old Konqueror browsers */
text-align: center;
          }
.votecard h4 {
background-color: #3D91D6;
color: #fff;
padding-top: 1px; 
margin-top: 5px;
margin-bottom: 5px;
font-weight: bold;
font-size: 10pt;
}

.votecard a {
font-weight: bold;
font-size: 10pt;
color: #fff;
background-color: #3D91D6;
padding-left: 15px;
padding-right: 15px;
text-decoration: none;
-moz-border-radius: 4px;
-webkit-border-radius: 4px;
border-radius: 4px; /* future proofing */
-khtml-border-radius: 4px; /* for old Konqueror browsers */
text-align: center;
border: 1px solid #444;
}

.votecard a:hover { background-color: #FFFF44; color: #3D91D6;}

.votecard p {
height: 100px;
line-height: 1.0;
font-size: 10pt;
font-weight: bold;
padding: 2px;
}

.Mon {background-color: #AAD4FF;}
.Tue {background-color: #CCE6FF;}
.Wed {background-color: #AAD4FF;}
.Thu {background-color: #CCE6FF;}
.Fri {background-color: #AAD4FF;}
</style>
<% count = 4 %>
% for vot in c.votes:
<% count = count -1 %>
%   for i in c.events:
%     if int(i.id) == int(vot.event_id):
  <div class="votecard">
  <h4>VOTE CAST</h4>
  <p>You have cast one of your votes for:<br/> <br/>${i.computed_title()} (${i.computed_speakers()[0]})</p>
 <a href="/vote/new?eventid=${i.id}&revoke=1" >REVOKE VOTE</a>
  </div>
%     endif
%   endfor

% endfor

<br clear="all"/>



<p>Vote for your favourite presentations here. You can vote for the same presentation more than once, and can cast up to four (4) votes. Presentations are listed below in chronological order.</p>
<p><b>You have ${count} votes remaining.${c.registration}</b></p>
% for t in c.time_slot:
%   for s in c.schedule:
%     if s.time_slot_id == t.id:
%       for i in c.events:
%         if i.id == s.event_id and i.type_id == 3 and i.computed_title() not in ['Keynote 1','Keynote 2','Sysadmin Miniconf','Best Of #1','Best Of #2','Best Of #3','Best Of #4']:
   <div class="votecard ${t.start_time.strftime("%a")}"><h4>${t.start_time.strftime("%a %I:%M%p")}</h4>
          <p> ${i.computed_title()} (${i.computed_speakers()[0]}) </p>
%         if count > 0:
    <a href="/vote/new?eventid=${i.id}" >VOTE</a>
%         endif
   </div>
%         endif
%       endfor
%     endif
%   endfor
% endfor
<%def name="title()">
Vote - ${ parent.title() }
</%def>
