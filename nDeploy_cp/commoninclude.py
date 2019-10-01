#!/usr/bin/env python

import os
import yaml
import socket


installation_path = "/opt/nDeploy"  # Absolute Installation Path
ndeploy_control_file = installation_path+"/conf/ndeploy_control.yaml"
branding_file = installation_path+"/conf/branding.yaml"
cluster_config_file = installation_path+"/conf/ndeploy_cluster.yaml"
homedir_config_file = installation_path+"/conf/nDeploy-cluster/group_vars/all"
autom8n_version_info_file = installation_path+"/conf/version.yaml"
nginx_version_info_file = "/etc/nginx/version.yaml"


# nDeploy Control
if os.path.isfile(ndeploy_control_file):
    with open(ndeploy_control_file, 'r') as ndeploy_control_data_file:
        yaml_parsed_ndeploy_control_settings = yaml.safe_load(ndeploy_control_data_file)
    ndeploy_theme_color = yaml_parsed_ndeploy_control_settings.get("ndeploy_theme_color", "light")
    primary_color = yaml_parsed_ndeploy_control_settings.get("primary_color", "#121212")
    logo_url = yaml_parsed_ndeploy_control_settings.get("logo_url", "None")
    app_email = yaml_parsed_ndeploy_control_settings.get("app_email", "None")
else:
    ndeploy_theme_color = "light"
    primary_color = "#121212"
    logo_url = "None"
    app_email = "None"

# Branding Support
if os.path.isfile(branding_file):
    with open(branding_file, 'r') as brand_data_file:
        yaml_parsed_brand = yaml.safe_load(brand_data_file)
    brand_logo = yaml_parsed_brand.get("brand_logo", "xtendweb.png")
    brand = yaml_parsed_brand.get("brand", "AUTOM8N")
    brand_group = yaml_parsed_brand.get("brand_group", "NGINX AUTOMATION")
    brand_anchor = yaml_parsed_brand.get("brand_anchor", "A U T O M 8 N")
    brand_link = yaml_parsed_brand.get("brand_link", "https://autom8n.com/")
else:
    brand_logo = "xtendweb.png"
    brand = "AUTOM8N"
    brand_group = "NGINX AUTOMATION"
    brand_anchor = "A U T O M 8 N"
    brand_link = "https://autom8n.com/"


# Get version of Nginx and plugin
with open(autom8n_version_info_file, 'r') as autom8n_version_info_yaml:
    autom8n_version_info_yaml_parsed = yaml.safe_load(autom8n_version_info_yaml)

# Bypass Cloudlinux perms
if os.access(nginx_version_info_file, os.R_OK): # Check for read access
    with open(nginx_version_info_file, 'r') as nginx_version_info_yaml:
        nginx_version_info_yaml_parsed = yaml.safe_load(nginx_version_info_yaml)
    nginx_version = nginx_version_info_yaml_parsed.get('nginx_version')
else:
    nginx_version = ""
autom8n_version = autom8n_version_info_yaml_parsed.get('autom8n_version')


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


def return_label(theoption, hint):
    result = '<div class="d-flex w-50 justify-content-end align-items-center" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result


def return_prepend(theoption, hint):
    result = '<div class="d-flex w-50 align-items-center" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result

def return_sys_tip(theoption, hint):
    result = '<div class="col-md-6 alert" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result


def print_nontoast_error(thenotice, thereason):
    print('            <div class="row justify-content-center">')
    print('                <div class="col-lg-6 alert alert-danger">')
    print('                    <div class="text-center">')
    print('                        <i class="fa fa-exclamation"></i>')
    print('                        <h3>'+thenotice+'</h3>')
    print('                        <h5>'+thereason+'</h5>')
    if app_email != 'None':
        print('                        <p>Please contact <a href="mailto:'+app_email+'">'+app_email+'</a> if you need assistance.</p>')
    print('                    </div>')
    print('                </div>')
    print('            </div>')
    print_footer()
    print('        </div> <!-- Main Container End -->')
    print('')
    print('    <!-- Body End -->')
    print('    </body>')
    print('</html>')


def print_forbidden():
    print('<i class="fas fa-exclamation"></i><p>Forbidden</p>')


def print_error(themessage):
    print('<i class="fas fa-exclamation"></i><p>'+themessage+'</p>')


def print_success(themessage):
    print('<i class="fas fa-thumbs-up"></i><p>'+themessage+'</p>')


def print_success_alert(themessage):
    print('<div class="alert alert-success">'+themessage+'</div>')


def print_error_alert(themessage):
    print('<div class="alert alert-danger text-left">'+themessage+'</div>')


def print_sys_tip(theoption, hint):
    print('<div class="col-md-6 alert" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>')


def print_disabled():
    print('                                <div class="col-md-6">')
    if app_email != 'None':
        print('                                    <div class="btn btn-light btn-block btn-not-installed" data-toggle="tooltip" title=" An additional '+brand+' module is required for this functionality. Contact '+app_email+' if you need assistance with this. ">Not Installed</div>')
    else:
        print('                                    <div class="btn btn-light btn-block btn-not-installed" data-toggle="tooltip" title=" An additional '+brand+' module is required for this functionality. ">Not Installed</div>')
    print('                                </div>')


