## Author: Svetlana
## Date: 29/11/2021 
## Task: Create logger , set host, database, port variables ,
#         show menu and call pizza_db2 or pizza_server modules


from sys import modules, path
import sys
import logging
from os import strerror
import configparser
import os
from packages.pizza_progs import pizza_db
from packages.pizza_progs import pizza_server 
from packages.pizza_progs import config

#############################
## create log file in current dir

logger = logging.getLogger('pizza')
logger.setLevel(logging.DEBUG)

handler = logging.FileHandler('pizza_order_log.txt', 'w')
handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(levelname)s - %(message)s')

handler.setFormatter(formatter)

logger.addHandler(handler)

#############################
print("START")
logger.debug('{0} {1} '.format(__name__, ": process started!"))

#read_config class
logger.debug('{0} {1} '.format(__name__, ": Read config file"))
conf = config.config_cl()
conf_dic = conf.read_config()
Port = conf_dic["port"]
host = conf_dic["host"]
database = conf_dic["database"]
dicname = conf_dic["dicname"]
outfile = conf_dic["outfile"]

## path for output files
path_dir_out = os.getcwd() + '\\' + outfile + '\\'

logger.debug('{0} {1} {2} {3} {4} {5} {6}'.format(__name__, "host/port/database", host, '/',Port, '/',database ))
while True:
    print('''
     1. Show Pizza
     2. Add Pizza
     3. Change Pizza
     4. Delete Pizza
     5. Order Pizza
     6. Unload Pizzas
     7. Pizza on server
     8. Exit''' )
    try:
         put = int(input("Put what you want 1, 2 ,3 , 4 ,5, 6, 7,8: "))
         logger.debug('{0} {1} {2} '.format(__name__, "Enter Put", put))
         if put ==8:
             print("PUT",put)
             #pizzeria1.menu_controller(put, pizzeria )
             break
    except: 
        print("Bad operation")
    else:
        if put in [1,2,3,4, 5, 6]:
            pizza_db.start(put,logger, database, path_dir_out) 
            
        if put == 7:
            pass
            pizza_server.start(host, Port, logger, dicname)             