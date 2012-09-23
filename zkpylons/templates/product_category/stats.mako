<%inherit file="/base.mako" />
<%def name="extra_head()">
    <!--[if IE]><script language="javascript" type="text/javascript" src="/js/flot/excanvas.min.js"></script><![endif]-->
    <script language="javascript" type="text/javascript" src="/js/flot/jquery.flot.js"></script>
    <script language="javascript" type="text/javascript" src="/js/flot/jquery.flot.pie.js"></script>
</%def>

<%
  import re 
  grand_total = 0
  count = 0
  graph_data = []

  cat_menu = []
  for category in c.product_categories:
    esc_name = h.util.html_escape(category.name)
    if category.id == c.product_category.id:
      cat_menu.append(esc_name)
    else:
      cat_menu.append(h.link_to(esc_name,
            url=h.url_for(controller='product_category', id=category.id,
            action='stats')))
  cat_menu = 'See also:' + ' &#8226; '.join(cat_menu)
%>

    <h2>List products in the ${c.product_category.name} category</h2>
% if True:
<%
      category = c.product_category
      simple_title = re.compile('([^a-zA-Z0-9])').sub('', category.name) 
      count = count + 1
      graph_invoiced_sales = dict()
%>

    <table>
      <thead>
        <td colspan="12" align="left">
    <b>Pie charts:</b> Show invoiced product counts (including overdue).
        </td>
      <tr>
        <td colspan="12" align="center"><div id="sales${ simple_title }" style="width:600px;height:300px;"></div></td>
      </tr>
      <tr>
        <td colspan="12" align="left">
    <b>Note:</b> Money totals are not necessarily accurate as vouchers are not taken into account. They are simply paid items times cost.
        </td>
      </tr>
      <tr>
        <th>Description</th>
        <th>Display Order</th>
        <th>Active</th>
        <th>Available</th>
        <th>Cost</th>
        <th>Invoiced (Overdue)</th>
        <th>Invoiced (Current)</th>
        <th>Sold</th>
        <th>Free</th>
        <th>Total</th>
        <th>&nbsp;</th>
        <th>&nbsp;</th>
      </tr></thead>
%       if len(category.products) > 0:
<%
           cat_total = 0
           invoiced_total = 0
           valid_invoices_total = 0
           sold_total = 0
           free_total = 0
%>
%           for product in category.products:
<%
               cat_total += (product.qty_sold() * product.cost)
               invoiced_total += product.qty_invoiced(date = False)
               valid_invoices_total += product.qty_invoiced()
               sold_total += product.qty_sold()
               free_total += product.qty_free()
               graph_invoiced_sales[product.description] = product.qty_invoiced(date = False)
%>

      <tr class="${ h.cycle('odd', 'even') }">
        <td>${ h.link_to(product.description, url=h.url_for(controller='product', action='view', id=product.id)) }</td>
        <td>${ product.display_order }</td>
        <td>${ h.yesno(product.active) |n }</td>
        <td>${ h.yesno(product.available()) |n }</td>
        <td>${ h.integer_to_currency(product.cost) | h }</td>
        <td>${ product.qty_invoiced(date = False) }</td>
        <td>${ product.qty_invoiced() }</td>
        <td>${ product.qty_sold() }</td>
        <td>${ product.qty_free() }</td>
        <td>${ h.integer_to_currency(product.qty_sold() * product.cost) }</td>
%               if c.can_edit:
%                   for action in ['edit', 'delete']:
        <td>${ h.link_to(action, url=h.url_for(controller='product', action=action, id=product.id)) }</td>
%                   endfor
%               endif
      </tr>
%           endfor
<%
            grand_total += cat_total

            products = graph_invoiced_sales.keys()
            products.sort()
            graph_data = []

            sales_d1 = '['
            first = True
            for p in products:
              if first:
                first = False
              else:
                sales_d1 += ', '

              sales_d1 += '{ label: "' + p + '", data: ' + str(graph_invoiced_sales[p]) + '}'
            sales_d1 += ']'
%>
        <tr>
            <td colspan="5" style="font-weight: bold; text-align: right;">Totals:</td>
            <td>${ invoiced_total }</td>
            <td>${ valid_invoices_total }</td>
            <td>${ sold_total }</td>
            <td>${ free_total }</td>
            <td colspan="3">${ h.integer_to_currency(cat_total) }</td>
        </tr>
%       endif
%       if count == len(c.product_categories):
        <tr>
            <td colspan="8" style="font-weight: bold; text-align: right;">Grand Total:</td>
            <td colspan="3">${ h.integer_to_currency(grand_total) }</td>
        </tr>
%       endif
    </table>

<script type="text/javascript">
% if category.products:
%       if sales_d1 == '[]':
    $("#sales${simple_title }").hide()
%       else:
  var sales_d1 = ${ sales_d1 | n };

    $.plot($("#sales${ simple_title }"), sales_d1, {
        "series": {
          "pie": {
            "show": true,
            "combine": {
              "color": "#999",
              "threshold": 0.02
            }
          },
        },
        "legend": {
          "backgroundOpacity": 0.5,
        },
      }
    );
%       endif:
%       endif:
</script>




% endif

<p>${ h.link_to('Manage Categories', url=h.url_for(action='index')) }</p>
<p>${ h.link_to('New product', url=h.url_for('/product/new/%d'%category.id)) }</p>

<p>${cat_menu |n}</p>

<%def name="contents()">
<%
  menu = ''

  for category in c.product_categories:
    esc_name = h.util.html_escape(category.name)
    if category.id == c.product_category.id:
      menu += '<li>'+esc_name+'</li>'
    else:
      menu += '<li>%s</li>'%h.link_to(esc_name,
            url=h.url_for(controller='product_category', id=category.id,
            action='stats'))

  return menu
%>
</%def>
<%def name="title()">
Products -
 ${ parent.title() }
</%def>

