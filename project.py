from easygui import *
import MySQLdb

p=MySQLdb.connect('kali','root','','LIBSYS')
cur=p.cursor()    
title='Library Management System'
res=''
##########################################################################################################################################
#code for the student login
def student_login():
    usrname=enterbox('Enter the Username',title)
    passwd=passwordbox('Enter password',title)
    query="SELECT LOGID FROM STUDENT_LOGIN WHERE USERNAME="+`usrname`+" AND PASSWORD="+`passwd`
 
    try:
        cur.execute(query)
        getid=cur.fetchone()
        sid=getid[0]            #get the userid into a sid variable and use this id to do any operation on the database
        msgbox('Login Sucessful for '+sid,title)
        query="SELECT B.BOOKNAME,BI.* FROM BOOKSISSUED BI,BOOK B WHERE BI.BOOKID=B.CODE AND STUID="+`sid`
        cur.execute(query)
        print query
        rows=cur.fetchone()
        res=''
        if(rows==None):
            msgbox("No books have been borrowed")
            return
        else:
           cur.execute(query)
        
           rows=cur.fetchall()
           for row in rows:
               for i in row:
                   res=res+"\t\t"+`i`
               res=res+"\n"
        
        textbox("Query Result",title,res)

    except:
            exceptionbox()
##########################################################################################################################################


def librarian():
 password='tameem'
 title='Library Management System'
 if(passwordbox('Hello Librarian enter password to continue',title)=='tameem'):
   while 1: 
    msg='Choose What you want to do'
    title='Library Management System'
    choices=['Insert New book detais','Enter New Student details','Enter new teacher details','Exchange books','Exit']
    choice=indexbox(msg,title,choices)
    if choice==1:
        while 1:
            msg='Enter new Student details'
            title='Library Management System'
            feildnames=['Reg No.','Name','Branch','Semester','Section','Year of Admission(yyyy)']
            feildvalues=[]
            feildvalues=multenterbox(msg,title,feildnames)
            
            while 1:
                if feildvalues == None: break
                errmsg = ""
                for i in range(len(feildnames)):
                    if feildvalues[i].strip() == "":
                        errmsg = errmsg + ('"%s" is a required field.\n\n' % feildnames[i])
                if errmsg == "": break # no problems found
                feildvalues = multenterbox(errmsg, title, feildnames, feildvalues)
            print "Reply was:", feildvalues


            try:
               cur.execute("INSERT INTO STUDENT(REGNO,NAME,BRANCH,SEMESTER,SECTION,YEAR_OF_ADM,NO_OF_BOOKS_BORROWED) VALUES(%s,%s,%s,%s,%s,%s,%s)", (feildvalues[0],feildvalues[1],feildvalues[2],feildvalues[3],feildvalues[4],feildvalues[5],'0'))
            except:
               msgbox('Improper Entries detected')
            if ccbox('Do you want to continue the entry',title)==0: break

#################
    if choice==0:
        while 1:
            msg='Enter New book details'
            title='Library Management System'
            feildnames=['Book Code','Book Name','Author','Publications','Subject']
            feildvalues=[]
            feildvalues=multenterbox(msg,title,feildnames)
            
            while 1:
                if feildvalues == None: break
                errmsg = ""
                for i in range(len(feildnames)):
                    if feildvalues[i].strip() == "":
                        errmsg = errmsg + ('"%s" is a required field.\n\n' % feildnames[i])
                if errmsg == "": break # no problems found
                feildvalues = multenterbox(errmsg, title, feildnames, feildvalues)
            print "Reply was:", feildvalues


            try:
               cur.execute("INSERT INTO BOOK(CODE,BOOKNAME,AUTHOR,PUBLICATION,SUBJECT) VALUES(%s,%s,%s,%s,%s)", (feildvalues[0],feildvalues[1],feildvalues[2],feildvalues[3],feildvalues[4]))
            except:
               exceptionbox()
               
            if ccbox('Do you want to continue the entry',title)==0: break


#######################################


    if choice==2:
        while 1:
            msg='Enter New teacher details'
            title='Library Management System'
            feildnames=['Teacher ID','Name','Designation','Branch','Contact No.','Lectures']
            feildvalues=[]
            feildvalues=multenterbox(msg,title,feildnames)
            
            while 1:
                if feildvalues == None: break
                errmsg = ""
                for i in range(len(feildnames)):
                    if feildvalues[i].strip() == "":
                        errmsg = errmsg + ('"%s" is a required field.\n\n' % feildnames[i])
                if errmsg == "": break # no problems found
                feildvalues = multenterbox(errmsg, title, feildnames, feildvalues)
            print "Reply was:", feildvalues


            try:
               cur.execute("INSERT INTO TEACHER(TID,NAME,DESIGNATION,BRANCH,CONTACT_NO,LECTURES,NO_OF_BOOKS_BORROWED) VALUES(%s,%s,%s,%s,%s,%s)", (feildvalues[0],feildvalues[1],feildvalues[2],feildvalues[3],feildvalues[4],feildvalues[5],'0'))
            except:
               exceptionbox()
               
            if ccbox('Do you want to continue the entry',title)==0: break


