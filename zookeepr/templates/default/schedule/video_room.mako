<%inherit file="/base.mako" />

% if c.room_id:
    <p><a href="/schedule/video">&larr; Back to all Live Video streams</a></p>

    <h2>Live Video Stream - ${ c.room_name }</h2><br/>

%   if c.room_id == 'mfc':
        <p>
            The Michael Fowler Center Auditorium is hosting the linux.conf.au 2010
            <a href="/programme/keynotes">keynote presentations</a>. There are a number
            of different streams available depending on your connection speed:
        </p>
        <ul>
            <li><a href="_mfc_384">384kbps Stream - suitable for good broadband. Video and audio (including Ogg Theora)</a></li>
            <li><a href="_mfc_128">128kbps Stream - suitable for slow broadband. Video and audio</a></li>
            <li><a href="_mfc_56">56kbps Stream - suitable for dial up modems. Video and audio</a></li>
            <li><a href="_mfc_28a">28kbps Stream - suitable for poorly connected sites. Audio only</a></li>
        </ul>
%   else:
        <p>Welcome to the live webcast of the ${ c.room_name } from linux.conf.au 2010 in Wellington, New Zealand. Special thanks to <a href="http://www.r2.co.nz">R2</a> who are producing the video at LCA2010.</p>

        <p>Live video can be viewed by clicking on the links or player below. Note that a few presenters have not agreed (or are not able to) release video of their presentations, and the streams will be unavailable for those periods. Videos of individual presentations will be available in various <span style="border-bottom: 1px black dotted" title="OGG Theora & H264 video, OGG Vorbis & MP3 audio">formats</span> for viewing and downloading once processing and editing is completed.</p>

        <h3>Linux</h3>
        <div style="text-align:center;float:right; height:330px; width:500px; margin-left:10px; margin-bottom: 20px; border:1px solid grey;">
%       if c.room_name == 'Auditorium':
            <video src="http://repeater.xiph.org:8000/lca-mfc.ogg" controls="controls" width="500" height="330" >
                Your browser does not support the HTML5 &lt;video&gt; tag.
            </video>
%       else:
            <video src="http://repeater.xiph.org:8000/lca-${c.room_id}.ogg" controls="controls" width="500" height="330" >
                Your browser does not support the HTML5 &lt;video&gt; tag.
            </video>
%       endif
        </div>
        <p>The webcast is best viewed in <a href="http://www.mplayerhq.hu/">MPlayer</a>, although <a href="http://www.gnome.org/projects/totem/">Totem</a> and <a href="http://www.videolan.org/">VideoLan (VLC)</a> also work well.
        Thanks to Silvia Pfeiffer, Ralph Giles, Jan Gerber, Jan Schmidt, the <a href="http://www.icecast.org/">Icecast</a> project, and <a href="http://xiph.org">Xiph.org</a> there's now an Ogg Theora stream of the video as well, based out of the US. If your browser supports the HTML5 &lt;video&gt; tag, you should see a player to the right.</p>

        <p style="padding-left:20px"><strong><a href="http://www.r2.co.nz/20100118/${c.room_id}.asx">View WMV Stream (or give this URL to MPlayer/etc)</a></strong></p>
        <p style="padding-left:20px"><strong>
%       if c.room_name == 'Auditorium':
        <a href="http://repeater.xiph.org:8000/lca-mfc.ogg">View OGG Stream (or give this URL to MPlayer/etc)</a>
%       else:
        <a href="http://repeater.xiph.org:8000/lca-${c.room_id}.ogg">View OGG Stream (or give this URL to MPlayer/etc)</a>
%       endif
        </strong></p>

        <hr style="clear:right;"/>

        <h3>Mac OS X</h3>

        <div style="float:right; height:330px; width:500px; margin-left:10px; margin-bottom: 20px; border:1px solid grey;">
            <object data="data:application/x-silverlight," type="application/x-silverlight-2" height="330" width="500">
                <param name="source" value="/video_player/MinoPlayer_Ver1_2.xap">
                <param name="onerror" value="onSilverlightError">
                <param name="background" value="black">
                <param name="initParams" value="VideoSource=http://ac1.streaming.net.nz/${c.room_stream_id},AutoPlay=false,EnableScrubbing=true,InitialVolume=1">
                <param name="minRuntimeVersion" value="2.0.31005.0">
                <param name="autoUpgrade" value="true">
                <a href="http://go.microsoft.com/fwlink/?LinkID=124807" style="text-decoration: none;">
                    <img src="http://go.microsoft.com/fwlink/?LinkId=108181" alt="Get Microsoft Silverlight" style="border-style: none;">
                </a>
            </object>
            <iframe style='visibility:hidden;height:0;width:0;border:0px'></iframe>
        </div>

        <p>The webcast is best viewed in Silverlight Media Player (right), Real Player, or Mplayer, although Totem and VideoLan (VLC) also work well. If you see a Silverlight logo, you may install the free Silverlight player by clicking on it. After the installation of Silverlight, you may need to refresh your webpage (Crtl-R or F5). Or feel free to use the HTML5 &lt;video&gt; player above if your browser supports it. :)</p>
        <p style="padding-left:20px"><strong><a href="http://www.r2.co.nz/20100118/${c.room_id}.asx">View Stream</a></strong></p>

        <h3>Windows</h3>
        <p>The webcast is best viewed in Silverlight Media Player (right) or Real Player. VideoLan (VLC) also works well. If you see a Silverlight logo, you may install the free Silverlight player by clicking on it. After the installation of Silverlight, you may need to refresh your webpage (Crtl-R or F5). Or feel free to use the HTML5 &lt;video&gt; player above if your browser supports it. :)
        <p style="padding-left:20px"><strong><a href="http://www.r2.co.nz/20100118/${c.room_id}.asx">View Stream</a></strong></p>

        <div style="clear:right"></div>
%   endif

% else:
    <h2>Live Video Streams</h2><br/>
    <p>The following rooms have live streaming video available:</p>
    <ul>
%   for rk,rn,rs in c.all_rooms:
%       if not rk.startswith('_'):
            <li><a href="video/${rk}">${rn}</a></li>
%       endif
%   endfor
    </ul>
    <p>Special thanks to <a href="http://www.r2.co.nz">R2</a> who are producing the video at LCA2010.</p>
% endif

<%def name="title()">
% if c.room_id:
Live Video Streams
 - ${ c.room_name }
% else:

% endif
</%def>
