#!/usr/bin/python
import os
import socket
import yaml
import cgi
import cgitb
import re
import sys


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path

cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>XtendWeb</title>')
print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')
print('<div class="row">')
print('<div class="col-md-6 col-md-offset-3">')
print('<div class="logo">')
print('<a href="xtendweb.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-cog" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-home"></span></a></li>')
print('<li><a href="xtendweb.live.py">Set Domain</a></li><li class="active">Password Protected URLs</li>')
print('</ol>')
print('<div class="panel panel-default">')
if form.getvalue('domain') and form.getvalue('action') and form.getvalue('protectedurl'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    action = form.getvalue('action')
    protectedurl = form.getvalue('protectedurl')
    if not protectedurl.startswith('/'):
        protectedurl = '/'+protectedurl
    if protectedurl != '/' and protectedurl.endswith('/'):
        protectedurl = protectedurl[:-1]
    if not re.match("^[0-9a-zA-Z/_-]*$", protectedurl):
        print("Error: Invalid char in sub-directory name")
        sys.exit(0)
    profileyaml = installation_path + "/domain-data/" + mydomain
    if os.path.isfile(profileyaml):
        # Get all config settings from the domains domain-data config file
        with open(profileyaml, 'r') as profileyaml_data_stream:
            yaml_parsed_profileyaml = yaml.safe_load(profileyaml_data_stream)
        protected_dir_list = yaml_parsed_profileyaml.get('protected_dir')
        if action == 'add':
            if protectedurl not in protected_dir_list:
                protected_dir_list.append(protectedurl)
        elif action == 'del':
            if protectedurl in protected_dir_list:
                protected_dir_list.remove(protectedurl)
        yaml_parsed_profileyaml['protected_dir'] = protected_dir_list
        print(('<div class="panel-heading"><h3 class="panel-title">Domain: <strong>'+mydomain+'</strong></h3></div><div class="panel-body">'))
        with open(profileyaml, 'w') as yaml_file:
            yaml.dump(yaml_parsed_profileyaml, yaml_file, default_flow_style=False)
        print('<div class="icon-box">')
        print('<span class="glyphicon glyphicon-thumbs-up" aria-hidden="true"></span> Password Protected URLs updated')
        print('</div>')
        print('</form>')
    else:
        print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> domain-data file i/o error</div>')
else:
    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden</div>')
print('</div>')
print('<div class="panel-footer"><small>Powered by <a target="_blank" href="http://xtendweb.gnusys.net/">XtendWeb</a> <span class="glyphicon glyphicon-flash" aria-hidden="true"></span> Themed by <a target="_blank" href="http://www.stirstudiosdesign.com/">StirStudios</a></small></div>')
print('</div>')
print('<div class="help pull-right"><a target="_blank" href="http://xtendweb.gnusys.net/"><span class="glyphicon glyphicon-question-sign" aria-hidden="true"></span> <em>Need Help?</em></a></div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')