<talks>
% for t in c.talks:
  <talk id="${ t.id }">
    <title>${ t.title |h}</title>
<%   speakers = [(s.lastname.lower(), s.firstname.lower(), s) for s in t.people] %>
<%   speakers.sort() %>
    <speaker id="${ s.id }">${ s.firstname |h} ${ s.lastname |h}</speaker>
%   endfor
    <video>${ release_yesno(s.video_release) }</video>
    <slides>${ release_yesno(s.slides_release) }</slides>
%   if t.scheduled:
    <scheduled>
      <code>${ t.code }</code>
      <time>
        <date>${ t.scheduled.strftime('%Y-%m-%d') |h}</date>
        <dow></dow> <!-- FIXME: Probably want to add times back into here if you have them. 09 Did not store time information to save hassle -->
        <start></start>
        <end></end>
      </time>
      <venue>
        <building>${ t.building |h}</building>
        <theatre>${ t.theatre |h}</theatre>
      </venue>
    </scheduled>
%   elif t.id>=500:
    <scheduled>
      <time>
        <dow>${ {5: 'Sun', 6: 'Mon', 7: 'Tue', 8: 'Wed'}[t.id / 100] |h}</dow>
      </time>
    </scheduled>
%   endif
  </talk>
% endfor
</talks>
