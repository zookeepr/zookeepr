<%inherit file="/base.mako" />

<p>${ c.text | n}</p>

${ h.form(h.url_for()) }
<p>Type:<br />
<select id="type" name="type">
    <option value="all">All</option>
    <option value="concession">Concession/Student</option>
    <option value="hobby">Hobbyist</option>
    <option value="professional">Professional/Fairy Penguin</option>
    <option value="speaker">Speaker</option>
    <option value="mc_organiser">miniconf Organiser</option>
    <option value="volunteer">Volunteer</option>
    <option value="press">Press</option>
    <option value="organiser">Organiser</option>
    <option value="monday_tuesday">Monday+Tuesday only</option>
</select></p>

<p><i>Or</i> Registration ID (one per line):<br>
<textarea id="reg_id" name="reg_id"></textarea></p>

<p><label for="stamp">Include Stamp? <input type="checkbox" value="1" id="stamp" name="stamp" /></label> (recommended for All)</p>

<p class="submit">${ h.submit('submit', 'Generate') }</p>
${ h.end_form() }
