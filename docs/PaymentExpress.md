PaymentExpress Details
----------------------

For NZ credit card processing we utilise the DPS PxPay system

This code was originally written by Francois for LCA 2010 in Wellington
Initial backport to LCA 2015 was by Steven Ellis and Ben

Credentials
-----------
We have two sets of credentials, a primary business account and
a secondary developer account

Primary Account UserID = LinuxAust
Developer Account UserID = LinuxAU_Dev

These also require an API key


Testing
-------
For testing details reference
 - http://www.paymentexpress.com/Knowledge_Base/Frequently_Asked_Questions/Developer_FAQs#Testing%20Details

If we wish to simulate a transaction flagged for retry how should we test?
 - Using card number 4999999999999202 will result in a declined transaction and set the retry flag to "1" for interfaces that support it.

 
What other tests can I perform in addition to the ones I have tried?
 - You could try the following card numbers to simulate other common declines:
 - 4999999999999236 - ReCo 05
 - 4999999999999269 - ReCo 12
 - 5431111111111301 - ReCo 30
 - 5431111111111228 - ReCo 51

What credit card and expiry date should we be testing with?
Only pre-approved 'test card' numbers provided by DPS can be used for testing, within test environments. We recommend using the test card 
 - 4111111111111111 for Visa, 
 - 5431111111111111 for MasterCard, 
 - 371111111111114 for Amex, and 
 - 36000000000008 for Diners.

These can be used with any current expiry, and are suitable only for DPS test accounts.

DPS and payment_id_seq
----------------------

Note that the DPS field TxnId needs to be unique which causes issues with out testing.

Hence we need to set a different sequence id for payments for each of our environments

Without this change we get clashing invoices with the wrong values.

-- Sandbox Environment
ALTER SEQUENCE payment_id_seq RESTART WITH 5100000;
-- DEV Environment
ALTER SEQUENCE payment_id_seq RESTART WITH 5200000;
-- UAT Environment
ALTER SEQUENCE payment_id_seq RESTART WITH 5300000;
-- PROD Environment
ALTER SEQUENCE payment_id_seq RESTART WITH 5400000;

