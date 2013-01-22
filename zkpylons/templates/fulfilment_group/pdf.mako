<boardingpass>
  <id>${ c.fulfilment_group.id }</id>
  <code>${ c.fulfilment_group.code }</code>
%if c.fulfilment_group.person:
  <fullname>${ c.fulfilment_group.person.fullname() }</fullname>
%endif
  <fulfilments>
%for fulfilment in c.fulfilment_group.fulfilments:
    <fulfilment>
      <id>${ fulfilment.id }</id>
      <type>${ fulfilment.type.name }</type>
      <items>
% for item in fulfilment.items:
        <item>
%   if fulfilment.type.name == item.product.category.name:
          <description>${ item.product.description }</description>
%   else:
          <description>${ item.product.category.name } - ${ item.product.description }</description>
%   endif
          <qty>${ item.qty }</qty>
        </item>
% endfor
      </items>
    </fulfilment>
%endfor
  </fulfilments>
</boardingpass>