def print_forbidden_wrapper():
    print('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>Forbidden</p></div></div>')


def print_error_wrapper(themessage):
    print('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body"><i class="fas fa-exclamation"></i><p>'+themessage+'</p></div></div>')


def print_success_wrapper(themessage):
    print('<div class="card"><div class="card-header"><h5 class="card-title mb-0"><i class="fas fa-terminal float-right"></i> Command Output</h5></div><div class="card-body text-center"><i class="fas fa-thumbs-up"></i><p>'+themessage+'</p></div></div>')


def return_multi_input(theoption, hint):
    result = '<div class="label label-default" data-toggle="tooltip" title="'+hint+'">'+theoption+'</div>'
    return result


def print_loader():
    print('')
    print('        <div id="loader"><i class="fas fa-infinity fa-spin"></i></div>')
    print('')


# Print Header
def print_header(title=''):
    print('Content-Type: text/html')
    print('')
    print('<!doctype html>')
    print('<html lang="en">')
    print('    <head>')
    print('        <!-- Required meta tags -->')
    print('        <meta charset="utf-8">')
    print('        <meta name="viewport" content="width=device-width, initial-scale=1">')
    print('        <title>'+brand+' - '+title+'</title>')
    print('        <script src="https://code.jquery.com/jquery-3.4.1.min.js" integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo=" crossorigin="anonymous"></script>')
    print('        <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>')
    print('        <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>')
    print('        <link href="https://fonts.googleapis.com/css?family=Poppins&display=swap" rel="stylesheet">')
    print('        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.8.1/css/all.min.css" rel="stylesheet">')
    print('        <script src="js.js"></script>')
    print('        <link rel="stylesheet" href="styles.css">')
    print('    </head>')
    print('')
    print('    <!-- Body Start -->')
    print('    <body class="ndeploy-theme-'+ndeploy_theme_color+'">')
    print('        <header id="main-header" class="d-flex justify-content-between align-items-center">')
    print('            <div class="logo">')
    print('                <h4>')
    if logo_url != 'None':
        print('                    <a href="xtendweb.live.py"><img border="0" src="'+logo_url+'"></a>')
    else:
        print('                    <a href="xtendweb.live.py"><img border="0" src="'+brand_logo+'" width="48" height="48"></a>'+brand)
    print('                </h4>')
    print('            </div>')
    print('            <div class="d-flex">')
    if app_email != 'None':
        print('                <div class="buttons p-2"><a class="btn btn-'+ndeploy_theme_color+'" href="mailto:'+app_email+'"><i class="fas fa-envelope"></i> Support </a></div>')
    print('                <div class="buttons p-2"><a class="btn btn-'+ndeploy_theme_color+'" target="_blank" href="help.txt"><i class="fas fa-book-open"></i> Documentation </a></div>')
    print('            </div>')
    print('        </header>')
    print('')
    print('        <!-- Main Container Start -->')
    print('        <div id="main-container" class="container">') #Main Container


# Print Footer
def print_footer():
    print('')
    print('            <!-- Footer Start -->')
    print('            <div id="footer" class="container text-center mt-2 mb-5">')
    print('                <a style="color:'+primary_color+'" href="'+brand_link+'" target="_blank">'+brand_anchor+'</a>')
    if ndeploy_theme_color == 'light':
        print('            <p class="text-dark small">We are running '+brand+' version '+autom8n_version.replace("Autom8n ",'')+' on '+nginx_version+'.</p>')
    if ndeploy_theme_color == 'dark':
        print('            <p class="text-light small">We are running '+brand+' version '+autom8n_version.replace("Autom8n ",'')+' on '+nginx_version+'.</p>')
    print('            </div>')
    print('')


# Card Start
def cardheader(header='Untitled Card', faicon='fas fa-cogs'):
    print('')
    print('                    <!-- Bootstrap Card Start for '+header+' -->')
    if ndeploy_theme_color == 'dark':
        print('                    <div class="card mb-4 text-white bg-'+ndeploy_theme_color+'">')
    if ndeploy_theme_color == 'light':
        print('                    <div class="card mb-4 text-dark bg-'+ndeploy_theme_color+'">')
    if header != '':
        print('                        <div class="card-header">')
        print('                            <h5 class="card-title mb-0"><i class="'+faicon+' float-right"></i>'+header+'</h5>')
        print('                        </div>')
    print('')


# Card Footer
def cardfooter(text='Unmodified Footer Text'):
    if text != '':
        print('')
        print('                        <!-- Card Footer Start -->')
        print('                        <div class="card-footer">')
        print('                            <small><center>'+text+'</center></small>')
        print('                        </div>')
    print('')
    print('                    <!-- Bootstrap Card End -->')
    print('                    </div>')
    print('')


