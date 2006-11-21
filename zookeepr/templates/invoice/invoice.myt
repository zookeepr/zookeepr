<%init>
total = 0
</%init>
                         Linux Australia Incorporated
                            TAX INVOICE/STATEMENT
                             ABN 56 987 117 479
#                             NZ GST #90-792-369

Issue Date: <% invoice.issue_date.strftime("%Y-%m-%d") %>

TAX INVOICE REFERENCE: <% invoice.id %>

Attention: <% invoice.person.fullname %>

linux.conf.au 2007

This invoice has been issued as a result of an application to attend
linux.conf.au 2007, being held at the University of New South Wales
in Sydney, Australia.


Description                                             Cost

% for item in invoice.items:	
<% "%-50s\t%s" % (item.description, h.number_to_currency(item.cost)) %>

%	total += item.cost
% #endif
----------------------------------------------------------------
                                                 Total: <% h.number_to_currency(total) %>



Further information on your registration is available at:
http://lca2007.linux.org.au/profile

Enquiries may be emailed to the organisers:
  seven-contact@lca2007.linux.org.au .

linux.conf.au is a project of Linux Australia, Incorporated.
              GPO Box 4788,  Sydney NSW 2001, Australia
                         ABN 56 987 117 479
#                         NZ GST #90-792-369
                        fax: +61 2 8211 5211

<%args>
invoice
</%args>
