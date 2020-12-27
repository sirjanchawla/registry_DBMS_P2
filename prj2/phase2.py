import os

def c_recs():
    os.system("sort -u recs.txt -o recs.txt|perl break.pl < recs.txt| db_load -T -t hash re.idx")
    
def c_terms():
    os.system("sort -u terms.txt -o terms.txt|perl break.pl < terms.txt| db_load -T -t btree -c duplicates=1 te.idx")
    
def c_dates():
    os.system("sort -u dates.txt -o dates.txt|perl break.pl < dates.txt| db_load -T -t btree -c duplicates=1 da.idx")
    
def c_emails():
    os.system("sort -u emails.txt -o emails.txt|perl break.pl < emails.txt| db_load -T -t btree -c duplicates=1 em.idx")
   
def main():
    c_recs()
    c_terms()
    c_dates()
    c_emails()
main()
    