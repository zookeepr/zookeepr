<%def name="extra_head()">
    <!--[if IE]><script language="javascript" type="text/javascript" src="/js/flot/excanvas.min.js"></script><![endif]-->
    <script language="javascript" type="text/javascript" src="/js/flot/jquery.flot.js"></script>
    <script language="javascript" type="text/javascript" src="/js/flot/jquery.flot.pie.js"></script>
</%def>

<%inherit file="/base.mako" />
<% import markupsafe %>


    <a name="summary"></a>
    <h2>View Ceiling</h2>

	<p><b>Name:</b> ${ c.ceiling.name }</p>
% if c.ceiling.parent:
    <p><b>Parent:</b> ${ h.link_to(c.ceiling.parent.name, h.url_for(id=c.ceiling.parent.id)) } (This ceiling will not become available until the parent is not available)
% endif
    <p><b>Limit:</b> ${ c.ceiling.max_sold | h }<br></p>
    <p>
      <b>Available From:</b>
% if c.ceiling.available_from:
      ${ c.ceiling.available_from.strftime('%d/%m/%y') | h }
% endif
      <br>
    </p>
    <p>
      <b>Available Until:</b>
% if c.ceiling.available_until:
      ${ c.ceiling.available_until.strftime('%d/%m/%y') | h }
% endif
      <br>
    </p>
    <p><b>Currently Available:</b> ${ h.yesno(c.ceiling.available()) | n } <br></p>

    <a name="products"></a>
    <h3>Products in this Ceiling</h3>

    <table>
      <tr>
        <th>Invoiced</th>
      </tr>
      <tr>
        <td><div id="graph_invoiced_sales" style="width:500px;height:200px;"></div></td>
      </tr>
    </table>

    <p><b>Note:</b> Dollar totals are not necessarily accurate as they do not take into account vouchers. They are simply paid items times cost.</p>
    <table>
      <thead><tr>
        <th>Description</th>
        <th>Category</th>
        <th>Active</th>
        <th>Cost</th>
        <th>Invoiced (inc. overdue)</th>
        <th>Valid Invoices (paid)</th>
        <th>Paid</th>
        <th>Free</th>
        <th>Total</th>
      </tr></thead>
<% ceiling_total = 0 %>
<%
  graph_invoiced_sales = {}
%> 
% for product in c.ceiling.products:
<%   ceiling_total += product.qty_sold() * product.cost %>
      <tr>
        <td>${ h.link_to(product.description, url=h.url_for(controller='product', action='view', id=product.id)) }</td>
        <td>${ product.category.name }</td>
        <td>${ h.yesno(product.active) | n }</td>
        <td>${ h.integer_to_currency(product.cost) }</td>
        <td>${ product.qty_invoiced(date=False) }</td>
        <td>${ product.qty_invoiced() }</td>
        <td>${ product.qty_sold() }</td>
        <td>${ product.qty_free() }</td>
        <td>${ h.integer_to_currency(product.qty_sold() * product.cost) }</td>
      </tr>
<%
  graph_invoiced_sales[product.description] = product.qty_invoiced(date=False)
%>
% endfor
      <tr>
        <td colspan="4" style="font-weight: bold; text-align: right;">Total:</td>
        <td>${ c.ceiling.qty_invoiced( date = False )  }</td>
        <td>${ c.ceiling.qty_invoiced()  }</td>
        <td>${ c.ceiling.qty_sold()  }</td>
        <td>${ c.ceiling.qty_free()  }</td>
        <td>${ h.integer_to_currency(ceiling_total) }</td>
    </table>
<script type="text/javascript">
<%
  d1 = '['
  first = True
  for desc in graph_invoiced_sales:
    if first:
      first = False
    else:
      d1 += ', '
    d1 += '{ label: "' + desc + '", data: ' + str(graph_invoiced_sales[desc]) + '}'
  d1 += ']'
%>
  var d1 = ${ d1 | n };

  $.plot($("#graph_invoiced_sales"), d1,
    {
      series: {
        pie: {
          show: true,
          label: {
            radius: 3/4,
            opacity: 0.5,
            formatter: function(label, series){
              return '<div style="font-size:8pt;text-align:center;padding:2px;color:white;">'+label+'<br/>'+Math.round(series.percent)+'%</div>';
            }
          },
          combine: {
             color: '#999',
             threshold: 0.02
          }
        }
      },
      legend: { backgroundOpacity: 0.5 }
    });
