'URL configuration'
# Import pylons modules
from routes import Mapper


def make_map(config):
    'Create, configure and return the routes mapper'
    # Initialize map
    map = Mapper(directory=config['pylons.paths']['controllers'], always_scan=config['debug'])
    map.minimization = False
    map.explicit = False
    # Remove trailing slash
    map.redirect('/{controller}/', '/{controller}')
    # Map errors
    map.connect('/errors/{action}', controller='errors')
    map.connect('/errors/{action}/{id}', controller='errors')
    # Map people
    map.connect('person_index', '/people', controller='people', action='index')
    map.connect('person_register', '/people/register', controller='people', action='register')
    map.connect('person_register_', '/people/register_', controller='people', action='register_')
    map.connect('person_confirm', '/people/confirm/{ticket}', controller='people', action='confirm')
    map.connect('person_login', '/people/login/{targetURL}', controller='people', action='login')
    map.connect('person_login_plain', '/people/login', controller='people', action='login')
    map.connect('person_login_', '/people/login_', controller='people', action='login_')
    map.connect('person_update', '/people/update', controller='people', action='update')
    map.connect('person_update_', '/people/update_', controller='people', action='update_')
    map.connect('person_logout_plain', '/people/logout', controller='people', action='logout') 
    map.connect('person_logout', '/people/logout/{targetURL}', controller='people', action='logout')
    map.connect('person_reset', '/people/reset', controller='people', action='reset')
    # Map jobs
    map.connect('job_index', '/jobs', controller='jobs', action='index')
    map.connect('job_register', '/jobs/register', controller='jobs', action='register')
    map.connect('job_register_', '/jobs/register_', controller='jobs', action='register_')
    map.connect('job_show', '/jobs/{jobID}', controller='jobs', action='show')
    # Redirect index
    map.redirect('/', '/jobs')
    # Return
    return map
