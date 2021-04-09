from datetime import date
import smtplib, ssl
import re
import imghdr
from email.message import EmailMessage
class details():
    def __init__(self,col, u_name):
        self.uname =u_name
        self.col=col

    def insert_details(self,source_loc,num_people,budget):
        budget=int(budget)
        self.col.insert_one({"username":self.uname,"source":source_loc,"budget":budget,"travellers":num_people})
    
    def view_details(self):
        i=self.col.find({"username":self.uname})
        return i
	
    def delete_details(self):
        self.col.delete_one({"username":self.uname})
        return
	
    def update_details(self,source_loc,num_people,budget):
        budget=int(budget)
        self.col.update({"username":self.uname},{"username":self.uname,"source":source_loc,"budget":budget,"travellers":num_people})

class feed(details):
    def __init__(self,col, u_name):
        details.__init__(self,col, u_name)
        self.uname =u_name
        self.col=col
    
    def insert_details(self,sub,con):
        today = date.today()
        d2 = today.strftime("%B %d, %Y")
        self.col.insert_one({"username":self.uname,"date":d2,"subject":sub,"desc":con})


class check():
    def __init__(self):
        pass
    def check_username(self,inp):
        regex = re.compile('[@_!#$%^&*()<>?/|}{~:"]')
        if inp.isdigit():
            return"Username cannot be digits alone,Enter valid username"
        elif inp[0].isdigit():
            return"Enter valid username"
        elif regex.search(inp) != None:
            return"Special characters not allowed"
        else:
            return True
    def check_email(self,email):
        regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
        if(re.search(regex,email)):   
            return True
        else:   
            return"Invalid Email"  

class mail():
    def __init__(self):
        pass
    def send_email(self,name,receiver_email,sub,con):
        sender_email = 'copperswitch839@gmail.com'
        password=""
        msg = EmailMessage()
        msg['Subject'] = sub
        msg['From'] = receiver_email
        msg['To'] = sender_email
        msg.set_content(con)
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(sender_email,password)
                smtp.send_message(msg)
        except:
            return "Email does not exist"

