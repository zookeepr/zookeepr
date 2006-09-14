#!/bin/sh
echo Content-Type: text/plain
echo
echo "Your web server is running as:"
id
echo "CGI scripts work"
echo "Now we try to invoke Python interpreters and get their versions:"
python -V 2>&1
python2 -V 2>&1
python2.0 -V 2>&1
python2.1 -V 2>&1
python2.2 -V 2>&1
python2.3 -V 2>&1
python2.4 -V 2>&1
echo "Finished."
