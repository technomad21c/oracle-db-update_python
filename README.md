# oracle-db-update_python

## Purpose
It is to update fields in remote Oracle database with data returned from a Rest API server.
   
## Prerequisite 
1. Cx_Oracle library

   `python -m pip install cx_Oracle --upgrade`

    reference: [cx_Oracle 8 Installation](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html)
  
- Oracle Instant Client

    1. download the [Oracle Instant Client](https://www.oracle.com/database/technologies/instant-client/downloads.html)
    
    2. unzip it
    
    3. set the PATH to the directory of the Oracle Instant Client

       - Linux
    
         `export LD_LIBRARY_PATH=/opt/oracle/instantclient_19_6:$LD_LIBRARY_PATH`
      
       - Window
     
         add the path of the Oracle Instant Client to 'PATH' variable in the system variable window
    
    reference: [Oracle Instant CLient Installation](https://cx-oracle.readthedocs.io/en/latest/user_guide/installation.html#id3)
    
- request

  `python -m pip install requests`
      

