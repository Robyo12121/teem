import os
import configparser


class CustomConfigParser():

    def __init__(self):
        self.home = os.environ['HOME']
        self.config_path = f"{self.home}\\.teem\\"
        self.files = {
            'creds_file': f"{self.home}\\.teem\\credentials.ini",
            'config_file': f"{self.home}\\.teem\\config.ini"
            }
        self.data = ['teem_username', 'teem_password', 'teem_access_key_id', 'teem_secret_access_key']
        self._parser = configparser.ConfigParser()

    def write_file(self, data_dict, file):
        self._parser['default'] = data_dict
        with open(file, 'w') as data:
            self._parser.write(data)
        return

    def get_data(self, file):
        self._parser.read(file)
        data = {}
        try:
            for key in self._parser['default']:
                data[key] = self._parser['default'][key]
        except KeyError as k_err:
            print("file empty")
        return data


if __name__ == '__main__':
    cred = CustomConfigParser()
    data = cred.get_data(cred.files['creds_file'])
    print(data)
