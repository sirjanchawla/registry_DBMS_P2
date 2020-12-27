import interpreter
from bsddb3 import db
import numpy as np
from functools import reduce
import re
#https://stackoverflow.com/questions/22821124/berkeley-db-equivalent-of-select-count-all-select-count-where-like
global brief
brief = True
def FindFilename(column_name):
    if column_name in ["subject", "body"]:
        return "te.idx"
    elif column_name in ["from", "to", "bcc", "cc"]:
        return "em.idx"
    elif column_name == "date":
        return "da.idx"
    else:
        return ""


def ExactQuery(subquery):
    filename = FindFilename(subquery[0])

    database = db.DB()
    database.open(filename, None)
    curs = database.cursor()
    
    key_value = ""
    if subquery[0] == "subject":
        key_value = "s-" + subquery[2]
    elif subquery[0] == "body":
        key_value = "b-" + subquery[2]
    elif subquery[0] in ["from", "to", "bcc", "cc"]:
        key_value = subquery[0] + "-" + subquery[2]
    else :
        key_value = subquery[2]
    #else:
        #x = 0

    results = []
    result = curs.set(key_value.encode())
        
    if not result is None:
        results.append(str(result[1].decode()))

        #iterating through duplicates:
        duplicate = curs.next_dup()

        while not duplicate is None:
            results.append(str(duplicate[1].decode()))
            duplicate = curs.next_dup()
    
    curs.close()    
    database.close()
    #results = set(results)def find_m(r_id):

    return results
def RangeQuery(subquery):
    database = db.DB()
    database.open('da.idx', None)
    curs = database.cursor()
    list_d = []
    if subquery[1] == "<":
        result = curs.first()
        
        while(result!=None):
            if(result[0].decode('utf-8')< subquery[2]):
                list_d.append(result[1].decode('utf-8'))
            
                result=curs.next()
        if(result == None):
            print("date not correct")
    elif subquery[1] == ">":        
        result=curs.set_range(subquery[2].encode('utf-8'))
        
        while(result != None):
            if result[0].decode('utf-8') == subquery[2]:
                result = curs.next()
                
            list_d.append(result[1].decode('utf-8'))
            result = curs.next()
            
        if(result == None):
            print("Lastest date")
            
    elif subquery[1] == "<=":
        result = curs.first()
        
        while(result!=None):
            if(result[0].decode('utf-8') <= subquery[2]):
                list_d.append(result[1].decode('utf-8'))
            
                result=curs.next()
    
    elif subquery[1] == ">=":
        result=curs.set_range(subquery[2].encode('utf-8'))
        
        while(result != None):
            list_d.append(result[1].decode('utf-8'))
            result = curs.next()
            
        if(result == None):
            print("Lastest date")        
        
        
    curs.close()    
    database.close()
    return list_d
            

def find_m_b(r_id):
    database = db.DB()
    database.open('re.idx',None)
    curs = database.cursor()
    
    for l in r_id:        
        result = curs.set(l.encode('utf-8'))
 
        if(result != None):
            email = str(result[1].decode('utf-8'))
            subject = re.search(r"<subj>[a-zA-Z0-9 _/:,;-?!]+</subj>", email)
            
            if subject is None:
                subject = "Empty subject"            
            else:
                subject = subject.group()
                subject = subject.replace("<subj>", "")
                subject = subject.replace("</subj>", "")
           
            
            print(l, ":", subject)
            
                
        else:
            print("No Entry Found.")    
    
    
    
def find_m(r_id):
    database = db.DB()
    
    #database.set_flags(db.DB_DUP) #declare duplicates allowed before you create the database
    database.open('re.idx',None)
    
    curs = database.cursor()
    
    #list_e = []
    #bool_e = True
    for l in r_id:
        
        
        result = curs.set(l.encode('utf-8'))
        if(result != None):
            print(str(result[1].decode('utf-8')))
                
                #iterating through duplicates:
            dup = curs.next_dup()
            while(dup != None):
                print(str(dup[1].decode('utf-8')))
                   
                dup = curs.next_dup()
        else:
            print("No Entry Found.")    
        
        
def PartialMatch(subquery):
    database = db.DB()
    database.open('te.idx',None)
    curs = database.cursor()
    p_id = []
    word = subquery[2]
    
    key_val = curs.get(('s-'+ word).encode(), flags=db.DB_SET_RANGE)
    while key_val != None:
        p_id.append(key_val[1].decode('utf-8'))
        key_val = curs.next()
    key_val = curs.get(('b-'+ word).encode(), flags=db.DB_SET_RANGE)
    while key_val != None:
        p_id.append(key_val[1].decode('utf-8'))
        key_val = curs.next()
    
    return p_id
       
def main():
    global brief
    line = input("Please enter a query: ")
    query = interpreter.Interpret(line)
    results = []
    
    for subquery in query:
        if subquery[1] == "=":
            if subquery[2] == "brief":
                brief = True
            else:
                brief = False
        elif subquery[1] == ":":
            results.append(ExactQuery(subquery))
        elif subquery[1] in ["<",">","<=",">="]:
            results.append(RangeQuery(subquery))
        else:
            results.append(PartialMatch(subquery))
            
            
    if len(results)>0:    
    
        r_id = reduce(np.intersect1d,results)
        r_id = set(r_id)
    
        if brief == False:
            find_m(r_id)
        else:
            find_m_b(r_id)
    main()
    
    #print(hey)
            
    
main()
