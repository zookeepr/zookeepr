<%inherit file="/base.mako" />
<%namespace file="../bookmark_submit.mako" name="bookmark_submit" inheritable="True"/>

<%
  import datetime
%>

<h2>Photo Competition Entry Form</h2>

%if c.days_open < 0:
  <p>
    The competition has not opened yet.  It opens on ${ c.open_date.strftime("%A %d %B") }.
  </p>
%elif c.days_open >= c.DAYS_OPEN:
  <p>
    Entries have closed.
  </p>
%endif

${ h.form(h.url_for(controller="photocomp", action="upload"), multipart=True) }

<table summary="entries" style="padding: 10px;">
  <thead>
  <tr>
    <td style="border: none;">&nbsp;</td>
%for entry_id in range(len(c.ENTRY_NAMES)):
    <td style="text-align: center; border-left: none; border-top: none; border-right: none; padding-bottom: 10px"><b>Entry ${c.ENTRY_NAMES[entry_id]}</b></td>
%endfor
  </tr>
  <tbody>
%for day in range(c.DAYS_OPEN):
  <tr>
    <td style="padding-right: 10px; border-left: none; border-top: none; border-bottom: none; vertical-align: middle">
      <b>${(c.open_date + datetime.timedelta(day)).strftime("%A")}</b>
%if c.days_open < -1:
      <br/><br/>(Not open)
%elif c.days_open > day:
      <br/><br/>(Closed)
%endif
    </td>
%for entry_id in range(len(c.ENTRY_NAMES)):
    <td style="padding: 10px;">
      <table style="height: 250px; width: 250px; border: none; margin: auto; padding: 0"><tr><td style="border: none; padding: 0;"><div style="margin: auto; text-align: center;">
%if c.photo(day, entry_id) is not None:
        <a href="/photocomp/photo/${c.photo(day, entry_id).filename('orig')}"><img src="/photocomp/photo/${c.photo(day, entry_id).filename('250x250')}" style="margin: 0;"/></a>
%else:
        <img src="/images/photocomp-noentry.png" style="margin: 0;"/>
%endif
      </div></td></tr></table>
%if c.is_organiser or c.days_open >= -1 and c.days_open <= day:
      <br/>
      <div style="text-align: right"><input type=checkbox name="${ 'delete-%d-%d' % (day, entry_id) }"/><label for="${ 'delete-%d-%d' % (day, entry_id) }" value="delete">Delete?</label></div>
      <input type=file name="${ 'photo-%d-%d' % (day, entry_id) }"/>
%endif
    </td>
%endfor
  </tr>
%endfor
%if c.days_open >= -1 and c.days_open < c.DAYS_OPEN:
  <tr>
    <td style="border: none;">&nbsp;</td>
    <td colspan=2 style="border: none; padding-top: 10px; text-align: center">
        ${ h.submit("submit", "Submit") }
    </td>
  </tr>
%endif
</table>

${ h.end_form() }

<%def name="extra_head()">
</%def>
