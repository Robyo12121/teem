import argparse
import os
from json import dumps
from .base import Base

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
                           ************************************
    >>>Teem Access Key ID [**************1vRt]:
    >>>Teem Secret Access Key [****************cp96]:
    >>>Teem other settings [current-setting]:
    >>> *   *   *   *   *  *  * :
    exit

    input function:
        0) Make sure files and folders exist
        1) Get input from user, None for values not entered
        2) If all Nones, do nothing.
        3) If any not Nones, read file, write values
        4) Don't bother with error checking of access keys and secret keys
        5) Some error checking on other values that are easier
    
    """
    home = os.environ['HOME']
    config_path = f"{home}\\.teem\\"
    creds = f"{home}\\.teem\\credentials.ini"
    config = f"{home}\\.teem\\config"
    parser = configparser.ConfigParser()
    
    def get_info(self):
        # 0) check if .teem exits, if .teem/config and .teem/credentials exist
        # 0.5) check if 'teem_access_key' = <something>
        # 0.6) check if 'teem_secret_key' = <something>
        # 1) If first time usage of configure (ie credentials file is empty)
        #       get credentials and settings from user
        # 2) Make .teem file with 'config' and 'credentials' files
        # 3) Set credentials and settings from user in those files
        user_input = {}
        current_creds = self.load_info(self)
        for key, value in current_creds.items():
            if key in ['teem_access_key_id', 'teem_secret_access_key']:
                current_creds[key] = self.scrub(self, value)
        try:
            user_input['username'] = str(input(f"Teem Username [{current_creds['username']}: "))
        except:
            pass
        try:
            user_input['password'] = str(input(f"Teem Password [{current_creds['password']}]: "))
        except:
            pass
        try:
            user_input['access_key'] = str(input(f"Access key [{current_creds['teem_access_key_id']}]: "))
        except:
            pass
        try:
            user_input['secret_key'] = str(input(f"Secret key [{current_creds['teem_secret_access_key']}]: "))
        except:
            pass
        print(user_input)

        if not None in user_input.values():
            #Call set_info function here
            print("Calling 'set_info' to write to creds")
        return

    def load_info(self):
        self.parser.read(self.creds)
        creds = {}
        for key in self.parser['default']:
            creds[key] = self.parser['default'][key]
        return creds

    def scrub(self, string):
        last4 = string[-4:]
        stars = '*'*14
        
        return stars + last4
        
    def settings_files(self):
        if not os.path.exists(self.config_path):
            os.makedirs(self.config_path)
        if not os.path.exists(self.creds):
            creds_f = open(self.creds, 'w').close()
        if not os.path.exists(self.config):
            config_f = open(self.config, 'w').close()

    def run(self, some_dict):
        print("Running configure with the following options", some_dict)
        self.settings_files(self)
##        creds = self.load_info(self)
##        print(creds)
        self.get_info(self)


if __name__ == '__main__':
    conf = configure()
    conf.get_info(conf)
    
    
