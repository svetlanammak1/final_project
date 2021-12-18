## Author: Svetlana
## Date: 29/11/2021 
## Task: Create config_cl class to read config file: Config_new.ini

import configparser
from os import strerror

class config_cl():
    def __init__(self):
        self.host = ""
        self.port = ""
        self.database = ""
        self.dicname = ""
        self.outfile = ""
        self.conf_dic = {}
        
    
    def read_config(self):
        config = configparser.ConfigParser()
        
        try:
            config.read('Config_new.ini')
            self.conf_dic["host"] = config.get('DEFAULT','host')
            self.conf_dic["outfile"] = config.get('DEFAULT','outfile')
            
            self.database = config.get('mariadb','name')
            User = config.get('mariadb','user')
            Password = config.get('mariadb','password')
                                  
            self.conf_dic["port"] = config.get('redis','port')
            self.conf_dic["database"] = config.get('redis','db')
            self.conf_dic["dicname"] = config.get('redis','dicname')
            
        
        except IOError as e:
            print("I/O error occured: ", strerror.errno())      
        except Exception as e:
           print(e.__str__())
        else:
            return self.conf_dic      
        
    
