The project is in pizzeria folder:
pizzeria folder contains:
  - main.py - main program 
  - pizza.db  
  - Config_new.ini  - config file
  - pizza_order_log.txt  - logger 
  - output_file folder
  - help folder
  - packages folder: 
    - pizza_progs folder:
      - pizza_db.py  
      - pizza_server.py
      - config.py 

1. main.py description.
 The program creates log file , reads Config_new.ini (config file)
 and shows menu with 8 items:
     1. Show Pizza
     2. Add Pizza
     3. Change Pizza
     4. Delete Pizza
     5. Order Pizza
     6. Unload Pizzas
     7. Pizza on server
     8. Exit

1. displays data from pizza table (calls piza_db program)
2. inserts pizza into pizza table (calls piza_db program)
3. updates pizza in pizza table   (calls piza_db program) 
4. deletes pizza from pizza table (calls piza_db program)
5. selects pizza from pizza table on pizza id and writes out into 'pizza_order.txt'file(calls piza_db program)
6. unloads data from pizza table to the (calls piza_db program)
7. calls pizza_server program 
8. exit from the program 

  
  Config_new.ini :
[DEFAULT]
host = localhost
outfile = output_files

[mariadb]
name = pizza.db
user = root
password = password

[redis]
port = 3000
db = pizza.db
dicname = pizza

2. Description config.py:

The program reads Config_new.ini file and returns 
dictionary with host, database name, port, json name (dicname), outfile path variables.

3.Description python_db2.py: 
The Pizza class to make pizza with methods:
       - create_pizza_table - create pizza table if it does not exist
       - add_pizza - insert pizza to pizza table
       - remove_pizza - delete pizza from  pizza table
       - show_pizza  - show all pizza in table
       - unload_pizza - unload pizzas from the table to the  'output_files\pizza_json.json' file
       - find_id - find pizza on id  and return value if id exists or None  if id does not exist
       - close_conn - close db connection
The Order class with methods:
        - make_pizza - get pizza order on pizza id and write out the order to the  'output_files\pizza_order.txt' file.
          The output file contains last order. All orders are displayed in log file.
  
The PizzaError class to raise  exception if pizza name is empty or not 
The IdExc  class to raise exception from wrong pizza id
The TooMuchCheeseError class to raise exception from cheese value > 100 or <0 

The function: menu_controller(put, pizzeria, logger)- to call class method according to 'put' parameter from main.py
The function: start(put, logger, database,path_dir_out) - create  pizzeria (Order class instance) and call  menu_controller function
The Process is commented in logger('pizza_order_log.tx'  file)

4. Description python_server.py
   At first server should be started using 'pizza_json.json' file in the /pizzeria/output_files dir:
             json-server --watch pizza_json.json.
   The program shows all pizza and choice menu after run:
        1. Server:Show Pizza
        2. Server:Add Pizza
        3. Server:Change Pizza
        4. Server:Delete Pizza
        5. Exit

     The program creates Server class to process pizza with methods:
        - Select - show all pizza ( choice_menu = 1)
        - Post_pz - post pizza    ( choice_menu = 2)
        - Delete_pz - delete pizza ( choice_menu = 4)
        - Update_pz - put pizz     ( choice_menu = 3)
      
       

       The IdExc  class - to raise exception from wrong pizza id
       The TooMuchCheeseError class - to raise exception from cheese value > 100 or <0 

       The function: menu_choice(logger) - shows menu  and calls method according to the choice
       The function: start(localhost, port, logger,dicname) - calls  menu_choice function
       The frocess is commented in logger('pizza_order_log.tx'  file) 



