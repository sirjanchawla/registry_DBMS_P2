import xml.etree.cElementTree as ET
import re




def c_dates(filename):
	tree = ET.ElementTree(file=filename)
	root = tree.getroot()

	file = open("dates.txt","w")
	for Em in root: 
	    # every email
	    for attri in Em:
	        # every attributes inside Email
	        if(attri.tag == 'row'):
	            text = attri.text
	        if(attri.tag == 'date'):
	            date_row = attri.text+':'+text
	            file.write(date_row)
	            file.write("\n")
	            
	            
	            
	file.close()




def c_emails(filename):
	tree = ET.ElementTree(file=filename)
	root = tree.getroot()
	counter = 0
	file = open("emails.txt","w")

	for Em in root:
	    for attri in Em:
	        if(attri.tag == "row"):
	            row = attri.text
	            
	        
	        if(attri.tag == "from" and attri.text != None):
	            #print(root[counter][0].text+":",end="")
	            #print(attri.tag,end="-")        
	            #print(attri.text,end=":")
	            #print(row)
	            f = attri.tag + "-" + attri.text + ":" + row
	            file.write(f)
	            file.write("\n")
	            #print(f)
	            
	            
	        if(attri.tag == "to" and attri.text != None):
	            #print(attri.tag,end="-")
	            #print(attri.text,end=":")
	            #print(row)
	            t = attri.tag + "-" + attri.text + ":" + row
	            file.write(t)
	            file.write("\n")
	            #print(t)
	            
	        if(attri.tag == "cc" and attri.text != None):
	            #print(attri.tag,end="-")
	            #print(attri.text,end=":")
	            #print(row)
	            cc = attri.tag + "-" + attri.text + ":" + row
	            file.write(cc)
	            file.write("\n")
	            #print(cc)            
	            
	        if(attri.tag == "bcc" and attri.text != None):
	            #print(attri.tag,end="-")
	            #print(attri.text,end=":")
	            #print(row)
	            bcc = attri.tag + "-" + attri.text + ":" + row
	            file.write(bcc)
	            file.write("\n")
	            #print(bcc)            
	    
	            
	file.close()


def c_terms(filename):
	tree = ET.ElementTree(file=filename)
	root = tree.getroot()
	counter = 0
	file = open("terms.txt","w")

	for Em in root:
	    for attri in Em:
	        if(attri.tag == "row"):
	            the_row = attri.text
	        
	        if(attri.tag == "subj" and attri.text != None):
	            for u in re.split("[^0-9a-zA-Z_-]+", attri.text):
	                we_want = re.sub("[^0-9a-zA-Z_-]",'',u)
	                if(len(we_want)>2):
	                    #print("s-",end="")
	                    file.write("s-")
	                    for ch in we_want:
	                        ch = ch.lower()
	                        #print(ch,end="")  
	                        file.write(ch)
	                    #print(":"+the_row)
	                    file.write(":")
	                    file.write(the_row)
	                    file.write("\n")
	                    
	        if(attri.tag == "body" and attri.text != None):
	            for uu in re.split("[^0-9a-zA-Z_-]+", attri.text):
	                we_wantt = re.sub("[^0-9a-zA-Z_-]",'',uu)
	                if(len(we_wantt)>2):
	                    #print("b-",end="")
	                    file.write("b-")
	                    for ch in we_wantt:
	                        ch = ch.lower()
	                        #print(ch,end="")
	                        file.write(ch)
	                    #print(":"+the_row)
	                    file.write(":")
	                    file.write(the_row)
	                    file.write("\n")                    

	file.close()


def c_recs(filename):


	tree = ET.ElementTree(file=filename)
	root = tree.getroot()
	counter = 0
	file = open("recs.txt","w")

	for Em in root:
	    #print(root[counter][0].text+":",end="")
	    mail = Em.tag
	    start = root[counter][0].text+":"+"<"+mail+">"
	    counter += 1
	    #print("<"+mail+">",end="")    #print out the row id and the first tag of mail
	    file.write(start)
	    for attri in Em:
	        # every attributes inside Email
	        first = "<"+attri.tag+">"
	        file.write(first)
	        #print(first,end="")
	        
	        
	        second = attri.text
	        if(second != None):
	            for h in second:    #go through every characters in the <value>
	                if(h != "\n"):   # normal things
	                    #print(h,end='')
	                    file.write(h)
	                    
	                if(h == "\n"):   # switching lines
	                    #print("&#10;",end="")
	                    file.write("&#10;")    
	                    
	                if(h == "<"):   # switching lines
	                    #print("&lt;",end="")
	                    file.write("&lt;")  
	                
	                if(h == ">"):   # switching lines
	                    #print("&gt;",end="")
	                    file.write("&gt;")     
	                    
	                if(h == "&"):   # switching lines
	                    #print("&amp;",end="")
	                    file.write("&amp;")     
	                
	                if(h == "'"):
	                    #print("&apo;",end="")
	                    file.write("&apo;")
	                    
	                if(h == "quot"):
	                    #print('''"''',end="")
	                    file.write('''"''')
	                
	        
	        third = "</"+attri.tag+">"
	        file.write(third)
	        #print(third,end="")
	        
	    fourth = "</"+mail+">"
	    file.write(fourth)
	    file.write("\n")
	    #print(fourth)
	    
	            
	file.close()

def main():
	filename = input("Please enter the XML file :")
	c_dates(filename)
	c_terms(filename)
	c_recs(filename)
	c_emails(filename)

main()

    
            