<%page args="parent" />
<%namespace file="../bookmark_submit.mako" name="bookmark_submit" inheritable="True"/>
<%
    this_url = h.url_for()
    url=h.lca_info["event_permalink"] + this_url
%>
<%def name="make_link(title, url)">
<%
      if this_url == url:
          cls=' class="selected"'
      else:
          cls=''
%>
      <li${cls | n}>${ h.link_to(title, url=url) }</li>
</%def>

  

## Toolbox links
<div class = 'yellowbox'>
  <div class="boxheader">
    <h1>Toolbox</h1>
% if h.auth.authorized(h.auth.has_organiser_role):
    <h2>Organiser</h2>
    <ul>
      ${ make_link('Admin', h.url_for(controller='admin')) }
      ${ make_link('View People', h.url_for(controller='person')) }
      ${ make_link('View Pages', h.url_for(controller='db_content')) }
      ${ make_link('New Page', h.url_for(controller='db_content', action='new')) }
%   if c.db_content and not h.url_for().endswith('/edit'):
      ${ make_link('Edit Page', h.url_for(controller='db_content', action='edit', id=c.db_content.id)) }
%   endif
${ parent.toolbox_extra_admin() }
    </ul>
% endif
% if h.auth.authorized(h.auth.has_reviewer_role):
    <h2>Paper Reviewer</h2>
    <ul>
${ parent.toolbox_extra_reviewer() }
      ${ make_link('How to review', '/help/review') }
      ${ make_link('Proposals to review', h.url_for(controller='proposal', action='review_index')) }
      ${ make_link("Reviews you've made", h.url_for(controller='review', action='index')) }
      ${ make_link('Summary of reviewed proposals', h.url_for(controller='proposal', action='summary')) }
      ${ make_link('Reviewer summary', h.url_for(controller='review', action='summary')) }
      <li>List of proposals by:</li>
      <ul class="indent">
        ${ make_link('number of certain score / number of reviewers', h.url_for(controller='admin', action='proposals_by_strong_rank')) }
        ${ make_link('max score, min score then average', h.url_for(controller='admin', action='proposals_by_max_rank')) }
        ${ make_link('stream and score', h.url_for(controller='admin', action='proposals_by_stream')) }
      </ul>
    </ul>
% endif
% if h.auth.authorized(h.auth.has_funding_reviewer_role):
    <h2>Funding Reviewer</h2>
    <ul>
${ parent.toolbox_extra_funding_reviewer() }
      ${ make_link('Proposals to review', h.url_for(controller='funding', action='review_index')) }
      ${ make_link("Reviews you've made", h.url_for(controller='funding_review', action='index')) }
      ${ make_link('Summary of reviewed proposals', h.url_for(controller='funding', action='summary')) }
      ${ make_link('Reviewer summary', h.url_for(controller='funding_review', action='summary')) } 
      <li>List of requests by:</li>
      <ul class="indent">
        ${ make_link('number of certain score / number of reviewers', h.url_for(controller='admin', action='funding_requests_by_strong_rank')) }
        ${ make_link('max score, min score then average', h.url_for(controller='admin', action='funding_requests_by_max_rank')) }
      </ul>
    </ul>
% endif
% if h.signed_in_person():
    <h2>${ h.signed_in_person().firstname }</h2>
    <ul>
${ parent.toolbox_extra() }
%   if h.lca_info["cfp_status"] == 'open' or h.auth.authorized(h.auth.has_late_submitter_role):
      ${ make_link('Submit a paper', h.url_for(controller='proposal', action='new', id=None)) }
%   endif
%   if h.lca_info["cfmini_status"] == 'open':
      ${ make_link('Submit a miniconf', h.url_for(controller='miniconf_proposal', action='new', id=None)) }
%   endif
%   if h.lca_info["funding_status"] == 'open':
      ${ make_link('Submit a Funding Application', h.url_for(controller='funding', action='new', id=None)) }
%   endif
%   if h.lca_info['conference_status'] == 'open' or h.signed_in_person().registration:
      ${ make_link('Conference registration', h.url_for(controller='registration', action='status')) }
%   endif
%   if len(h.signed_in_person().proposals) > 0:
      ${ make_link('My proposals', h.url_for(controller='proposal')) }
%   endif
      ${ make_link('My profile', h.url_for(controller='person', action='view', id=h.signed_in_person().id)) }
      ${ make_link('Sign out', h.url_for(controller='person', action='signout')) }
% else:
    <ul>
      ${ make_link('Sign in', "/person/signin") }
      ${ make_link('Register', "/person/new") }
% endif
    </ul>
% if (c.db_content and not c.db_content.is_news()) or len(parent.short_title()) > 0:
<div style="text-align:center;">
%   if c.db_content:
${ bookmark_submit.bookmark_submit(url, c.db_content.title) }
%   else:
${ bookmark_submit.bookmark_submit(url, parent.short_title()) }
%   endif
</div>
% endif
% if h.signed_in_person():
    <p class = 'more'>${h.signed_in_person().email_address}</p>
% endif
  </div>
</div>
