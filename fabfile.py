from fabric.api import env, sudo

# domain should be domain='toto.digidisk.fr'
# fab -H testeur-0X.digidisk.fr:17224 function:arg1,arg2

env.user = 'cubie'

def update_1(domain):
    regenerate_public_certificate(domain)
    set_domain(domain)
    update_home()



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
    print('CSR generated and self-signed for %s' % domain)



def set_domain(domain):    
    with cd('/usr/local/cozy/apps/home/home/digidisk-files/'):
        sudo('coffee commands setdomain %s' % domain, user='cozy')
    print('Domain set to: %s' % domain)


def update_home():    
    sudo('cozy-monitor uninstall home')
    result = sudo('cozy-monitor install home -r https://github.com/poupotte/digidisk-files.git')
    result = result.find('successfully updated')
    if result == -1:
        print(red('Home updating failed'))
    else:
        print(green('Home successfully updated'))
