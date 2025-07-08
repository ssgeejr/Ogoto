import os

class Saturn:
    def __init__(self, folder='.ogoto', filename='ogoto.cfg'):
        self.config = {}
        home_directory = os.path.expanduser('~')
        file_path = os.path.join(home_directory, folder, filename)

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Configuration file not found: {file_path}")

        with open(file_path, 'r') as f:
            contents = f.read()

        for line in contents.splitlines():
            if '~' not in line:
                continue  # Skip malformed lines
            key, value = line.split('~', 1)
            self.config[key.strip()] = value.strip()

    # ANY
    def get_value(self, key):
        return self.config.get(key)

    # MYSQL
    def get_dbhost(self):
        return self.config.get('DBHOST')

    def get_db(self):
        return self.config.get('DB')

    def get_db_uname(self):
        return self.config.get('DBUNAME')

    def get_db_pword(self):
        return self.config.get('DBPWORD')

    # JIRA
    def get_api_key(self):
        return self.config.get('APIKEY')

    def get_user_id(self):
        return self.config.get('USERID')

    def get_assign_to(self):
        return self.config.get('ASSIGN_TO')

    def get_company_id(self):
        return self.config.get('COMPANYID')

    def get_jira_url(self):
        company_id = self.get_company_id()
        return f'https://{company_id}.atlassian.net' if company_id else None
