#!/bin/python

import commoninclude
import cgi
import cgitb
import yaml
import os
import subprocess


__author__ = "Budd P Grant"
__copyright__ = "Copyright Budd P Grant"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Budd Grant, https://highavailability.io"
__email__ = "ops@highavailability.io"
__status__ = "Development"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
whm_terminal_log = installation_path+"/nDeploy_whm/term.log"

cgitb.enable()

form = cgi.FieldStorage()

print('Content-Type: text/html')
print('')
print('<html>')
print('    <head>')
print('    </head>')
print('    <body>')

if form.getvalue('test_cookie') and \
    form.getvalue('mod_security') and \
    form.getvalue('pagespeed') and \
    form.getvalue('brotli') and \
    form.getvalue('geoip2') and \
    form.getvalue('passenger'):

    cmd_install = ""
    cmd_uninstall = ""

    if form.getvalue('test_cookie') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/testcookie_access.load'):
        cmd_install += "nginx-nDeploy-module-testcookie_access "
    elif form.getvalue('test_cookie') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/testcookie_access.load'):
        cmd_uninstall += "nginx-nDeploy-module-testcookie_access "

    if form.getvalue('mod_security') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/zz_modsecurity.load'):
        cmd_install += "nginx-nDeploy-module-modsecurity "
    elif form.getvalue('mod_security') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/zz_modsecurity.load'):
        cmd_uninstall += "nginx-nDeploy-module-modsecurity "

    if form.getvalue('pagespeed') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
        cmd_install += "nginx-nDeploy-module-pagespeed "
    elif form.getvalue('pagespeed') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/pagespeed.load'):
        cmd_uninstall += "nginx-nDeploy-module-pagespeed "

    if form.getvalue('brotli') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/brotli.load'):
        cmd_install += "nginx-nDeploy-module-brotli "
    elif form.getvalue('brotli') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/brotli.load'):
        cmd_uninstall += "nginx-nDeploy-module-brotli "

    if form.getvalue('geoip2') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/geoip2.load'):
        cmd_install += "nginx-nDeploy-module-geoip2 "
    elif form.getvalue('geoip2') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/geoip2.load'):
        cmd_uninstall += "nginx-nDeploy-module-geoip2 "

    if form.getvalue('passenger') == 'enabled' and not os.path.isfile('/etc/nginx/modules.d/passenger.load'):
        cmd_install += "nginx-nDeploy-module-passenger "
    elif form.getvalue('passenger') == 'disabled' and os.path.isfile('/etc/nginx/modules.d/passenger.load'):
        cmd_uninstall += "nginx-nDeploy-module-passenger "

    if cmd_install != "" or cmd_uninstall != "":
        if cmd_install == "" and cmd_uninstall != "":
            if os.path.isfile(cluster_config_file):

                procExe = subprocess.Popen('echo "*** Uninstalling the following modules cluster-wide: '+cmd_uninstall+' ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('yum -y remove '+cmd_uninstall+' && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y remove '+cmd_uninstall+'\" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('echo "*** The following modules have been uninstalled cluster-wide: '+cmd_uninstall+' ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()

                commoninclude.print_success('The following modules have been removed cluster-wide: <br>'+cmd_uninstall)

            else:

                procExe = subprocess.Popen('echo "*** Uninstalling the following modules: '+cmd_uninstall+' ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('yum -y remove '+cmd_uninstall+' >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('echo "*** The following modules have been uninstalled cluster-wide: '+cmd_uninstall+' ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()

                commoninclude.print_success('The following modules have been removed: <br>'+cmd_uninstall)

        elif cmd_install != "" and cmd_uninstall == "":
            if os.path.isfile(cluster_config_file):

                procExe = subprocess.Popen('echo "*** Installing the following modules cluster-wide: '+cmd_install+' ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('yum -y --enablerepo=ndeploy install '+cmd_install+' && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy install '+cmd_install+'\" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('echo "*** The following modules have been installed cluster-wide: '+cmd_install+' ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()

                commoninclude.print_success('The following modules have been added cluster-wide: <br>'+cmd_install)

            else:

                procExe = subprocess.Popen('echo "*** Installing the following modules: '+cmd_install+' ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('yum -y --enablerepo=ndeploy install '+cmd_install+' >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('echo "*** The following modules have been installed: '+cmd_install+' ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()

                commoninclude.print_success('The following modules have been added: <br>'+cmd_install)

        else:
            if os.path.isfile(cluster_config_file):

                procExe = subprocess.Popen('echo "*** Uninstalling the following modules cluster-wide: '+cmd_uninstall+' ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('yum -y remove '+cmd_uninstall+' && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y remove '+cmd_uninstall+'\" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('echo "*** Installing the following modules cluster-wide: '+cmd_install+' ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('yum -y --enablerepo=ndeploy install '+cmd_install+' && ansible -i /opt/nDeploy/conf/nDeploy-cluster/hosts ndeployslaves -m shell -a \"yum -y --enablerepo=ndeploy install '+cmd_install+'\" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()

                commoninclude.print_success('The following modules have been added cluster-wide: <br>'+cmd_install+'<br>The following modules have been removed cluster-wide: <br>'+cmd_uninstall)

            else:

                procExe = subprocess.Popen('echo "*** Uninstalling the following modules: '+cmd_uninstall+' ***" > '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('yum -y remove '+cmd_uninstall+' >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('echo "*** Installing the following modules cluster-wide: '+cmd_install+' ***" >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()
                procExe = subprocess.Popen('yum -y --enablerepo=ndeploy install '+cmd_install+' >> '+whm_terminal_log, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                procExe.wait()

                commoninclude.print_success('The following modules have been added: <br>'+cmd_install+'<br>The following modules have been removed: <br>'+cmd_uninstall)

    else:
        commoninclude.print_warning('Nothing to do.')

else:
    commoninclude.print_forbidden()

print('    </body>')
print('</html>')
