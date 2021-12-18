## Author: Svetlana
## Date: 09/12/2021 
## Task: Create Pizza class to make pizza with methods:
##       - create_pizza_table - create pizza table if it does not exist
##       - add_pizza - insert pizza to pizza table
##       - remove_pizza - delete pizza from  pizza table
##       - show_pizza  - show all pizza in table
##       - unload_pizza - unload pizzas from the table to the  'pizza_json.json' file
##       - find_id - find pizza on id  and return value if id exists or None  if id does not exist
##       - close_conn - close db connection
##       Create Order class with methods:
##        - make_pizza - get pizza order on pizza id and write out the order to the  'pizza_order.txt' file
##  
##       Create PizzaError class to raise  exception if pizza name is empty or not 
##       Create IdExc  class to raise exception from wrong pizza id
##       Create TooMuchCheeseError class to raise exception from cheese value > 100 or <0 
##
##       Function: menu_controller(put, pizzeria, logger)- to call class method according to 'put' parameter from main.py
##       Function: start(put, logger, database,path_dir_out) - create  pizzeria (Order class instance) 
##                 and call  menu_controller function
##       Process is commented in logger('pizza_order_log.tx'  file)

from os import strerror
import logging
import sqlite3
import configparser
import json


class Pizza():
    
    def __init__(self,logger,db):
        self.logger = logger
        self.db = db
        print("self db", self.db)
        #self.conn = sqlite3.connect('pizza.db')
        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()
        self.create_pizza_table()
    
    
    def create_pizza_table(self):
        '''Create pizza table'''

        self.c.execute('''CREATE TABLE IF NOT EXISTS pizza
            (id INTEGER PRIMARY KEY ,name TEXT NOT NULL, 
            cheese INTEGER  WITH DEFAULT 0)''')     
        

    def add_pizza(self):

        ''' adds pizza to pizza table'''    

        self.logger.debug('{0} {1} '.format(__name__, ": process insert pizza started!"))
        name = input("Enter pizza name: ")
        if  name.isspace() or not name.isalpha():
            raise PizzaError(pizza = name, message = 'Bad pizza name')
        cheese = int(input("Enter cheese: "))   
        if cheese < 1 or cheese > 100:
            raise TooMuchCheeseError(pizza = name, cheese = cheese, message='Bad cheese value')
              
        self.c.execute('''INSERT INTO pizza (name, cheese) VALUES(?,?)''',
                       (name, cheese,))
           
        self.conn.commit()               
        self.logger.debug('{0} {1} '.format(name, "Successfully inserted to pizza tab"))
        print(name, ": Successfully added to pizza table!")
        

    def remove_pizza(self):    
        ''' Remove pizza from pizza tab'''

        self.logger.debug('{0} {1} '.format(__name__, ": process delete pizza started!"))
        numid = int(input("Enter id pizza which you want to delete: "))
        if numid < 1:
            raise IdExc(id = numid)
       
        numpz = self.find_id(numid)
        if numpz is not None:
            self.c.execute('''DELETE from pizza  WHERE id = ?''' ,
                (numid,))   
            self.conn.commit()
            self.logger.info('{0} {1} '.format(numpz[1], "pizza successfully removed from pizza table")) 
            print(numpz[1], ": pizza successfully removed from pizza table!")
        else:
            print('The such id does not exist!')   
            raise IdExc(id = numid)
            
        

    def show_pizza(self):
        ''' Show all pizzas from pizza tab'''

        print("Pizza table contains the following...") 
        self.logger.debug('{0} {1} '.format(__name__, ": process show pizzas started!"))   
        print("ID  ", "Pizza       ", " Cheese    ")
        for row in self.c.execute('''SELECT id, name, cheese FROM pizza'''):
            print(row[0], "  ",  row[1].ljust(15),  str(row[2]).ljust(5) )   
            
    def update_pizza(self):
        ''' Update cheese value in pizza tab on id'''
        
        self.logger.debug('{0} {1} '.format(__name__, ": process update pizza started!"))

        id = int(input("Enter pizza id : "))
        if id < 1:
           raise IdExc(id=id)
         
        cheese = int(input("Enter cheese value: "))   
        if cheese < 1 or cheese > 100:
            raise TooMuchCheeseError( pizza=str(id), cheese = str(cheese), message='Cheese error')
        numpz = self.find_id(id)    
        if numpz is not None:
            self.c.execute('''UPDATE pizza SET cheese = ? WHERE id = ?''', 
                (cheese, id))    
            self.conn.commit()
            self.logger.info('{0} {1} {2} '.format(__name__,numpz[1], "pizza successfully updated in pizza table")) 
            print(numpz[1], ": pizza successfully updated from pizza table!")
        else:
            print('The such id does not exist!')     
            raise IdExc(id = id)

    def find_id(self, id): 
        self.id = id
        find = False   
        que =  '''SELECT id, name, cheese FROM pizza'''
        rows =  self.c.execute(que)
        for row in rows:
            if row[0] == self.id:
               find = True
               return row
        if not find:
            return None      

    def unload_pizza(self):
        ''' Unload pizza table to result_json json file'''
        
        self.logger.debug('{0} {1} '.format(__name__, ": process unload pizzas started!"))
        dic = {}
        list_dic=[]
        ll =[]
        pizza = {}
        print("Pizza table is unloading")    
        ff = 'pizza_json.json'
        try:       
            with open(self.outpath+'pizza_json.json', 'w') as newfile:
            
                rows = self.c.execute('''SELECT id, name, cheese FROM pizza''')
                for row in rows:
                    dic["id"] = row[0]
                    dic["name"] = row[1]
                    dic["cheese"] = row[2]
                    dictionary_copy = dic. copy()
                    list_dic.append(dictionary_copy)
                
                pizza["pizza"] = list_dic
                to_json = json.dumps(pizza)
                
                newfile.write(to_json)
            
            newfile.close()
        except IOError as e:
                    print("I/O error occured: ", strerror.errno())    
        self.logger.info('{0} {1}'.format(__name__,"pizza tab unloaded to result_json file"))
        
    
    def close_conn(self):
        self.conn.close()              

