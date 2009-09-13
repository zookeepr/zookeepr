function toggle_select_hidden(select, field) {
  if ( document.getElementById(select).value == 'other' ) {
    document.getElementById(field).style.display = 'inline';
  } else {
    document.getElementById(field).style.display = 'none';
  }
}
