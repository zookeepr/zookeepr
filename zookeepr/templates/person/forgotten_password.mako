<%inherit file="/base.mako" />
<form method="post" action="${ h.url_for() }" >
        <h3>Forgotten password?</h3>
        <p>
            Enter your email address and an email will be sent to you allowing you to
            select a new password.
        </p>
        <div class="centre">
            <p class="label"><span class="mandatory">*</span>Email address:</p>
            <p class="entries">${ h.text('email_address', size=60) }</p>
            <p class="submit">${ h.submit('submit', 'Set a new password') }</p>
        </div>
</form>

