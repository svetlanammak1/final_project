## Author: Svetlana
## Date: 09/12/2021 
## Task: server starts using 'pizza_json.json' file: json-server --watch pizza_json.json 
#        Create Server class to make pizza with methods:
##       - Select - show all pizza
##       - Post_pz - post pizza 
##       - Delete_pz - delete pizza 
##       - Update_pz - put pizz
##       - find_id - find pizza on id  and return value if id exists or None  if id does not exist
##       - close_conn - close db connection
##       
##  
##       Create IdExc  class to raise exception from wrong pizza id
##       Create TooMuchCheeseError class to raise exception from cheese value > 100 or <0 
##
##       Function: menu_choice(logger) - show menu  and call method according to the choice
##       Function: start(localhost, port, logger,dicname) - call  menu_choice function
##       Process is commented in logger('pizza_order_log.tx'  file)

import json
from os import name
import sys
import requests
from requests import exceptions
from requests import status_codes
from requests.models import codes 


key_names = ["id", "name", "cheese"]
               
key_width =[10, 15, 10]

list_id = []
list_name = []
list_cheese =[]

headers = {'Connection' : 'Close'}
h_content = {'Content-Type': 'application/json'}

def show_head():
    for(n,w) in zip(key_names, key_width):
        print(n.ljust(w), end="|")
    print()

def show_empty():
    for w in  key_width:
        print(' '.ljust(w), end='|')
    print()

def show_pz(car):
    for(n,w) in zip(key_names, key_width):
        print(str(car[n]).ljust(w), end='|')
    print()


def show(json):
    show_head()
    if type(json) is list:
        for car in json:
            show_pz(car)
    elif  type(json) is dict:
        if json:
             show_pz(json)
        else:
             show_empty()     


class Server():
    def __init__(self, location, port, logger,dicname):
        self.location = location
        self.port = port
        self.logger = logger
        self.dicname = dicname
        self.list_id = []
        self.list_name = []
        self.list_cheese = []
        
    def Select(self):
        ''' Show pizzas'''
        try:
            reply = requests.get('http://'+ self.location +':' + self.port + '/' + self.dicname,headers = headers)
           
        except Exception as p:
            print(p.__str__()) 
            self.logger.debug('{0} {1} {2}'.format(__name__,"Select error ", p.__str__()))   
       
        if reply.status_code == requests.codes.ok:
            show(reply.json())
            
            for pz in reply.json():
               for(n) in key_names:
                    if n == "id":
                       self.list_id.append(pz[n])
                    if n == "name":
                       self.list_name.append(pz[n])    
                    if n == "cheese":    
                       self.list_cheese.append(pz[n]) 
            

    def Post_pz(self):
        '''' Insert (post)  pizza'''

        self.logger.debug('{0} {1} '.format(__name__, "Server: post  pizza start "))
        n_pz = input("Enter pizza name: ")
        ch = int(input("Enter pizza cheese value: "))
        max_id = max(self.list_id) + 1
        if ch < 0 or ch > 100: 
            print("Incorrect cheese vlue was entered!")
            raise TooMuchCheeseError(pizza=max_id, cheese = str(ch))


        di = {}
        di[key_names[0]] = max_id
        di[key_names[1]] = n_pz
        di[key_names[2]] = ch
        di["convertible"] = False
        
        try:
            reply = requests.post('http://'+ self.location +':' + self.port + '/' + self.dicname,headers = h_content,data =json.dumps(di))
            #reply = requests.get('http://localhost:3000/test',headers = headers)
            Server.Select(self)
        except Exception as p:
            print(p.__str__())    
        print("Pizza was added")
        self.logger.debug('{0} {1}{2} '.format(__name__,n_pz, "Server: Successfully inserted to pizza tab"))

    def Delete_pz(self):
        '''Delete pizza'''
        self.logger.debug('{0} {1} '.format(__name__, "Server: delete  pizza  start"))
        pz_id = int(input("Enter pizza id: "))
        if pz_id not in self.list_id:
            print("Incorrect id was entered!")
            raise IdExc(id =pz_id)
        
        try:
          
            reply = requests.delete('http://'+ self.location +':' + self.port + '/' + self.dicname+ '/'+str(pz_id))
            #reply = requests.get('http://localhost:3000/test',headers = headers)
            Server.Select(self)
        except Exception as p:
            print(p.__str__())    
        print("Pizza was deleted")  
        self.logger.debug('{0} {1} {2} '.format(__name__, pz_id, "Server: Successfully deleted  pizza "))  

    def Update_pz(self):
        ''' Update pizza'''
        self.logger.debug('{0} {1} '.format(__name__, "Server: Update pizza started "))
        pz_id = int(input("Enter pizza id: "))

        if pz_id not in self.list_id:
            print("Incorrect id was entered!")
            raise IdExc(id =pz_id)
            
        pz_ch = int(input("Enter pizza cheese value: ")) 
        if pz_ch < 0 or pz_ch > 100: 
            print("Incorrect cheese vlue was entered!")
            raise TooMuchCheeseError(pizza=pz_id, cheese = str(pz_ch))
               
        di = {}    
        for i in range(len(self.list_id)):
            if  self.list_id[i] ==  pz_id:
                di[key_names[0]] = pz_id
                di[key_names[1]] = self.list_name[i]
                di[key_names[2]] = pz_ch
                di["convertible"] = True                

        try:
            reply = requests.put('http://'+ self.location +':' + self.port + '/' + self.dicname + '/'+str(pz_id), \
                                  headers = h_content,data =json.dumps(di))
            
            Server.Select(self)
        except Exception as p:
            print(p.__str__())    
        print("Pizza was updated")
        self.logger.debug('{0} {1} '.format(pz_id, "Server: Successfully updated  pizza "))  

        
