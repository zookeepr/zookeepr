<%namespace name="toolbox" file="/leftcol/toolbox.mako"/>
<%inherit file="/base.mako" />

<h2>Not Allowed</h2>

<p>Unfortunately the function you are trying to perform is not allowed at this time.</p>

<%def name="title()">
Not Allowed - ${ parent.title() }
</%def>