</script>
    
    <a name="paid_invoices"></a>
    <h3>Paid invoices in this Ceiling</h3>
    <table>
      <thead><tr>
        <th>Invoice</th>
        <th>Person</th>
        <th>Product</th>
        <th>Qty</th>
        <th>Status</th>
      </tr></thead>
% for product in c.ceiling.products:
%   for invoice_item in product.invoice_items:
%        if invoice_item.invoice.is_paid:
      <tr>
        <td>${ h.link_to('id: ' + str(invoice_item.invoice.id), url=h.url_for(controller='invoice', action='view', id=invoice_item.invoice.id)) }</td>
        <td>${ h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url_for(controller='person', action='view', id=invoice_item.invoice.person.id)) }</td>
        <td>${ invoice_item.description }</td>
        <td>${ invoice_item.qty }</td>
        <td>${ invoice_item.invoice.status }</td>
      </tr>
%        endif
%   endfor
% endfor
    </table>

    <a name="unpaid_invoices"></a>
    <h3>Unpaid invoices in this Ceiling</h3>
    <table>
      <thead><tr>
        <th>Invoice</th>
        <th>Person</th>
        <th>Product</th>
        <th>Qty</th>
        <th>Status</th>
      </tr></thead>
% for product in c.ceiling.products:
%   for invoice_item in product.invoice_items:
%        if not invoice_item.invoice.is_void and not invoice_item.invoice.is_paid:
      <tr>
        <td>${ h.link_to('id: ' + str(invoice_item.invoice.id), url=h.url_for(controller='invoice', action='view', id=invoice_item.invoice.id)) }</td>
        <td>${ h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url_for(controller='person', action='view', id=invoice_item.invoice.person.id)) }</td>
        <td>${ invoice_item.description }</td>
        <td>${ invoice_item.qty }</td>
        <td>${ invoice_item.invoice.status }</td>
      </tr>
%        endif
%   endfor
% endfor
    </table>

    <a name="invalid_invoices"></a>
    <h3>Invalid Invoices in this Ceiling</h3>
    <table>
      <thead><tr>
        <th>Invoice</th>
        <th>Person</th>
        <th>Product</th>
        <th>Qty</th>
        <th>Status</th>
      </tr></thead>
% for product in c.ceiling.products:
%   for invoice_item in product.invoice_items:
%        if not invoice_item.invoice.is_paid and invoice_item.invoice.is_void:
      <tr>
        <td>${ h.link_to('id: ' + str(invoice_item.invoice.id), url=h.url_for(controller='invoice', action='view', id=invoice_item.invoice.id)) }</td>
        <td>${ h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url_for(controller='person', action='view', id=invoice_item.invoice.person.id)) }</td>
        <td>${ invoice_item.description }</td>
        <td>${ invoice_item.qty }</td>
        <td>${ invoice_item.invoice.status }</td>
      </tr>
%        endif
%   endfor
% endfor
    </table>

    <p>
    ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.ceiling.id)) } |
    ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</p>

<%def name="contents()">
<%
  menu =  '<li><a href="#summary">Summary</a></li>'
  menu += '<li><a href="#products">Products in Ceiling</a></li>'
  menu += '<li><a href="#paid_invoices">Paid Invoices</a></li>'
  menu += '<li><a href="#unpaid_invoices">Unpaid Invoices</a></li>'
  menu += '<li><a href="#invalid_invoices">Invalid Invoices</a></li>'

  menu +=  '<li><a href="#diet_special_paid">Diet/Special - Paid</a></li>'
  menu += '<li><a href="#diet_special_invoiced">Diet/Special - Invoiced</a></li>'
  menu += '<li><a href="#diet_paid">Diet - Paid</a></li>'
  menu += '<li><a href="#diet_invoiced">Diet - Invoiced</a></li>'
  menu += '<li><a href="#under18_paid">Under 18 - Paid</a></li>'
  menu += '<li><a href="#under18_invoiced">Under 18 - Invoiced</a></li>'

  return menu
