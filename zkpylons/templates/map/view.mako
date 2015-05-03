<%inherit file="/base.mako" />

<%def name="extra_head()">
<meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
<script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script type="text/javascript" src="/js/geoxml3.js"></script>
<script type="text/javascript">
function detectBrowser() {
  var useragent = navigator.userAgent;
  var mapdiv = document.getElementById("map_canvas");
    
  if (useragent.indexOf('iPhone') != -1 || useragent.indexOf('Android') != -1 ) {
    mapdiv.style.width = '100%';
    mapdiv.style.height = '100%';
  } else {
    mapdiv.style.width = '600px';
    mapdiv.style.height = '800px';
  }
}
function map_load() {
    var myLatlng = new google.maps.LatLng(${ c.config.get('google_map_latlng') });
    var myOptions = {
      zoom: 11,
      center: myLatlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
    }

    var myMap = new google.maps.Map(document.getElementById("map_canvas"), myOptions);

    var myParser = new geoXML3.parser({map: myMap});
    myParser.parse("/map.kml");
  }
</script>
</%def>

<%def name="extra_body()">
  <body onload="map_load()">
</%def>

<h2>Venue Map</h2>

<p>View this map on <a href="${ c.config.get('google_map_url') }">Google Maps</a>, download the <a href="${ c.config.get('google_map_url') }&output=kml">KML file</a>.</p>

<div id="map_canvas" style="width:680px; height:500px"></div>
