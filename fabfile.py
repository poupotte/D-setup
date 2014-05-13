

#domain should be domain='toto.digidisk.fr'

@task
def update_1(domain):
    update_certificate(domain)
    update_domain(domain)
    update_home()

@task
def regenerate_public_certificate(domain):
    with cd('/etc/cozy/'):
        sudo("openssl req -new -key server.key -out server.csr -subj '/CN=%s/O=Internet Widgits Pty Ltd/ST=Some-State/C=AU'" %domain)
        sudo('openssl x509 -req -days 3650 -in server.csr -signkey server.key -out server.crt')
        sudo('rm server.csr')
        sudo('chown root:root server.key; chmod 440 server.key')
        sudo('chown root:root server.crt; chmod 440 server.crt')
        sudo('service nginx reload')
    print(green('CSR generated and self-signed for %s' % domain))


@task
def update_domain(domain):    
    with cd('/usr/local/cozy/apps/home/home/digidisk-files/'):
        cozydo('coffee commands setdomain %s' % domain)
    print(green('Domain set to: %s' % domain))

@task
def update_home():    
    sudo('cozy-monitor uninstall home')
    result = sudo('cozy-monitor install home -r https://github.com/poupotte/digidisk-files.git')
    result = result.find('successfully updated')
    if result == -1:
        print(red('Home updating failed'))
    else:
        print(green('Home successfully updated'))
