from pymongo import MongoClient
import dns
client=MongoClient("mongodb+srv://admin-Ayush:vSYzh9RDkmZ8dr0t@cluster0.llgkb.mongodb.net/user?retryWrites=true&w=majority")
collection2=client.user.deets
x=collection2.find({"username":"Ayush Kuruvilla"})
if len(list(x))==0:
    print("Empty")