#######################################

#ISSUE CODE
    if choice==3:
     msg='What would you like to do'
     choices=['Issue book to a student','Return book from a student','Issue book to a teacher','Return book from teacher','Exit']
     choice=indexbox(msg,'Library Management System',choices)
     
     if choice==0:
       res=''
       raw=enterbox('Enter the USN of the student')
       if raw=='':
           msgbox("Please provide an input","Library Management System")
           continue
       
       query="SELECT REGNO FROM STUDENT WHERE REGNO="+`raw`
       try:
           cur.execute(query) 
           sid=cur.fetchone()
           print 'USN '+`sid[0]`+' Selected'
       except:
           exceptionbox()
       
       
       while 1: 
        try:
            cur.execute(query) 
            sid=cur.fetchone()
            print 'USN '+`sid[0]`+' Selected'
            bksborrowed="SELECT NO_OF_BOOKS_BORROWED FROM STUDENT WHERE REGNO="+`sid[0]`
            maxbooks="SELECT BORROW_LIMIT FROM STUDENT_LOGIN WHERE LOGID="+`sid[0]`
            print bksborrowed
            print maxbooks
            try:
                 cur.execute(bksborrowed)
                 ch1=cur.fetchone()
            except:
                 exceptionbox()
               
    
            try:
                cur.execute(maxbooks)
                ch2=cur.fetchone()
            except:
                exceptionbox()
            print ch1[0]
            
               
         
    
            if ch1[0]==ch2[0]:
                msgbox('Limit reached')
            else:
                bkid=enterbox('Enter the id of the book to be issued:')
                d1=enterbox('Enter the issue date:')
                d2=enterbox('Enter the date at which the book is to be returned:')
                cur.execute("INSERT INTO BOOKSISSUED (BOOKID,STUID,ISSUE_DATE,RETURN_DATE) VALUES (%s,%s,%s,%s)",(bkid,sid[0],d1,d2))
                UPD1="UPDATE STUDENT SET NO_OF_BOOKS_BORROWED=NO_OF_BOOKS_BORROWED+1 WHERE REGNO="+`sid[0]`
                cur.execute(UPD1)
                cur.execute("SELECT *FROM BOOKSISSUED")
                rows=cur.fetchall()
                for row in rows:  
                     res=res+`row`+'\n'
                print res
                
                  
            if ccbox('Select continue to issue other books to other/same student')==0: break               

   

        except:
            exceptionbox()
        
     if choice==1:
               res=''
               raw=enterbox('Enter the USN of the student')
               query="SELECT REGNO FROM STUDENT WHERE REGNO="+`raw`
               try:
                   cur.execute(query) 
               except:
                   exceptionbox()
               sid=cur.fetchone()
               bkid=enterbox('Enter the id of the book to be returned:')
               QUE="SELECT BOOKID FROM BOOKSISSUED"
               UPD3="UPDATE STUDENT SET NO_OF_BOOKS_BORROWED=NO_OF_BOOKS_BORROWED-1 WHERE REGNO="+`sid[0]`
               DEL="DELETE FROM BOOKSISSUED WHERE BOOKID="+`bkid`

               try:
                   cur.execute(DEL)
                   
                                    
               except:
                   exeptionbox()
                   
               if (cur.fetchone()==None):
                   print "Transaction successful"
                   return
               else:
                   print 'Book not found'
                   
               
    	
     if choice==2:
       raw=enterbox('Enter the ID number of the teacher')
       query="SELECT TID FROM TEACHER WHERE TID="+`raw`
      
       while 1: 
        res=''
        try:
            cur.execute(query) 
            tid=cur.fetchone()
            print 'Teacher '+`tid[0]`+' Selected'
            bksborrowed="SELECT NO_OF_BOOKS_BORROWED FROM TEACHER WHERE TID="+`tid[0]`
            maxbooks="SELECT BORROW_LIMIT FROM TEACHER_LOGIN WHERE LOGIN_ID="+`tid[0]`
            print bksborrowed
            print maxbooks
            try:
                 cur.execute(bksborrowed)
                 ch1=cur.fetchone()
            except:
                 exceptionbox()
               
    
            try:
                cur.execute(maxbooks)
                ch2=cur.fetchone()
            except:
                exceptionbox()
            print ch1[0]
            
               
         
    
            if ch1[0]==ch2[0]:
                msgbox('Limit reached')
            else:
                
                bkid=enterbox('Enter the id of the book to be issued:')
                d1=enterbox('Enter the issue date:')
                d2=enterbox('Enter the date at which the book is to be returned:')
                cur.execute("INSERT INTO BOOKSISSUED (BOOKID,STUID,ISSUE_DATE,RETURN_DATE) VALUES (%s,%s,%s,%s)",(bkid,tid[0],d1,d2))
                UPD1="UPDATE TEACHER SET NO_OF_BOOKS_BORROWED=NO_OF_BOOKS_BORROWED+1 WHERE TID="+`tid[0]`
                cur.execute(UPD1)
                cur.execute("SELECT *FROM BOOKSISSUED")
                rows=cur.fetchall()
                for row in rows:  
                     res=res+`row`+"\n"
                print res
                
                  
            if ccbox('Select continue to issue other books to other/same teacher')==0: break               

   

        except:
            exceptionbox()
        
     if choice==3:
               title="Library Management System"
               raw=enterbox('Enter the ID number of the teacher')
               query="SELECT TID FROM TEACHER WHERE TID="+`raw`
               cur.execute(query)
               tid=cur.fetchone()
               print `tid[0]`+"selected"	
               bkid=enterbox('Enter the id of the book to be returned:')
               QUE="SELECT BOOKID FROM BOOKSISSUED"
               DEL="DELETE FROM BOOKSISSUED WHERE BOOKID="+`bkid`
               UPD3="UPDATE TEACHER SET NO_OF_BOOKS_BORROWED=NO_OF_BOOKS_BORROWED-1 WHERE tid="+`tid[0]`
               
               try:
                   cur.execute(DEL)
                   if(cur.fetchone()==None):
                       msgbox("Book Not found",title)
                       continue
                   else:
                       cur.execute(UPD3)  
                       continue
               except:
                   exeptionbox()
                   
               msgbox("Transaction Sucessful",title)
     if choice==4:
         return
