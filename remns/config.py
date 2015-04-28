import yaml

with open('config.yaml', 'r') as config_file:
    config_data = yaml.load(config_file)

USER=config_data['admin']['username']
PASSWORD=config_data['admin']['password']
FULLNAME=config_data['admin']['author']
DB_CONN_STRING="{engine}+{driver}://{user}:{password}@{host}/{name}".format(**(config_data['db']))
ADMIN_TEMPLATES_PATH='templates/admin'
TEMPLATES_PATH='templates'