# Breadcrumbs
def bcrumb(pagename="Unnamed Page", active_fa_icon="fas fa-infinity"):
    print('')
    print('            <!-- Navigation -->')
    print('            <nav aria-label="breadcrumb">')
    print('                <ol class="breadcrumb justify-content-md-center">')
    if pagename != 'Home':
        print('                    <li class="breadcrumb-item"><a href="xtendweb.live.py"><i class="fas fa-infinity"></i>&nbsp;Home</a></li>')
        print('                    <li style="color:'+primary_color+'" class="breadcrumb-item active" aria-current="page"><i class="'+active_fa_icon+'"></i>&nbsp;'+pagename+'</li>')
    else:
        print('                    <li class="breadcrumb-item active" aria-current="page"><a style="color:'+primary_color+' !important;" href="xtendweb.live.py"><i class="fas fa-infinity"></i>&nbsp;Home</a></li>')
    print('                </ol>')
    print('            </nav>')
    print('')


def print_modals():

    # Modal
    print('        <div class="modal fade" id="myModal" tabindex="-1" role="dialog">')
    print('            <div class="modal-dialog modal-dialog-centered" role="document">')
    print('                <div class="modal-content">')
    print('                    <div class="modal-header">')
    print('                        <h4 class="modal-title">Command Output</h4>')
    print('                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">')
    print('                            <span aria-hidden="true">&times;</span>')
    print('                        </button>')
    print('                    </div>')
    print('                    <div class="modal-body">')
    print('                    </div>')
    print('                    <div class="modal-footer">')
    print('                        <button type="button" class="btn btn-outline-secondary" data-dismiss="modal">Close</button>')
    print('                    </div>')
    print('                </div>')
    print('            </div>')
    print('        </div>')

    # Modal with no reload
    print('        <div class="modal fade" id="myModal-nl" tabindex="-1" role="dialog"> ')
    print('            <div class="modal-dialog modal-xl modal-dialog-centered" role="document">')
    print('                <div class="modal-content">')
    print('                    <div class="modal-header">')
    print('                        <h4 class="modal-title">Command Output</h4>')
    print('                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">')
    print('                            <span aria-hidden="true">&times;</span>')
    print('                        </button>')
    print('                    </div>')
    print('                    <div class="modal-body">')
    print('                    </div>')
    print('                    <div class="modal-footer">')
    print('                        <button type="button" class="btn btn-outline-secondary" data-dismiss="modal">Close</button>')
    print('                    </div>')
    print('                </div>')
    print('            </div>')
    print('        </div>')

    # Modal Large Width
    print('        <div class="modal fade" id="myModal-xl" tabindex="-1" role="dialog">')
    print('            <div class="modal-dialog modal-xl modal-dialog-centered" role="document">')
    print('                <div class="modal-content">')
    print('                    <div class="modal-header">')
    print('                        <h4 class="modal-title">Command Output</h4>')
    print('                        <button type="button" class="close" data-dismiss="modal" aria-label="Close">')
    print('                            <span aria-hidden="true">&times;</span>')
    print('                        </button>')
    print('                    </div>')
    print('                    <div class="modal-body">')
    print('                    </div>')
    print('                    <div class="modal-footer">')
    print('                        <button type="button" class="btn btn-outline-secondary" data-dismiss="modal">Close</button>')
    print('                    </div>')
    print('                </div>')
    print('            </div>')
    print('        </div>')

    # Toast
    print('        <div class="toast fade hide" id="myToast" role="alert" aria-live="assertive" aria-atomic="true">')
    print('            <div class="toast-header">')
    print('                <strong class="mr-auto">Command Output</strong>')
    print('                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                    <span aria-hidden="true">&times;</span>')
    print('                </button>')
    print('            </div>')
    print('            <div class="toast-body">')
    print('            </div>')
    print('        </div>')

    # Toast with long autohide
    print('        <div class="toast fade hide" id="myToastnohide" role="alert" aria-live="assertive" aria-atomic="true" data-delay="5000">')
    print('            <div class="toast-header">')
    print('                <strong class="mr-auto">Command Output</strong>')
    print('                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                    <span aria-hidden="true">&times;</span>')
    print('                </button>')
    print('            </div>')
    print('            <div class="toast-body">')
    print('            </div>')
    print('        </div>')

    # Toast with no reload
    print('        <div class="toast fade hide" id="myToast-nl" role="alert" aria-live="assertive" aria-atomic="true">')
    print('            <div class="toast-header">')
    print('                <strong class="mr-auto">Command Output</strong>')
    print('                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                    <span aria-hidden="true">&times;</span>')
    print('                </button>')
    print('            </div>')
    print('            <div class="toast-body">')
    print('            </div>')
    print('        </div>')

    # Toastback
    print('        <div class="toast fade hide" id="myToastback" role="alert" aria-live="assertive" aria-atomic="true">')
    print('            <div class="toast-header">')
    print('                <strong class="mr-auto">Command Output</strong>')
    print('                <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">')
    print('                    <span aria-hidden="true">&times;</span>')
    print('                </button>')
    print('            </div>')
    print('            <div class="toast-body">')
    print('            </div>')
    print('        </div>')
