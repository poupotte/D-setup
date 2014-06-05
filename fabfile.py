from fabric.api import env, sudo, cd

from termcolor import colored

'''
Utilities to manage digidisk trough ssh
'''

# domain should be domain='toto.digidisk.fr'
# fab -H testeur-0X.digidisk.fr:17224 function:arg1,arg2
# fab -H testeur-0X.digidisk.fr:17224 set_domain:testeur-0X.digidisk.fr

env.user = 'cubie'

def update_1(domain):
    regenerate_public_certificate(domain)
    set_domain(domain)
    first_update_proxy()



def regenerate_public_certificate(domain):
    '''
    Create a new CSR from the same key
    Self signed the csr with the key
    Reload Nginx
    '''
    with cd('/etc/cozy/'):
        sudo("openssl req -new -key server.key -out server.csr -subj '/CN=%s/O=Internet Widgits Pty Ltd/ST=Some-State/C=AU'" %domain)
        sudo('openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt')
        sudo('rm server.csr')
        sudo('chown root:root server.key; chmod 440 server.key')
        sudo('chown root:root server.crt; chmod 440 server.crt')
        sudo('service nginx reload')
    print colored('CSR generated and self-signed for %s' % domain, 'green')



def set_domain(domain):    
    with cd('/usr/local/cozy/apps/home/home/digidisk-files/'):
        sudo('coffee commands.coffee setdomain %s' % domain, user='cozy')
    print colored('Domain set to: %s' % domain, 'green')


def first_update_proxy():
    result = sudo('cozy-monitor install proxy -r https://gitlab.cozycloud.cc/cozy/digidisk-proxy.git')
    result = result.find('successfully installed')
    if result == -1:
        print colored('Proxy updating failed', 'red')
    else:

        print colored('Proxy successfully updated', 'green')





def whereami():
    sudo('uname -a')
    sudo('hostname')



def first_update_home():
    result = sudo('cozy-monitor install home -r https://gitlab.cozycloud.cc/cozy/digidisk-files.git')
    result = result.find('successfully installed')
    if result == -1:
        print colored('Home updating failed', 'red')
    else:
        print colored('Home successfully updated', 'green')

def first_update_data_system():
    result = sudo('cozy-monitor install data-system -r https://gitlab.cozycloud.cc/cozy/digidisk-data-system.git')
    result = result.find('successfully installed')
    if result == -1:
        print colored('Data-system updating failed', 'red')
    else:
        print colored('Data-system successfully updated', 'green')

def update_proxy():
    result = sudo('cozy-monitor update proxy https://gitlab.cozycloud.cc/cozy/digidisk-proxy.git')
    result = result.find('successfully updated')
    if result == -1:
        print colored('Proxy updating failed', 'red')
    else:
        print colored('Proxy successfully updated', 'green')

def update_home():
    result = sudo('cozy-monitor update home https://gitlab.cozycloud.cc/cozy/digidisk-files.git')
    result = result.find('successfully updated')
    if result == -1:
        print colored('Home updating failed', 'red')
    else:
        print colored('Home successfully updated', 'green')

def update_data_system():
    result = sudo('cozy-monitor update data-system https://gitlab.cozycloud.cc/cozy/digidisk-data-system.git')
    result = result.find('successfully updated')
    if result == -1:
        print colored('Data-system updating failed', 'red')
    else:
        print colored('Data-system successfully updated', 'green')