%>
</%def>
<%def name="title()">
Ceiling - ${ c.ceiling.name } - ${ parent.title() }
</%def>


<%
	paid_special_diet = { s.person_id : s for s in c.specials if s.is_paid and (s.diet or s.special)}.values()
	unpaid_special_diet = { s.person_id : s for s in c.specials if not s.is_paid and (s.diet or s.special)}.values()

	paid_diet_keys = { s.diet : 1 for s in c.specials if s.is_paid and s.diet }.keys()
	paid_diet = {}
	for key in paid_diet_keys:
		paid_diet[key] = [s for s in c.specials if s.is_paid and s.diet == key]
	unpaid_diet_keys = { s.diet : 1 for s in c.specials if not s.is_paid and s.diet }.keys()
	unpaid_diet = {}
	for key in unpaid_diet_keys:
		unpaid_diet[key] = [s for s in c.specials if not s.is_paid and s.diet == key]

	paid_u18 = [s for s in c.specials if s.is_paid and s.u18]
	unpaid_u18 = [s for s in c.specials if not s.is_paid and s.u18]

%>
<h3 id="diet_special_paid">Diet/Special - Paid</h3>
${ diet_special(paid_special_diet) }

<h3 id="diet_special_invoiced">Diet/Special - Invoiced (Not Paid)</h3>
${ diet_special(unpaid_special_diet) }

<h3 id="diet_paid">Diet - Paid</h3>
${ diet(paid_diet) }

<h3 id="diet_invoiced">Diet - Invoiced (Not Paid)</h3>
${ diet(unpaid_diet) }

<h3 id="under18_paid">Under 18 - Paid</h3>
${ under18(paid_u18) }

<h3 id="under18_invoiced">Under 18 - Invoiced (Not Paid)</h3>
${ under18(unpaid_u18) }

<%def name="diet_special(data)">
<table>
  <thead><tr>
    <th>Person</th>
    <th>Rego ID</th>
    <th>Product</th>
    <th>Diet</th>
    <th>Special Needs</th>
  </tr></thead>
  <tbody>
	% if len(data):
		% for s in data:
			<tr>
				<td>${ h.link_to(s.fullname, h.url_for(controller='person', action='view', id=s.person_id)) }</td>
				<td>${ h.link_to('rego id: ' + str(s.reg_id), url=h.url_for(controller='registration', action='view', id=s.reg_id)) }</td>
				<td>${ s.product }</td>
				<td>${ s.diet }</td>
				<td>${ s.special }</td>
			</tr>
			% for note in s.notes:
				<tr>
					<td>&nbsp;</td>
					<td colspan="4">${ note.note }</td>
				</tr>
			% endfor
		% endfor
	% else:
		<tr>
			<td colspan="5">No entries</td>
		</tr>
	% endif
  </tbody>
</table>
</%def>

<%def name="diet(data)">
<table>
  <thead><tr>
    <th>Diet</th>
    <th>People</th>
  </tr></thead>
  <tbody>
	% for diet in data:
		<tr>
			<td>${ diet }</td>
			<td>${ markupsafe.Markup(", ".join([h.link_to(e.fullname, h.url_for(controller='person', action='view', id=e.person_id)) for e in data[diet]])) }</td>
		</tr>
	% endfor
	% if len(data) == 0:
		<tr><td colspan="2">No entries</td></tr>
	% endif
  </tbody>
</table>
</%def>

<%def name="under18(data)">
<table>
  <thead><tr>
    <th>Person</th>
    <th>Rego ID</th>
    <th>Product</th>
  </tr></thead>
  <tbody>
	% for u in data:
		<tr>
			<td>${ h.link_to(u.fullname, h.url_for(controller='person', action='view', id=u.person_id)) }</td>
			<td>${ h.link_to('rego id: ' + str(u.reg_id), url=h.url_for(controller='registration', action='view', id=u.reg_id)) }</td>
			<td>${ u.product }</td>
		</tr>
	% endfor
	% if len(data) == 0:
		<tr><td colspan="3">No entries</td></tr>
	% endif
  </tbody>
</table>
</%def>



