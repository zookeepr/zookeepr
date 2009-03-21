<%!
    title = 'linux.conf.au 2009 | 19 - 24 Jan | Marchsouth to Hobart'
%>

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en-us">
<head>
  <title>${self.attr.title}</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" media="screen" href="/marchsouth.css" type="text/css">
  <link href="/media/news/rss" rel="alternate" type="application/rss+xml" title="LCA09 News">
  <!--[if lt IE 7]>
  <link rel="stylesheet" media="screen" href="/ie.css" type="text/css">
  <![endif]-->
  ${self.extra_head()}
</head>

<body>
  <div class = 'content'>
    <div class = 'banner'>
      <a href="/"><img src = '/images/mountain.png' alt = 'Mount Wellington' class = 'mountain'></a>
      <a href="/"><img src = '/images/tuz.png' alt = 'mascot' class = 'mascot'></a>
      <a href="/"><img src = '/images/lca.png' alt = 'linux.conf.au' class = 'lca'></a>
      <a href="/"><img src = '/images/marchsouth.png' alt = 'march south together'></a>
    </div>
    <div class = 'menu'>
      ${self.big_promotion()}
<%include file="nav.mako" />
<%include file="subnav.mako" />
    </div>
    <!-- start content -->
    ${next.body()}
    <!-- end content -->

  </div>

% if not h.url.current().endswith('/sponsors/sponsors') and not h.url.current().endswith('/media/news/61'):
    <p class='sponsors_footer'>
      <a href="/sponsors/sponsors"><img src="/sponsors/HP-front.png" alt="Hewlett-Packard Logo"></a>
      <a href="/sponsors/sponsors"><img src="/sponsors/IBM-front.png" alt="IBM Logo"></a>
    </p>
% endif

  <div class = 'footer'>
    <div class = 'photos'>
      <img src = '/images/photo1.png' alt = 'Tasmania'>
      <img src = '/images/photo2.png' alt = 'Tasmania'>
      <img src = '/images/photo3.png' alt = 'Tasmania'>
      <img src = '/images/photo4.png' alt = 'Tasmania'>
      <img src = '/images/photo5.png' alt = 'Tasmania'>
    </div>
    <div class = 'copyright'>&copy; 2008-2009 <a href = 'http://www.linux.org.au'>Linux Australia</a> and LCA09 | Linux is a registered trademark of Linus Torvalds | <a href="http://validator.w3.org/check?uri=referer">HTML 4.01 Strict</a>
    </div>
  </div>
</body>
</html>
