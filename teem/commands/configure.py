import os
from .base import Base
import copy
import configparser


class configure(Base):
    """
    AWS configure operation:
        'aws configure'
    >>>AWS Access Key ID [**************L2MQ]:
    >>>AWS Secret Access Key [****************v0z9]:
    >>>Default region name [eu-central-1]:
    >>>Default output format [text]:
    exit

    Shows current setting in prompt (with keys mostly omitted for security.
    Entering nothing keeps the current setting.

    Making a request attempts to use the access keys even if they are incorrect.

    Teem configure operation:
        'py cli.py configure'
                           
    >>>Teem Access Key ID [**************1vRt]:
    >>>Teem Secret Access Key [****************cp96]:
    >>>Teem other settings [current-setting]:
    >>> *   *   *   *   *  *  * :
    exit
    """
    home = os.environ['HOME']
    config_path = f"{home}\\.teem\\"
    files = {'creds_file': f"{home}\\.teem\\credentials.ini",
             'config_file': f"{home}\\.teem\\config.ini"
             }
    data = ['teem_username', 'teem_password', 'teem_access_key_id', 'teem_secret_access_key']
    parser = configparser.ConfigParser()
    
    def get_user_input(self):
        user_input = {}
        current = {**self.get_data(self, self.files['config_file']),                   
                   **self.get_data(self, self.files['creds_file'])}

        # Obscure secret info
        scrubbed = copy.deepcopy(current)
        for item in self.data:
            if item in ['teem_access_key_id', 'teem_secret_access_key', 'teem_password']:
                try:
                    scrubbed[item] = self.scrub(self, current[item])
                except KeyError as k_err:
                    pass # Log 

        # Get info from user
        for item in self.data:
            try:
                user_input[item] = str(input(f"{self.pretty(self, item)} [{scrubbed[item]}]: "))
            except:
                user_input[item] = str(input(f"{self.pretty(self, item)}: "))

        # If no user input, put original value back into file
        for k, v in user_input.items():
            if v is '':
                try:
                    user_input[k] = current[k]
                except KeyError as k_err:
                    print(f"{k} doesn't exist")
                    
        return user_input

    def set_info(self, some_dict):
        """Write info contained in user_input to the creds.ini file or
            config file.
            1) If access key id or secret access key then write it to credentials file
            2) Otherwise write it to config file
        """
        teem_creds = ('teem_access_key_id', 'teem_secret_access_key')
        creds = {k: some_dict[k] for k in teem_creds}
        self.write_file(self, creds, self.files['creds_file'])

        other = {k: some_dict[k] for k in some_dict if k not in teem_creds}
        self.write_file(self, other, self.files['config_file'])

    def write_file(self, data_dict, file):
        self.parser['default'] = data_dict
        with open(file, 'w') as data:
            self.parser.write(data)
        return
        
    def get_data(self, file):
        self.parser.read(file)
        data = {}
        try:
            for key in self.parser['default']:
                data[key] = self.parser['default'][key]
        except KeyError as k_err:
            print("file empty")
        return data
    
    def no_input(somedict):
        for element in somedict:
            if not element == '':
                return False
        return True

    def scrub(self, string):
        last4 = string[-4:]
        stars = '*'*14
        return stars + last4
        
    def settings_exist(self):
        print("Checking if config and credentials file exist")
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)
        for file, path in self.files.items():
            if not os.path.exists(path):
                f = open(path, 'w').close()

    def run(self, some_dict):
        self.settings_exist(self)
        user_input = self.get_user_input(self)
        if not self.no_input(user_input.values()):
            self.set_info(self, user_input)

    def pretty(self, string):
        """Take string of the form: some_string_of_some_length
            and return it in the form Some String Of Some Length
        """
        lis = string.split('_')
        new = []
        for item in lis:
            new.append(item.capitalize())
        
        return ' '.join(new)


if __name__ == '__main__':
    conf = configure()
    print(conf.pretty('teem_username'))
    print(conf.pretty('teem_access_key_id'))
    
    
