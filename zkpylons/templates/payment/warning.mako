Subject: Payment error: ${ subject }
To: ${ c.config.get('contact_email') }
From: payment error <${ c.config.get('contact_email') }>

Something went horribly wrong whilst someone was trying to pay!

The error from the code is: ${ subject }

The PaymentReceived object looks like this:

${ pr }

Please look at it! People get iffy about payments!

Yours,

Some Robot.
