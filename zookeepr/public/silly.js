    function toggle_select_hidden(select, field) {
      if ( document.getElementById(select).value == 'other' ) {
        document.getElementById(field).style.display = 'inline';
      } else {
        document.getElementById(field).style.display = 'none';
      }
    }

    function silly_description() {
        path = "/registration/silly_description";
        xmlHttp = XMLHTTPObject();
        xmlHttp.open("POST", path, false);
        xmlHttp.send(null);
        response = xmlHttp.responseText;
        response_array = response.split(',');
        document.getElementById('silly_description').textContent = response_array[1];
        document.getElementById('registration.silly_description').value = response_array[1];
        document.getElementById('registration.silly_description_checksum').value = response_array[0];
    }

    function XMLHTTPObject() {
        var xmlhttp;
        if (window.ActiveXObject) {
            // Instantiate the latest Microsoft ActiveX Objects
            if (_XML_ActiveX) {
                xmlhttp = new ActiveXObject(_XML_ActiveX);
            } else {
                // loops through the various versions of XMLHTTP to ensure we're using the latest
                var versions = ["MSXML2.XMLHTTP", "Microsoft.XMLHTTP", "Msxml2.XMLHTTP.7.0", "Msxml2.XMLHTTP.6.0", "Msxml2.XMLHTTP.5.0", "Msxml2.XMLHTTP.4.0", "MSXML2.XMLHTTP.3.0"];
                for (var i = 0; i < versions.length ; i++) {
                    try {
                        // Try and create the ActiveXObject for Internet Explorer, if it doesn't work, try again.
                        xmlhttp = new ActiveXObject(versions[i]);
                        if (xmlhttp) {
                            var _XML_ActiveX = versions[i];
                            break;
                        }
                    } catch (e) {
                    // TRAP
                    };
                };
            }
        }
        // Well if there is no ActiveXObject available it must be firefox, opera, or something else
        if (!xmlhttp && typeof XMLHttpRequest != 'undefined') {
            try {
                xmlhttp = new XMLHttpRequest();
            } catch (e) {
                xmlhttp = false;
            }
        }
        return xmlhttp;
    }