#########################################################################################################################################
	
    if choice==4:
        break   
 else:
     msgbox('WRONG PASSWORD!!!',title)
    

##########################################################################################################################################       
def teacher_login():
    usrname=enterbox('Enter the Username')
    passwd=passwordbox('Enter password')
    query="SELECT LOGIN_ID FROM TEACHER_LOGIN WHERE USERNAME="+`usrname`+" AND PASSWORD="+`passwd`
 
    try:
        cur.execute(query)
        getid=cur.fetchone()
        sid=getid[0]            #get the userid into a sid variable and use this id to do any operation on the database
        print 'Login Sucessful for '+sid
        query="SELECT B.BOOKNAME,BI.* FROM BOOKSISSUED BI,BOOK B WHERE BI.BOOKID=B.CODE AND STUID="+`sid`
        cur.execute(query)
        rows=cur.fetchone()
        if rows==None:
            print "No books borrowed"
            return

        cur.execute(query)
        rows=cur.fetchall()
        res=''
        for row in rows:
                    for i in row:
                        res=res+"\t\t"+`i`
                    res=res+"\n"
        textbox("Query Result","Library Management System",res)
        return
    except:
           exceptionbox()

##########################################################################################################################################
def ADMIN():
    global cur
    passwd='tameem'
    title='Library Management System'
    
    if(passwordbox('Hi Admin enter your password to login into admin account','Authorization Login')==passwd):
        msg='Here are a few choices'
        choices= ['1.Write your own MySQLdb query','2.Enter the Student login details','3.Enter the teacher login details','4.Cancel','5.Drop the entire database and create new tables']
        while 1:
            choice=indexbox('Choose what you Want to do',title,choices)
        
            if choice==0:
                query=enterbox('Enter your query\n',title)
                if query=='':
                    msgbox('Please give an input','Library Management System')
                    continue
                res=''
                cur.execute(query)
                rows=cur.fetchall()
                for row in rows:
                    for i in row:
                        res=res+"\t\t"+`i`
                    res=res+"\n"
                   
                textbox('Query Result',title,res)
                res=''

            if choice==1:
                while 1:
                    msg='Enter New Student login details'
                    
                    feildnames=['Login ID','User Name','Password','Borrow limit']
                    feildvalues=[]
                    feildvalues=multenterbox(msg,title,feildnames)
              
                    while 1:
                        if feildvalues == None: break
                        errmsg = ""
                        for i in range(len(feildnames)):
                            if feildvalues[i].strip() == "":
                                errmsg = errmsg + ('"%s" is a required field.\n\n' % feildnames[i])
                        if errmsg == "": break # no problems found
                        feildvalues = multenterbox(errmsg, title, feildnames, feildvalues)
                    print "Reply was:", feildvalues


                    try:
                        cur.execute("INSERT INTO STUDENT_LOGIN(LOGID,USERNAME,PASSWORD,BORROW_LIMIT) VALUES(%s,%s,%s,%s)", (feildvalues[0],feildvalues[1],feildvalues[2],feildvalues[3]))
                    except:
                        exceptionbox()
               
                    if ccbox('Do you want to continue the entry',title)==0: break

