#from pymongo import MongoClient
#import dns
#import hashlib
#from datetime import date
#client=MongoClient("mongodb+srv://admin-Ayush:vSYzh9RDkmZ8dr0t@cluster0.llgkb.mongodb.net/user?retryWrites=true&w=majority")
#collection=client.user.project
#name='Ayush Kuruvilla'
#password=hashlib.sha256('master@4123'.encode('utf-8')).hexdigest()
#cur=collection.find({'username': name})
#if len(list(cur))==0:
#    print('fail')
#for x in collection.find({'username': name}):
#    if(x['username']=="admin" and x['password']==hashlib.sha256('admin123'.encode('utf-8')).hexdigest()):
#            print('lol')
#    else:
#            print('hello')
#from validate_email import validate_email
#is_valid = validate_email(email_address='example@example.com', check_format=True, check_blacklist=True, check_dns=True, dns_timeout=10, check_smtp=True, smtp_timeout=10, smtp_helo_host='my.host.name', smtp_from_address='my@from.addr.ess', smtp_debug=False)
#print(is_valid)
import models
ob=models.mail()
l=ob.send_email('Ayush', "lolqdwecwdc@gmail.com", "ahem", "ahem")
print(l)