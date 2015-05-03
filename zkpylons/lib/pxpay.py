import urllib2
from xml.dom import minidom
from zkpylons.model.config import Config

pxpay_url = 'https://www.paymentexpress.com/pxpay/pxaccess.aspx'
currency  = 'NZD'

def get_node_value(parent_node, node_name):
    if parent_node is None:
        return None

    node = parent_node.getElementsByTagName(node_name)
    if len(node) < 1:
        return None

    text_node = node[0].firstChild
    if text_node is None:
        return None
    
    return text_node.nodeValue

def generate_request(fields):
    xml_request = "<GenerateRequest>"
    xml_request += "<PxPayUserId>" + Config.get('paymentgateway_userid') + "</PxPayUserId>"
    xml_request += "<PxPayKey>" + Config.get('paymentgateway_secretkey') + "</PxPayKey>"
    xml_request += "<AmountInput>" + fields['amount'] + "</AmountInput>"
    xml_request += "<CurrencyInput>" + currency + "</CurrencyInput>"
    xml_request += "<MerchantReference>INV" + str(fields['invoice_id']) + "</MerchantReference>"
    xml_request += "<EmailAddress></EmailAddress>"
    xml_request += "<TxnData1>" + fields['client_ip'] + "</TxnData1>"
    xml_request += "<TxnData2>" + fields['email_address'] + "</TxnData2>"
    xml_request += "<TxnData3></TxnData3>"
    xml_request += "<TxnType>Purchase</TxnType>"
    xml_request += "<TxnId>PAY" + str(fields['payment_id']) + "</TxnId>"
    xml_request += "<EnableAddBillCard>0</EnableAddBillCard>"
    xml_request += "<UrlSuccess>" + fields['return_url'] + "</UrlSuccess>"
    xml_request += "<UrlFail>" + fields['return_url'] + "</UrlFail>"
    xml_request += "</GenerateRequest>"

    req = urllib2.Request(pxpay_url, xml_request)
    xml_response = minidom.parse(urllib2.urlopen(req))

    request_node = xml_response.getElementsByTagName("Request")[0]
    valid = request_node.getAttribute("valid")
    return valid, get_node_value(request_node, 'URI')

def process_response(fields):
    if fields['userid'] != Config.get('paymentgateway_userid'):
        return None, ['Invalid userid in redirect from payment gateway: ' + fields['userid'] ]

    xml_request = "<ProcessResponse>"
    xml_request += "<PxPayUserId>" + Config.get('paymentgateway_userid') + "</PxPayUserId>"
    xml_request += "<PxPayKey>" + Config.get('paymentgateway_secretkey') + "</PxPayKey>"
    xml_request += "<Response>" + fields['result'] + "</Response>"
    xml_request += "</ProcessResponse>"

    req = urllib2.Request(pxpay_url, xml_request)
    xml_response = minidom.parse(urllib2.urlopen(req))

    response_node = xml_response.getElementsByTagName("Response")[0]
    valid = response_node.getAttribute("valid")
    if valid != '1':
        return None, ['Invalid response from payment gateway: ' + get_node_value(response_node, 'ResponseText')]

    currency_request = get_node_value(response_node, 'CurrencyInput')
    transaction_type = get_node_value(response_node, 'TxnType')

    response = {
        'approved' : False,
        'success_code' : get_node_value(response_node, 'Success'),
        'amount_paid' : get_node_value(response_node, 'AmountSettlement'),
        'auth_code' : get_node_value(response_node, 'AuthCode'),
        'card_name' : get_node_value(response_node, 'CardHolderName'),
        'card_type' : get_node_value(response_node, 'CardName'),
        'card_number' : get_node_value(response_node, 'CardNumber'),
        'card_expiry' : get_node_value(response_node, 'DateExpiry'),
        'card_mac' : get_node_value(response_node, 'TxnMac'),
        'gateway_ref' : get_node_value(response_node, 'DpsTxnRef'),
        'response_text' : get_node_value(response_node, 'ResponseText'),
        'currency_used' : get_node_value(response_node, 'CurrencySettlement'),
        'invoice_id' : get_node_value(response_node, 'MerchantReference'),
        'client_ip_zookeepr' : get_node_value(response_node, 'TxnData1'),
        'client_ip_gateway' : get_node_value(response_node, 'ClientInfo'),
        'payment_id' : get_node_value(response_node, 'TxnId'),
        'email_address' : get_node_value(response_node, 'TxnData2'),
    }

    validation_errors = []

    # Reformat a few fields for zkpylons
    if response['amount_paid'] is not None:
        response['amount_paid'] = int(float(response['amount_paid']) * 100)
    if response['payment_id'] is not None:
        if 'PAY' == response['payment_id'][0:3]:
            response['payment_id'] = int(response['payment_id'][3:])
        else:
            validation_errors.append('Wrong format in the payment ID field: ' + response['payment_id'])
    if response['invoice_id'] is not None:
        if 'INV' == response['invoice_id'][0:3]:
            response['invoice_id'] = int(response['invoice_id'][3:])
        else:
            validation_errors.append('Wrong format in the invoice ID field: ' + response['invoice_id'])

    # Indicate whether or not the payment gateway has approved this transaction
    if response['success_code'] != '0':
        response['approved'] = True
    else:
        validation_errors.append('Transaction declined or unsuccessful (success_code=' + response['success_code'] + ')')

    # Validate the fields specific to the payment gateway (which we do not store)
    if transaction_type != 'Purchase':
        validation_errors.append('Invalid transaction type: ' + response['transaction_type'])
    if currency_request != currency:
        validation_errors.append('An invalid currency type was requested: ' + response['currency_request'])

    return response, validation_errors

# The TXT fields used to store user emails in PxPay are buggy and drop certain characters :(
def munge_email(email):
    ret = email.replace('+', ' ')
    return ret
