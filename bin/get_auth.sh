#!/bin/sh
psql -A -P pager -F '#' -c "
SELECT 
        person.*, account.*
FROM
        person, account,registration
WHERE

        (
                registration.id IN (SELECT rego FROM rego_invoice_payment WHERE payment > 0)
                OR
                registration.id IN (SELECT id FROM speaker_rego WHERE id IS NOT NULL)
                OR
                registration.id IN (SELECT registration.id FROM registration, discount_code WHERE registration.discount_code = discount_code.code)
        )
        AND
        registration.person_id = person.id
        AND
        person.account_id = account.id
"
