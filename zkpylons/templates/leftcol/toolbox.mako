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
      <li${cls | n}><a href="${url}"><span class="l"></span><span class="r"></span><span class="t">${title}</span></a>
</%def>


<ul class="netv-vmenu">
## Toolbox links
% if h.signed_in_person():
    <span class="menu-header">${ h.signed_in_person().firstname }'s Profile</span>
    <ul class="netv-vmenu">
${ parent.toolbox_extra() }
%   if h.lca_info["cfp_status"] == 'open' or h.auth.authorized(h.auth.has_late_submitter_role):
      ${ make_link('Submit a proposal', h.url_for(controller='proposal', action='new', id=None)) }
%   endif
%   if h.lca_info["cfmini_status"] == 'open':
      ${ make_link('Submit a miniconf', h.url_for(controller='miniconf_proposal', action='new', id=None)) }
%   endif
%   if h.lca_info["funding_status"] == 'open':
      ${ make_link('Submit a Funding Application', h.url_for(controller='funding', action='new', id=None)) }
%   endif
%   if h.lca_info['conference_status'] == 'open' or h.signed_in_person().registration:
      ${ make_link('Conference registration', '/register/status') }
%   endif
%   if h.signed_in_person().is_speaker():
      ${ make_link('Speakers Info', '/programme/presenter_faq') }
%   endif
%   if h.signed_in_person().is_miniconf_org():
      ${ make_link('Miniconf Organiser Info', '/programme/miniconf_information') }
%   endif
%   if len(h.signed_in_person().proposals) > 0:
      ${ make_link('My proposals', h.url_for(controller='proposal')) }
%   endif
      ${ make_link('My profile', h.url_for(controller='person', action='view', id=h.signed_in_person().id)) }
      ${ make_link('Sign out', h.url_for('/person/signout')) }
% else:
      ${ make_link('Sign in', "/person/signin") }
      ${ make_link('Create an account', "/person/new") }
% endif
% if h.auth.authorized(h.auth.has_organiser_role):
<span class="menu-header">Zookeepr Administration</span>
    <ul class="netv-vmenu">
      ${ make_link('Admin', h.url_for(controller='admin')) }
      ${ make_link('Lookup', h.url_for(controller='admin', action='lookup')) }
      ${ make_link('View People', h.url_for(controller='person')) }
      ${ make_link('Manage Pages', h.url_for(controller='db_content')) }
      ${ make_link('Manage Files', h.url_for('/db_content/list_files')) }
%   if c.db_content and not (h.url_for().endswith('/edit') or h.url_for().endswith('/new')):
      ${ make_link('Edit Page', h.url_for(controller='db_content', action='edit', id=c.db_content.id)) }
%   elif c.not_found:
      ${ make_link('Create page here', h.url_for(controller='db_content', action='new')) }
%   endif
${ parent.toolbox_extra_admin() }
    </ul>
% endif
% if h.auth.authorized(h.auth.has_reviewer_role):
    <span class="menu-header">Paper Reviewer</span>
    <ul class="netv-vmenu">
${ parent.toolbox_extra_reviewer() }
      ${ make_link('How to review', '/help/review') }
      ${ make_link('Proposals to review', h.url_for(controller='proposal', action='review_index', id=None)) }
      ${ make_link("Reviews you've made", h.url_for(controller='review', action='index', id=None)) }
      ${ make_link('Summary of reviewed proposals', h.url_for(controller='proposal', action='summary', id=None)) }
      ${ make_link('Reviewer summary', h.url_for(controller='review', action='summary', id=None)) }
      <span class="menu-header">List of proposals by:</span>
    <ul class="netv-vmenu">
    %if h.lca_info['cfp_hide_scores'] == 'no':
        ${ make_link('number of certain score / number of reviewers', h.url_for(controller='admin', action='proposals_by_strong_rank', id=None)) }
        ${ make_link('max score, min score then average', h.url_for(controller='admin', action='proposals_by_max_rank', id=None)) }
        ${ make_link('stream and score', h.url_for(controller='admin', action='proposals_by_stream', id=None)) }
    %endif
        ${ make_link('number of reviewers', h.url_for(controller='admin', action='proposals_by_number_of_reviewers', id=None)) }
        ${ make_link('submission date', h.url_for(controller='admin', action='proposals_by_date', id=None)) }
      </ul>
    </ul>
% endif
% if h.auth.authorized(h.auth.has_funding_reviewer_role):
    <span class="menu-header">Funding Reviewer</span>
    <ul class="netv-vmenu">
${ parent.toolbox_extra_funding_reviewer() }
      ${ make_link('How to review', '/help/funding_review') }
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
% if (c.db_content and not c.db_content.is_news()) or len(parent.short_title()) > 0:
<div style="text-align:center;">
</div>
% endif
% if h.signed_in_person():
    <p style="font-style: italic; padding-left: 7px;">${h.signed_in_person().email_address}</p>
% endif
</ul>
