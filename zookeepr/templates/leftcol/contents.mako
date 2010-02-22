<%page args="parent" />
% if parent.contents() != '':
  <div class="yellowbox">
    <div class="boxheader">
      <h1>Contents</h1>
      <ul>
${ parent.contents() | n }
      </ul>
    </div>
  </div>
% endif
