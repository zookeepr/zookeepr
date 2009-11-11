#!/usr/bin/perl -w

# Rewrite the SVG file to XSL fixing (some) fields.  This makes it much
# easier to prepare the stylesheet for the PDF invoices.

my %names = (
  desc => 'description',
  qty  => 'qty',
  sub  => 'subtotal',
  each => 'each',
  attn => 'attn',
  'inv num' => 'invoice/number',
  'inv paid txn' => 'invoice/paid/transaction',
  'inv amount' => 'invoice/amount',
  'inv owed' => 'invoice/owed',
);


while (<>) {
  $_ =~ s/>(desc|qty|sub|each) (\d+)<(?!(xsl:)?value-of)/><xsl:value-of select="invoice\/items\/item$2\/$names{$1}" \/></;
  $_ =~ s/>(desc|qty|sub|each) (\d+)(<(xsl:)?value-of)/>$3/;

  $_ =~ s/>(attn) (\d+)<(?!(xsl:)?value-of)/><xsl:value-of select="invoice\/$1\/field$2" \/></;
  $_ =~ s/>(attn) (\w+)<(?!(xsl:)?value-of)/><xsl:value-of select="invoice\/$1\/$2" \/></;

  $_ =~ s/issued (\w+)(?!<(xsl:)?value-of)/<xsl:value-of select="invoice\/issued\/date\/$1" \/>/g;
  $_ =~ s/(inv (amount|owed))(?!<(xsl:)?value-of)/<xsl:value-of select="$names{$1}" \/>/g;
  $_ =~ s/inv (num|paid txn)(?!<(xsl:)?value-of)/<xsl:value-of select="$names{$1}" \/>/g;
  $_ =~ s/inv (num|paid txn)(<(xsl:)?value-of)/$2/g;


  $_ =~ s/<value-of/<xsl:value-of/;

  print $_;

  if ($_ =~ /^<\?xml/) {
    print <<EOF;
<!-- Created with Inkscape (http://www.inkscape.org/) -->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:template match="/">
<xsl:comment>
  Zookeepr invoice template
</xsl:comment>
EOF
  }
}

print <<EOF;
</xsl:template>
</xsl:stylesheet>
EOF