class PizzaError(Exception):
   def __init__(self, head="PizzaError", pizza= 'uncknown', message = "Bad pizza name"):
        super().__init__(message)
        self.head = head
        self.message = message
    
class TooMuchCheeseError(PizzaError):
    def __init__(self, pizza='uncknown', cheese = '>100 G', message='Cheese error'):
        super().__init__(message)
        PizzaError.__init__(self, head="PizzaError",pizza = pizza, message=message)
        self.cheese = cheese
        
class IdExc(Exception):
    def __init__(self, head="PizzaIdError", id = 0, message="Bad ID: "):
            super().__init__(message)
            self.head = head
            self.message = message  + str(id) 


class Order(Pizza):
    ''' class to order Pizza'''

    def __init__(self,logger,db,path_dir_out): 
        super().__init__(logger,db)
        self.orders = {}
        self.counter = 1
        self.message = ""
        self.outpath = path_dir_out
    
       
    def make_pizza(self):
        
        ''' function create order for Pizza'''
        
        id = int(input("Enter pizza id : "))
        if id < 1:
            raise IdExc(id = id)
        
        rows = self.find_id(id)
        if rows is None:
            print("There is not the such pizza")
            raise IdExc(id = id)
                    
        self.orders["id"] = rows[0]
        self.orders["name"] = rows[1]
        self.orders["cheese"] = rows[2]
    
        try:
 
            with open(self.outpath+'pizza_order.txt', 'w') as orderfile:
                strout = str(self.counter) + " " + self.orders["name"] + " : Has successfully created!\n"
                orderfile.write(strout)
                self.logger.info('{0} {1} {2} {3}'.format(__name__, self.counter," order ",self.orders, \
                                        " was writen out to pizza_order.txt file"))
                print("File successfully written for pizza: ", self.orders["name"])  
        
                orderfile.close()
        except IOError as e:
                    print("I/O error occured: ", strerror.errno())
                    self.logger.debug('{0} {1} {2} '.format(__name__, "I/O error occured for pizza_order.txt: " + str(id)))     
        self.counter += 1
    
       

def start(put, logger, database, path_dir_out):
    pizzeria = Order(logger,database, path_dir_out)
    menu_controller(put,pizzeria,logger) 

## menu controller
def menu_controller (put, pizzeria, logger):
    print("PUT: ", put)
    
    if put == 1:
        #show task service
        pizzeria.show_pizza()
    elif put == 2:
        try:
            pizzeria.add_pizza()
        except PizzaError as e:
             print(e.message)
             logger.debug('{0} {1} {2}'.format(__name__," PizzaError  on add pizza ",e.message))  
        except TooMuchCheeseError as e:
             print(e.message)
             logger.debug('{0} {1} {2}'.format(__name__," TooMuchCheeseError  on add pizza ",e.message))     
        except Exception as e:
             print("Something goes bady :((")   
             logger.debug('{0} {1} {2}'.format(__name__," TooMuchCheeseError  on add pizza ",e.__str__()))
        else: print("The task was added successfully!")      
        finally:
            print()
    elif put == 3:
       ## update priority 
        try:
            pizzeria.update_pizza()
        except PizzaError as e:
             print(e.message)
             logger.debug('{0} {1} {2}'.format(__name__," PizzaError  on update ",e.message))  
        except TooMuchCheeseError as e:
             print(e.message)    
             logger.debug('{0} {1} {2}'.format(__name__,"TooMuchCheeseError  on update ",e.message))  
        except IdExc as e: 
            print(e.message)
            logger.debug('{0} {1} {2}'.format(__name__,"IdExc on update ",e.message))     
        except Exception as e:
             print("Something goes bady :((") 
             logger.debug('{0} {1} {2}'.format(__name__," PizzaError  on update pizza ",e.__str__()))     
        else: 
            print("The task  completed ")      
            
        finally:
            print()        
    elif put == 4:
       ## delete task 
        try:
            pizzeria.remove_pizza()
        except IdExc as e:
             print(e.message)
             logger.debug('{0} {1} {2}'.format(__name__,"IdExc on delete ",e.message))    
        except Exception as e:
            print(e.__str__())
            print("Something goes bady :((") 
            logger.debug('{0} {1} {2}'.format(__name__," PizzaError  on delete pizza ",e.__str__())) 
        else: print("The task was completed successfully!")      
        finally:
            print()        
    elif put == 5:
        try:
            pizzeria.make_pizza()
        except Exception as e:
            print(e.__str__())
            print("Something goes bady :((")  
            logger.debug('{0} {1} {2}'.format(__name__," Error  on order pizza ",e.__str__()))   

    elif put == 6:
        try:
            pizzeria.unload_pizza()       
        except Exception as e:
            print(e.__str__())
            print("Something goes bady :((")
            logger.debug('{0} {1} {2}'.format(__name__," Error  on unload pizzas ",e.__str__())) 
                 
    
    elif put == 7:
        pizzeria.close_conn()
        print("Exit")
        logger.info('{0} {1}'.format(__name__,"Exit from db2 pizza ")) 
        return

    else:
        pass     
#############################





   
        
   