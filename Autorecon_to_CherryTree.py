import sqlite3
import os 
import sys 

def CreateDatabase():
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    
    cur.execute('CREATE TABLE bookmark (node_id INTEGER UNIQUE,sequence INTEGER)')
    cur.execute('CREATE TABLE children (node_id INTEGER UNIQUE,father_id INTEGER,sequence INTEGER)')
    cur.execute('CREATE TABLE codebox(node_id INTEGER,offset INTEGER,justification TEXT,txt TEXT,syntax TEXT,width INTEGER,height INTEGER,is_width_pix INTEGER,do_highl_bra INTEGER,do_show_linenum INTEGER)')
    cur.execute('CREATE TABLE grid (node_id INTEGER,offset INTEGER,justification TEXT,txt TEXT,col_min INTEGER,col_max INTEGER)')
    cur.execute('CREATE TABLE image (node_id INTEGER,offset INTEGER,justification TEXT,anchor TEXT,png BLOB,filename TEXT,link TEXT,time INTEGER)')
    cur.execute('CREATE TABLE node (node_id INTEGER UNIQUE,name TEXT,txt TEXT,syntax TEXT,tags TEXT,is_ro INTEGER,is_richtxt INTEGER,has_codebox INTEGER,has_table INTEGER,has_image INTEGER,level INTEGER,ts_creation INTEGER,ts_lastsave INTEGER)')   
    
    con.commit()
    con.close()  
def EditDatabase(node_id, father_id, name, info):
     
    con = sqlite3.connect(database_name)
    cur = con.cursor()
    
    txt = '<?xml version="1.0" ?><node><rich_text>' + info + '</rich_text></node>' 
    syntax = 'custom-colors' 
    tags = ''
    is_ro = '0'
    is_richtext = '1' 
    has_codebox = '0' 
    has_table = '0'
    has_image = '0' 
    level = '0' 
    ts_creation = '0' 
    ts_lastsave = '0'    
    
    newnode = "'" + node_id +"','" + name + "','" + txt +"','"+ syntax +"','"+ tags +"','"+ is_ro +"','"+ is_richtext +"','"+ has_codebox +"','" + has_table + "','" + has_image +"','"+ level +"','"+ ts_creation +"','"+ ts_lastsave + "'"
    SQL_query = 'INSERT INTO node VALUES('+ newnode + ');'
    cur.execute(SQL_query)
    sequence = '1'
    
    newnode = "'" + node_id + "'," +  father_id + " ,'" + sequence + "'" 
    SQL_query = 'INSERT INTO children VALUES('+ newnode + ');'
    cur.execute(SQL_query)    
    con.commit()    
    con.close()


"""
Main function:
"""

autorecon_dir = sys.argv[1]

if len(sys.argv) > 2:
        con1 = sqlite3.connect(sys.argv[2])
        cur1 = con1.cursor()
        SQL_query = 'SELECT * FROM node ORDER BY node_id DESC LIMIT 1;'    
        print("Connecting to the CherryTree Database: " + sys.argv[2])
        nodeid = cur1.execute(SQL_query).fetchone()[0]
        database_name = sys.argv[2]
        con1.close()
else:
    nodeid = 0 
    database_name = "Autorecon_to_CherryTree.ctb" 
    
    try: 
        os.remove(database_name)
    except:
        pass    
    
    print ("Creating a new database: " + database_name) 
    CreateDatabase()

print("Reading the AutoRecon results and appending to the database")

for i in os.listdir(autorecon_dir):
    nodeid = nodeid + 1
    parent = nodeid
    EditDatabase(str(nodeid),'0',str(i),'-')
    for j in os.listdir(autorecon_dir + "/" + i):
        nodeid = nodeid + 1
        parent_1 = nodeid
        EditDatabase(str(nodeid),str(parent),str(j),'-')
        for k in os.listdir(autorecon_dir + "/" + i + "/" + j):
            nodeid = nodeid + 1
            try:
                fp = open(autorecon_dir + "/" + i + "/" + j + "/" + k)
                content = str(fp.read().replace('<','&lt;').replace('>','&gt;'))
                EditDatabase(str(nodeid),str(parent_1),str(k),str(content))
            except:
                pass

print("Done")
