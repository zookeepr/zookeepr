<%def name="extra_head()">
    <!--[if IE]><script language="javascript" type="text/javascript" src="/js/flot/excanvas.min.js"></script><![endif]-->
    <script language="javascript" type="text/javascript" src="/js/flot/jquery.flot.js"></script>
</%def>

<%inherit file="/base.mako" />

    <h2>View product</h2>

    <p><b>Description:</b> ${ c.product.description | h }<br></p>
    <p><b>Category:</b> ${ c.product.category.name }<br></p>
    <p><b>Active:</b> ${ h.yesno(c.product.active) |n }<br></p>
    <p><b>Cost:</b> ${ h.number_to_currency(c.product.cost/100.0) | h }<br></p>
    <p><b>Auth code:</b> ${ c.product.auth | h }<br></p>
    <p><b>Validate code:</b> ${ c.product.validate | h }<br></p>

    <h3>Product Totals</h3>
    <p><b>Note:</b> Totals are not necessarily accurate as they do not take into account for vouchers. They are simply paid items times cost.</p>
    <p><b>Invoiced (inc. overdue):</b> ${ c.product.qty_invoiced(date = False) }</p>
    <p><b>Invoiced:</b> ${ c.product.qty_invoiced() }</p>
    <p><b>Sold:</b> ${ c.product.qty_sold() }</p>
    <p><b>Total:</b> ${ h.number_to_currency((c.product.qty_sold() * c.product.cost)/100) }</p>

    <h3>Included Products</h3>
    <table>
      <thead><tr>
        <th>Name</th>
        <th>Qty</th>
      </tr></thead>
%for iproduct in c.product.included:
      <tr>
        <td>${ iproduct.include_category.name }</td>
        <td>${ iproduct.include_qty }</td>
      </tr>
%endfor
    </table>

    <h3>This Products Ceilings</h3>
    <table>
      <thead><tr>
        <th>Name</th>
        <th>Limit</th>
        <th>Available From</th>
        <th>Available Until</th>
        <th>Available</th>
        <th>Invoiced</th>
        <th>Sold</th>
      </tr></thead>
%for ceiling in c.product.ceilings:
      <tr>
        <td>${ h.link_to(ceiling.name, url=h.url_for(controller='ceiling', action='view', id=ceiling.id)) }</td>
        <td>${ ceiling.max_sold }</td>
%    if ceiling.available_from:
        <td>${ ceiling.available_from.strftime('%d/%m/%y') }</td>
%    else:
        <td></td>
%    endif
%    if ceiling.available_until:
        <td>${ ceiling.available_until.strftime('%d/%m/%y') }</td>
%    else:
        <td></td>
%    endif
        <td>${ h.yesno(ceiling.available()) |n }</td>
        <td>${ ceiling.qty_invoiced() }</td>
        <td>${ ceiling.qty_sold() }</td>
      </tr>
%endfor
    </table>

    <h3>This Product Sales</h3>

    <div id="graph_sales" style="width:600px;height:200px;"></div>
<%
#  sales = []
  sales_working = dict()
  sales_start = 0
  sales_end = 0
%>

    <table>
      <thead><tr>
        <th>Invoice</th>
        <th>Person</th>
        <th>Qty</th>
        <th>Status</th>
      </tr></thead>
%for invoice_item in c.product.invoice_items:
%    if invoice_item.invoice.paid():
<%
       sale_date = int(invoice_item.invoice.payment_received[0].last_modification_timestamp.strftime("%s")) * 1000

       if sales_start == 0 or sales_start > sale_date:
         sales_start = sale_date
       if sales_end < sale_date:
         sales_end = sale_date
#       sales.append('%s, %s' % (sale_date, invoice_item.qty))
       if sale_date not in sales_working:
         sales_working[sale_date] = invoice_item.qty
       else:
         sales_working[sale_date] += invoice_item.qty
%>
      <tr>
        <td>${ h.link_to('id: ' + str(invoice_item.invoice.id), url=h.url_for(controller='invoice', action='view', id=invoice_item.invoice.id)) }</td>
        <td>${ h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url_for(controller='person', action='view', id=invoice_item.invoice.person.id)) }</td>
        <td>${ invoice_item.qty }</td>
        <td>${ invoice_item.invoice.status() }</td>
      </tr>
%    endif
%endfor
    </table>

<%
  sales_dates = sales_working.keys()
  sales_dates.sort()
  sales = []
  sales_running = []
  sales_running_count = 0
  for sale_date in sales_dates:
    print sale_date
    sales_running_count += sales_working[sale_date]
    sales_running.append('%s, %s' % (sale_date, sales_running_count))
    sales.append('%s, %s' % (sale_date, sales_working[sale_date]))
%>


    <h3>This Product Invoices</h3>
    <table>
      <thead><tr>
        <th>Invoice</th>
        <th>Person</th>
        <th>Qty</th>
        <th>Status</th>
      </tr></thead>
%for invoice_item in c.product.invoice_items:
%    if not invoice_item.invoice.is_void() and not invoice_item.invoice.paid():
      <tr>
        <td>${ h.link_to('id: ' + str(invoice_item.invoice.id), url=h.url_for(controller='invoice', action='view', id=invoice_item.invoice.id)) }</td>
        <td>${ h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url_for(controller='person', action='view', id=invoice_item.invoice.person.id)) }</td>
        <td>${ invoice_item.qty }</td>
        <td>${ invoice_item.invoice.status() }</td>
      </tr>
%    endif
%endfor
    </table>

    <h3>Invalid Sales</h3>
    <table>
      <thead><tr>
        <th>Invoice</th>
        <th>Person</th>
        <th>Qty</th>
        <th>Status</th>
      </tr></thead>
%for invoice_item in c.product.invoice_items:
%    if not invoice_item.invoice.paid() and invoice_item.invoice.is_void():
      <tr>
        <td>${ h.link_to('id: ' + str(invoice_item.invoice.id), url=h.url_for(controller='invoice', action='view', id=invoice_item.invoice.id)) }</td>
        <td>${ h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url_for(controller='person', action='view', id=invoice_item.invoice.person.id)) }</td>
        <td>${ invoice_item.qty }</td>
        <td>${ invoice_item.invoice.status() }</td>
      </tr>
%    endif
%endfor
    </table>

    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.product.id)) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>

<script type="text/javascript">
    var d1 = [[ ${ "], [".join(sales_running) | n } ]];
    var d2 = [[ ${ "], [".join(sales) | n } ]];

    $.plot($("#graph_sales"), [ 
        { label: "Count", data: d1, lines: { fill: true } },
        { label: "Per Day", data: d2, yaxis: 2 },
      ], {
        series: { points: { show: true } },
        series: { lines: { show: true } },
        legend: {
          position: "nw"
        },
        yaxis: {
          minTickSize: 1,
        },
        yaxis2: {
          minTickSize: 1,
        },
        xaxis: {
          minTickSize: [1, "hour"],
          mode: "time",
          label: "Date",
          min: ${ sales_start },
          max: ${ sales_end },
        }
      }
    );
</script>
