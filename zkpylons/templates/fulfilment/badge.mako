<badge>
  <id>${ c.fulfilment.id }</id>
  <code>${ c.fulfilment.code }</code>
%if c.fulfilment.person:
  <firstname>${ c.fulfilment.person.firstname }</firstname>
  <lastname>${ c.fulfilment.person.lastname }</lastname>
  <company>${ c.fulfilment.person.company }</company>
% if reduce(lambda a, b: a or (b.product_id in [4,5,6,7,8,11,12]), c.fulfilment.items, False) or False:
  <pdns>1</pdns>
% else:
  <pdns>0</pdns>
% endif
%if c.fulfilment.person.country == 'AUSTRALIA':
% if 'tas' in c.fulfilment.person.state.lower():
  <origin>tasmania</origin>
% else:
  <origin>australia</origin>
% endif
%elif c.fulfilment.person.country == 'NEW ZEALAND':
  <origin>new zealand</origin>
%else:
  <origin>world</origin>
%endif
% if c.fulfilment.person.registration:
%   if c.fulfilment.person.registration.over18:
  <over18>1</over18>
%   else:
  <over18>0</over18>
%   endif
  <preferences>
<% registration = c.fulfilment.person.registration %>
${ registration.nick }\
%   if registration.nick and registration.distro:
@\
%   endif
${ registration.distro }\
%   if registration.distro and registration.shell:
:\
%   endif
${ registration.shell }\
%   if registration.shell:
$ \
%   endif
${ registration.editor }\
%   if registration.editor and registration.vcs:
 ; \
%   endif
${ registration.vcs }\
  </preferences>
  <silly_description>${ c.fulfilment.person.registration.silly_description }</silly_description>
  <keyid>${ c.fulfilment.person.registration.keyid }</keyid>
% endif
%endif
  <items>
% for item in c.fulfilment.items:
    <item>
      <product_id>${ item.product_id }</product_id>
      <product_category>${ item.product.category.name }</product_category>
      <product_description>${ item.product.description }</product_description>
%   if item.product.badge_text:
      <product_text>${ item.product.badge_text }</product_text>
%   else:
      <product_text>${ item.product_text }</product_text>
%   endif
      <qty>${ item.qty }</qty>
    </item>
%endfor
  </items>
</badge>
