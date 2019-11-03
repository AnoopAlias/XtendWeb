#!/usr/bin/python

import commoninclude
import cgi
import cgitb
import subprocess
from commoninclude import print_simple_header, print_simple_footer


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()

form = cgi.FieldStorage()

print_simple_header()

if form.getvalue('user'):
    subprocess.call(installation_path+'/scripts/cluster_gdnsd_ensure_user.py '+form.getvalue('user'), shell=True)
    commoninclude.print_success('GeoDNS zones synced successfully.')
else:
    commoninclude.print_forbidden()

print_simple_footer()
