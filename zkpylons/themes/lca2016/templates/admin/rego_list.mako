<%inherit file="/base.mako" />

<table class="table sortable">
  <tr>
    <th>Name</th>
    <th>&nbsp;</th>
    <th>ID</th>
    <th>Ticket</th>
    <th>Bag</th>
    <th>Products</th>
  </tr>
% for r in c.data:
  <tr>
    <td>${ r.person.lastname }, ${ r.person.firstname }</td>
    <td>
% if not r.person.paid():
<b>NOT PAID</b>
% else:
&nbsp;
% endif
    </td>
    <td>${ r.person.id }</td>
    <td>
<% bag = "Professional" %>
% if r.person.is_speaker():
Speaker
% elif r.person.is_miniconf_org():
Miniconf Org
% elif r.person.is_professional():
Professional
% elif r.person.has_role('press'):
Media
% else:
Hobby / Student
<% bag = "Hobby" %>
% endif
% if r.person.is_volunteer():
Volunteer
% endif
    </td>
    <td>${ bag }</td>
    <td>
<% 
  first = True
  products = dict()
  products['T-Shirt'] = []
  products['Partners Programme'] = []
  products['Partners Programme'] = []

  for invoice in r.person.invoices:
    if not invoice.is_void:
      for ii in invoice.items:
        if ii.product is not None and ii.product.category is not None:
          if ii.product.category.name in products:
            text = "%s x %s" % (ii.qty, ii.product.description)
            if not invoice.is_paid:
              text += " (Not paid)"
            products[ii.product.category.name].append(text)
%>

${ ", ".join(products['T-Shirt']) }
% if len(products['Partners Programme']) > 0:
<br />
PP: ${ ", ".join(products['Partners Programme']) }
% endif


    </td>
  </tr>
% endfor
</table>