class IdExc(Exception):
    def __init__(self, head="PizzaIdError", id= 0,message="Bad ID: "):
            super().__init__(message)
            self.head = head
            self.id = id
            self.message = message + str(self.id)  
            
                 

class TooMuchCheeseError(Exception):
    def __init__(self, pizza=id, cheese = ' >100 G or <0 ', message='Cheese error: '):
        super().__init__(message) 
        self.cheese = cheese            
        self.message = message + cheese + " pizza id: " +str(pizza)

#############################

def menu_choice(logger):        
   
        print('''
        1. Server:Show Pizza
        2. Server:Add Pizza
        3. Server:Change Pizza
        4. Server:Delete Pizza
        5. Exit''' )
        try:
            put = int(input("Put what you want 1, 2 ,3 , 4 ,5: "))
            logger.debug('{0} {1} {2}'.format(__name__, ": Put entered:", put))
            print("PUT", put)
            
        except: 
           print("Bad operation")
           
        else:
           if put in [1,2,3,4, 5]:
               #menu_controller(put,pizzeria)   
              return put 

def start(localhost, port, logger,dicname):
    ''' Start to work with server'''
    logger.debug('{0} {1}'.format(__name__,": Server process started"))
    try:
        req = Server(localhost,port, logger,dicname) 
        req.Select()
        
        while True:
            put=menu_choice(logger)
            if put == 1:
               req.Select()

            if put == 2:
               try:
                req.Post_pz()
               except IdExc as e: 
                    print(e.message)
                    logger.debug('{0} {1} {2}'.format(__name__,"IdExc on Post ",e.message))  
               except TooMuchCheeseError as e: 
                   print(e.message)
                   logger.debug('{0} {1} {2}'.format(__name__,"TooMuchCheeseError on Post ",e.message)) 
               except Exception as e:
                   print("Something goes bady :((") 
                   logger.debug('{0} {1} {2}'.format(__name__," PizzaError  on Post pizza ",e.__str__())) 


            if put == 3:
               try: 
                req.Update_pz()   
               except TooMuchCheeseError as e:
                print(e.message)    
                logger.debug('{0} {1} {2}'.format(__name__,"TooMuchCheeseError  on update ",e.message))  
               except IdExc as e: 
                print(e.message)
                logger.debug('{0} {1} {2}'.format(__name__,"IdExc on update ",e.message)) 
               except Exception as e:
                print("Something goes bady :((") 
                logger.debug('{0} {1} {2}'.format(__name__," PizzaError  on update pizza ",e.__str__())) 

            if put == 4:
                try: 
                    req.Delete_pz()
                except IdExc as e: 
                    print(e.message)
                    logger.debug('{0} {1} {2}'.format(__name__,"IdExc on delete ",e.message)) 
                except Exception as e:
                    print("Something goes bady :((") 
                    logger.debug('{0} {1} {2}'.format(__name__," PizzaError  on delete pizza ",e.__str__())) 

            if put == 5:
               print("End")
               logger.debug('{0} {1}'.format(__name__," Process on server ended"))
               break              
        
    except requests.RequestException:
     print("Communication error") 
     logger.debug('{0} '.format("Server Communication error"))
    else:
        print("End of server work")
        
        
        
     
