#!/bin/sh
echo Content-Type: text/plain
echo
echo "Your web server is running as:"
id
echo "CGI scripts work"
echo "Now we try to invoke Python interpreters and get their versions:"
echo "Your default version of python is:"
python -V 2>&1
echo 
echo "Available versions of python are:"
python2.2 -V 2>&1 && which python2.2
python2.3 -V 2>&1 && which python2.3
python2.4 -V 2>&1 && which python2.4
python2.5 -V 2>&1 && which python2.5
echo "Finished."