########################################
            if choice==2:
                while 1:
                    msg='Enter New Teacher login details'
                    
                    feildnames=['Login ID','User Name','Password','Borrow limit']
                    feildvalues=[]
                    feildvalues=multenterbox(msg,title,feildnames)
              
                    while 1:
                        if feildvalues == None: break
                        errmsg = ""
                        for i in range(len(feildnames)):
                            if feildvalues[i].strip() == "":
                                errmsg = errmsg + ('"%s" is a required field.\n\n' % feildnames[i])
                        if errmsg == "": break # no problems found
                        feildvalues = multenterbox(errmsg, title, feildnames, feildvalues)
                    print "Reply was:", feildvalues


                    try:
                        cur.execute("INSERT INTO TEACHER_LOGIN(LOGIN_ID,USERNAME,PASSWORD,BORROW_LIMIT) VALUES(%s,%s,%s,%s)", (feildvalues[0],feildvalues[1],feildvalues[2],feildvalues[3]))
                    except:
                        exceptionbox()
               
                    if ccbox('Do you want to continue the entry',title)==0: break


##############################################

            if choice==3:#exit
                break
     
            if choice==4:
                
                if(passwordbox("Enter your password","Library Management System")=='tameem'):
                    msgbox("PRESSING OK IN THE NEXT DIALOG BOX WILL ERASE ALL DATA!!!","CAUTION")
                    if(ccbox("I HERE BY CONFIRM THAT I'M RESPONSIBLE FOR THE DATABASE DELETION","CAUTION!!!")==0):
                         break
                    else:
                         cur.execute("DROP DATABASE IF EXISTS LIBSYS")
                         cur.execute("CREATE DATABASE LIBSYS")
                         p=MySQLdb.connect('kali','root','','LIBSYS')
                         cur=p.cursor(); 
                         cur.execute("CREATE TABLE BOOK(CODE INT(11) PRIMARY KEY AUTO_INCREMENT,BOOKNAME VARCHAR(255),AUTHOR VARCHAR(255),PUBLICATION VARCHAR(255),SUBJECT VARCHAR(255))")
                         cur.execute("CREATE TABLE STUDENT(REGNO VARCHAR(10) PRIMARY KEY,NAME VARCHAR(100) NOT NULL,BRANCH VARCHAR(50),SEMESTER VARCHAR(10),SECTION VARCHAR(2),YEAR_OF_ADM INT(4),NO_OF_BOOKS_BORROWED INT(1))")
                         cur.execute("CREATE TABLE TEACHER(TID VARCHAR(11) NOT NULL PRIMARY KEY,NAME VARCHAR(255),DESIGNATION VARCHAR(255),BRANCH VARCHAR(10),CONTACT_NO INT(13),LECTURES VARCHAR(30),NO_OF_BOOKS_BORROWED INT)")
                         cur.execute("CREATE TABLE BOOKSISSUED(BOOKID INT(11) REFERENCES BOOK(CODE) ON DELETE CASCADE,STUID VARCHAR(10) REFERENCES STUDENT(REGNO) ON DELETE CASCADE,ISSUE_DATE DATE,RETURN_DATE DATE)")
                         cur.execute("CREATE TABLE STUDENT_LOGIN(LOGID VARCHAR(10) REFERENCES STUDENT(REGNO) ON DELETE CASCADE,USERNAME VARCHAR(255) NOT NULL,PASSWORD VARCHAR(255) NOT NULL,BORROW_LIMIT INT(1))")
                         cur.execute("CREATE TABLE TEACHER_LOGIN(LOGIN_ID VARCHAR(11) NOT NULL,USERNAME VARCHAR(255) NOT NULL,PASSWORD VARCHAR(100) NOT NULL,FOREIGN KEY (LOGIN_ID) REFERENCES TEACHER(TID) ON DELETE CASCADE,BORROW_LIMIT INT)")
                    
                
                
                
                
            if ccbox('Press continue if you have Some thing else to be done',title)==0: break
            
    else:
        print 'WRONG PASSWORD!!!'    


while 1:
    msg='Hello! choose who you are'
    choices=['Student','Teacher','Admin','Librarian','Exit']
    choice=indexbox(msg,title,choices)
    if choice==0:
        student_login()
    if choice==1:
        teacher_login()
    if choice==2:
        ADMIN() 
    if choice==3:
        librarian()
    if choice==4:
       break
           
p.commit()
