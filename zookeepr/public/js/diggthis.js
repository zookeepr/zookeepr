/* Digg 'diggthis' JS library. */
(function() {
   function d_pa(dtb) { // parse anchors
       for (var i=0; i<dtb.length; i++) {
           // parse options
           opt = new Object();

           // get skin
           var m = /diggThis(Compact|Icon)?\.(gif|png)/i.exec(dtb[i].innerHTML);
           if (m && m[1]) opt.d_skin = m[1].toLowerCase();

           // get title and url
           var m = /http:\/\/digg\.com\/submit\?url=([^&]*)&(amp;)?title=([^&]*)/i.exec(dtb[i].href);
           if (m && m[3]) opt.d_title = unescape(m[3]);
           if (m && m[1]) opt.d_url = unescape(m[1]);

           // get background color
           if (dtb[i].style.backgroundColor) opt.d_bgcolor = d_pc(dtb[i].style.backgroundColor).toHex();

           // get media and topic
           var m = /(news|image|video)?,?\s*([^\s]*)?/i.exec(dtb[i].rev);
           if (m && m[1]) opt.d_media = m[1];
           if (m && m[2]) opt.d_topic = m[2];

           // get window preference
           var m = /\bexternal\b/i.exec(dtb[i].rel);
           if (m) opt.d_window = 'new';

           // get body text
           var m = /<span[^>]*>([^<]*)<\/span>/i.exec(dtb[i].innerHTML);
           if (m && m[1]) opt.d_bodytext = m[1];
           if (opt.d_bodytext && opt.d_bodytext.length > 350) opt.d_bodytext = opt.d_bodytext.substring(0, 350);

           // force visibility
           dtb[i].style.visibility = 'visible';
           dtb[i].style.display = 'block';

           var d = document.createElement('DIV');
           d.innerHTML = d_gs(opt);
           dtb[i].parentNode.replaceChild(d.firstChild, dtb[i]);
       }
   }
   function d_gs(o) {
       if (!o) o = new Object();

       var du  = escape(o.d_url ? o.d_url : (typeof digg_url == 'string') ? digg_url : ((typeof DIGG_URL == 'string') ? DIGG_URL : window.location.href)).replace(/\+/g, '%2b');
       var h=80, w=52;
       var ds  = o.d_skin     ? '&s=' + escape(o.d_skin)     : (typeof digg_skin     == 'string') ? '&s=' + escape(digg_skin)     : '';
       var dt  = o.d_title    ? '&t=' + escape(o.d_title)    : (typeof digg_title    == 'string') ? '&t=' + escape(digg_title)    : '&t=' + escape(document.title);
       var dw  = o.d_window   ? '&w=' + escape(o.d_window)   : (typeof digg_window   == 'string') ? '&w=' + escape(digg_window)   : '';
       var dbt = o.d_bodytext ? '&b=' + escape(o.d_bodytext) : (typeof digg_bodytext == 'string') ? '&b=' + escape(digg_bodytext) : '';
       var dm  = o.d_media    ? '&m=' + escape(o.d_media)    : (typeof digg_media    == 'string') ? '&m=' + escape(digg_media)    : '';
       var dc  = o.d_topic    ? '&c=' + escape(o.d_topic)    : (typeof digg_topic    == 'string') ? '&c=' + escape(digg_topic)    : '';
       var dbg = o.d_bgcolor  ? '&k=' + escape(o.d_bgcolor)  : (typeof digg_bgcolor  == 'string') ? '&k=' + escape(digg_bgcolor)  : '';

       if (ds == '&s=compact')   { h=18; w=120; }
       else if (ds == '&s=icon') { h=16; w=16; }

       return "<iframe src=\"http://digg.com/tools/diggthis.php?u=" + du + ds + dt + dw + dbt + dm + dc + dbg + "\" height='" + h + "' width='" + w + "' frameborder='0' scrolling='no'></iframe>";
   }
   function d_pc(color_string) { // parse color
       var t = new Object();
       color_string = color_string.replace(/[ #]/g,'').toLowerCase();
       var color_defs = [{ // array of color definition objects
           re: /^rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)$/,
           process: function (bits) { return [ parseInt(bits[1]), parseInt(bits[2]), parseInt(bits[3])]; }
       }, {
           re: /^(\w{2})(\w{2})(\w{2})$/,
           process: function (bits) { return [parseInt(bits[1], 16), parseInt(bits[2], 16), parseInt(bits[3], 16)]; }
       }, {
           re: /^(\w{1})(\w{1})(\w{1})$/,
           process: function (bits) { return [ parseInt(bits[1] + bits[1], 16), parseInt(bits[2] + bits[2], 16), parseInt(bits[3] + bits[3], 16)]; }
       }];

       for (var i = 0; i < color_defs.length; i++) { // search through the definitions to find a match
   		var bits = color_defs[i].re.exec(color_string)
           if (bits) {
   			channels = color_defs[i].process(bits);
   			t.r = parseInt(channels[0]);
               t.g = parseInt(channels[1]);
               t.b = parseInt(channels[2]);
           }
       }

       // validate/cleanup values
       t.r = (t.r < 0 || isNaN(t.r)) ? 0 : ((t.r > 255) ? 255 : t.r);
       t.g = (t.g < 0 || isNaN(t.g)) ? 0 : ((t.g > 255) ? 255 : t.g);
       t.b = (t.b < 0 || isNaN(t.b)) ? 0 : ((t.b > 255) ? 255 : t.b);

       t.toRGB = function () { return 'rgb(' + t.r + ', ' + t.g + ', ' + t.b + ')'; }
       t.toHex = function () {
           var r = t.r.toString(16);
           var g = t.g.toString(16);
           var b = t.b.toString(16);
           if (r.length == 1) r = '0' + r;
           if (g.length == 1) g = '0' + g;
           if (b.length == 1) b = '0' + b;
           return '#' + r + g + b;
       }
   	t.toString = function() { return t.toHex(); }
   	t.fadeTo = function (color, percentage) {
   		t.r = t.r + Math.round((color.r - t.r) * percentage);
   		t.g = t.g + Math.round((color.g - t.g) * percentage);
   		t.b = t.b + Math.round((color.b - t.b) * percentage);
   		return t.toHex();
   	}

   	return t;
   }
   var dtb = [];
   var elem = document.body.getElementsByTagName('A');
   for (var i = 0; i < elem.length; i++) {
       if (/\bDiggThisButton\b/.test(elem[i].className)) {
           dtb.push(elem[i]);
       }
   }
   if (dtb.length) {
       var old = window.onload;
   	if (typeof window.onload != 'function') window.onload = function() { d_pa(dtb); }
   	else window.onload = function() { old(); d_pa(dtb); }
   } else {
       document.write(d_gs());
   }
})();
