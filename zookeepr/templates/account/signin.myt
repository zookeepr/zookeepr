<h2>Sign in!</h2>

#<p>Don't have an account? <% h.link_to('Sign up', url=h.url(controller='person', action='new')) %> now!</p>

<% h.form(h.url_for(controller='/account', action='signin')) %>

<% h.text_field('email_address') %>
<% h.password_field('password') %>

<% h.submit('Sign in') %>

<% h.end_form() %>

<%method title>
Sign in! - <& PARENT:title &>
</%method>
