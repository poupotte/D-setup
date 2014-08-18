from fabric.api import env, sudo, run, cd
from fabtools import require
from termcolor import colored
from fabtools.require import file as require_file
from fabric.context_managers import hide

'''
Utilities to manage digidisk trough ssh
'''

# domain should be domain='toto.digidisk.fr'
# fab -H testeur-0X.digidisk.fr:17224 function:arg1,arg2
# fab -H testeur-0X.digidisk.fr:17224 set_domain:testeur-0X.digidisk.fr

env.user = 'cubie'

## Configuration

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

def set_gitlab_ids(username, password):
    require.files.file(
        path='/etc/cozy/gitlab.login',
        contents=username + '\n' + password,
        use_sudo=True,
        owner='root',
        mode='700'
    )

def install_imagemagick():
    """ TODOS :
        check if works on cubie
    """
    deb.update_index()
    deb.upgrade()
    require.deb.packages([
        'imagemagick'
    ])


## Installation

def install_proxy():
    result = sudo('cozy-monitor install proxy')
    result = result.find('successfully installed')
    if result == -1:
        print colored('Proxy updating failed', 'red')
    else:

        print colored('Proxy successfully installed', 'green')

def install_home():
    result = sudo('cozy-monitor install home')
    result = result.find('successfully installed')
    if result == -1:
        print colored('Home updating failed', 'red')
    else:
        print colored('Home successfully installed', 'green')

def install_data_system():
    result = sudo('cozy-monitor install data-system')
    result = result.find('successfully installed')
    if result == -1:
        print colored('Data-system updating failed', 'red')
    else:
        print colored('Data-system successfully installed', 'green')

def install_photo():
    result = sudo('cozy-monitor install photos')
    result = result.find('successfully installed')
    if result == -1:
        print colored('Photo updating failed', 'red')
    else:
        print colored('Photo successfully installed', 'green')

def install_contacts():
    result = sudo('cozy-monitor install contacts')
    result = result.find('successfully installed')
    if result == -1:
        print colored('Contact updating failed', 'red')
    else:
        print colored('Contact successfully installed', 'green')

def install_stack():
    result = sudo('cozy-monitor install proxy')
    result = result.find('successfully installed')
    if result == -1:
        print colored('Proxy installing failed', 'red')
    else:
        result = sudo('cozy-monitor install home')
        result = result.find('successfully installed')
        if result == -1:
            print colored('Home installing failed', 'red')
        else:
            result = sudo('cozy-monitor install data-system')
            result = result.find('successfully installed')
            if result == -1:
                print colored('Data-system installing failed', 'red')
            else:
                print colored('Stack successfully installed', 'green')


## Update

def update_proxy(branch):
    result = sudo('cozy-monitor update proxy %s' %branch )
    result = result.find('successfully updated')
    if result == -1:
        print colored('Proxy updating failed', 'red')
    else:
        print colored('Proxy successfully updated', 'green')

def update_home(branch):
    result = sudo('cozy-monitor update home %s' %branch )
    result = result.find('successfully updated')
    if result == -1:
        print colored('Home updating failed', 'red')
    else:
        print colored('Home successfully updated', 'green')

def update_data_system(branch):
    result = sudo('cozy-monitor update data-system %s' %branch )
    result = result.find('successfully updated')
    if result == -1:
        print colored('Data-system updating failed', 'red')
    else:
        print colored('Data-system successfully updated', 'green')

def update_photos(branch):
    result = sudo('cozy-monitor update photos %s' %branch )
    result = result.find('successfully updated')
    if result == -1:
        print colored('Photo updating failed', 'red')
    else:
        print colored('Photo successfully updated', 'green')

def update_contacts(branch):
    result = sudo('cozy-monitor update contacts %s' %branch )
    result = result.find('successfully updated')
    if result == -1:
        print colored('Contact updating failed', 'red')
    else:
        print colored('Contact successfully updated', 'green')

def update_stack_master():
    result = sudo('cozy-monitor update proxy master')
    result = result.find('successfully updated')
    if result == -1:
        print colored('Proxy updating failed', 'red')
    else:
        result = sudo('cozy-monitor update home master')
        result = result.find('successfully updated')
        if result == -1:
            print colored('Home updating failed', 'red')
        else:
            result = sudo('cozy-monitor update data-system master')
            result = result.find('successfully updated')
            if result == -1:
                print colored('Data-system updating failed', 'red')
            else:
                print colored('Stack successfully updated', 'green')

def update_version_contacts(username, password):
    # Update monitor
    with cd('/usr/local/lib/node_modules'):
        sudo('rm -rf cozy-monitor')
        sudo('git clone https://github.com/poupotte/cozy-monitor.git')
        with cd('/usr/local/lib/node_modules/cozy-monitor'):
            sudo('git checkout -b feature/without-home origin/feature/without-home')
            sudo('npm install')
    # Create file for gitlab login
    set_gitlab_ids(username, password)
    # Update data-system
    sudo('cozy-monitor install data-system -b feature/contacts')
    # Update home
    sudo('cozy-monitor install home -b feature/contacts')
    # Update proxy
    sudo('cozy-monitor install proxy -b feature/contacts')
    # Install contacts
    sudo('cozy-monitor install contacts')
    # Restart all apps
    sudo('cozy-monitor restart data-system')
    sudo('cozy-monitor restart home')
    sudo('cozy-monitor restart proxy')
    sudo('cozy-monitor restart contacts')
    # Check Contacts    
    with hide('running', 'stdout'):
        result = run('curl http://localhost:9114')    
    result = result.find('Digidisk - Contacts')
    if result == -1:
        print colored('Contact installing failed', 'red')
    else:
        print colored('Stack successfully updated', 'green')

def update_version_photos(username, password):
    # Update monitor
    sudo('ntpdate ntp.ovh.net')
    with cd('/usr/local/lib/node_modules'):
        sudo('rm -rf cozy-monitor')
        sudo('git clone https://github.com/poupotte/cozy-monitor.git')
        with cd('/usr/local/lib/node_modules/cozy-monitor'):
            sudo('git checkout -b feature/without-home origin/feature/without-home')
            sudo('npm install')
    # Create file for gitlab login
    set_gitlab_ids(username, password)
    # Update data-system
    sudo('cozy-monitor install data-system -b feature/photos')
    # Update home
    sudo('cozy-monitor install home -b feature/photos')
    # Update proxy
    sudo('cozy-monitor install proxy -b feature/contacts')
    # Install contacts
    sudo('cozy-monitor install contacts -b photos')
    # Install photos
    sudo('cozy-monitor install photos -b feature/photos')
    # Restart all apps
    sudo('cozy-monitor restart data-system')
    sudo('cozy-monitor restart home')
    sudo('cozy-monitor restart proxy')
    sudo('cozy-monitor restart contacts')
    sudo('cozy-monitor restart photos')
    # Check Contacts
    with hide('running', 'stdout'):
        result = run('curl http://localhost:9114')
    result = result.find('Digidisk - Contacts')
    if result == -1:
        print colored('Contact installing failed', 'red')
    else:
        # Check Photos
        with hide('running', 'stdout'):
            result = run('curl http://localhost:9119')
        result = result.find('Digidisk - Photos')
        if result == -1:
            print colored('Photo installing failed', 'red')
        else:
            run('cozy-monitor status')
            print colored('Stack successfully updated', 'green')
    