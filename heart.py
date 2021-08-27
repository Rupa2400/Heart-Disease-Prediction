#!/usr/bin/env python
# coding: utf-8

# In[15]:


import pandas as pd
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import warnings 
from sklearn import *
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from tkinter import *
from sqlite3 import *
import os.path
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from PIL import Image, ImageTk
warnings.filterwarnings("ignore")

#functions for buttons
def btRegister(): #register button on register window
    flag = 0
    usern=reg_window_textUsername.get()
    passw=reg_window_textPassword.get()
    if len(usern)<5:
        flag=1
        showerror("Invalid Value", "Username has to be more than 5 characters")
    elif len(passw)<6:
        showerror("Invalid value","Password has to be more than 6 characters")
        flag = 1
    if flag==0:
        try:
            con = None
            con=connect("users.db")
            sql="select * from users where username=? and password=?"
            cursor=con.cursor()
            cursor.execute(sql , (usern,passw))
            results=cursor.fetchone()
            if results:
            	showerror("Error","The username has already been registered")
            else:
                sql="insert into users (username,password) values(?,?)"
                cursor=con.cursor()
                cursor.execute(sql ,(usern,passw))
                con.commit()
                showinfo("Registration Successful","You've been succesfully registered")
                reg_window_textPassword.delete(0,END)
                reg_window_textUsername.delete(0,END)

        except Exception as e:
            showerror("Failure",e)
        finally:
            if con is not None:
                con.close()
def btLogin(): #login button on login widnow
    usern=login_window_textUsername.get()
    passw=login_window_textPassword.get()
    try:
            con = None
            con=connect("users.db")
            sql="select * from users where username='%s' and password='%s'"
            cursor=con.cursor()
            cursor.execute(sql % (usern,passw))
            results=cursor.fetchone()
            if results:
                showinfo("Success","You're logged in successfully '%s'" %usern)
                mod()
                login_window.withdraw()
            else:
                showerror("Error","Error in username or password")
    except Exception as e:
            showerror("Failure",e)
    finally:
            if con is not None:
                con.close()

def viewLogin():
    login_window_textUsername.delete(0,END)
    login_window_textPassword.delete(0,END)
    root.withdraw()
    login_window.deiconify()
def viewReg():
    reg_window_textUsername.delete(0,END)
    reg_window_textPassword.delete(0,END)
    root.withdraw()
    reg_window.deiconify()
def btnBack():
    login_window.withdraw()
    root.deiconify()
def btnBackR():
    reg_window.withdraw()
    root.deiconify()
def Exit():
    root.destroy()

def regExit():
    reg_window.destroy()
    root.deiconify()

def w_Exit():
    print("You've been logged out")
    root.deiconify()

def loginExit():
    login_window.destroy()
    root.deiconify()
#check if users.db exists
if os.path.exists("users.db"):
    pass
else:
    con = None
    con=connect("users.db")
    print("Connected")
    sql="create table users(userid integer primary key autoincrement,username text not null,password text not null)"
    cursor=con.cursor()
    cursor.execute(sql)
    print("Database created for the first time")
    print("table created")


#mainwindow
root=Tk()
root.resizable(False,False)
root.title("Heart Disease Prediction")
root.geometry("405x415+400+200")
root.configure(bg='black')
root.overrideredirect(True)


image1 = Image.open("main.png")
test = ImageTk.PhotoImage(image1)


label1 = Label(image=test,borderwidth=0,relief='flat')
label1.image = test
labeltitle=Label(root,text="Heart Disease Prediction System",font=('Segoe UI',10,'bold'),bg='black',fg='white')


btnLogin=Button(root,text="Login",width=10,font=('Segoe UI',15,'bold'),command=viewLogin,bg='black',fg='white',relief='flat',activeforeground='red',activebackground='black')
btnRegister=Button(root,text="Register",width=10,font=('Segoe UI',15,'bold'),command=viewReg,bg='black',fg='white',relief='flat',activeforeground='red',activebackground='black')


exitimg = Image.open("exit.png")
exitimg=exitimg.resize((20,20),Image.ANTIALIAS)
photoimg=ImageTk.PhotoImage(exitimg)
labeltitle.grid(row=0,column=0,sticky="w")


btnExit=Button(root,height=20,width=20, image = photoimg,command=Exit,bg='black',relief='flat',activebackground='black').grid(row=0,column=2,sticky="e")
label1.grid(row=2,column=0)
btnLogin.grid(row=3,column=0)
btnRegister.grid(row=4,column=0)


#loginwindow
login_window=Toplevel(root)
login_window.configure(bg='black')
login_window.resizable(False,False)

login_window.title("Login")
login_window.geometry("405x220+400+200")
login_window.overrideredirect(True)
logintitle=Label(login_window,text="Heart Disease Prediction System",font=('Segoe UI',10,'bold'),bg='black',fg='white')

login_window_lblusername=Label(login_window,text="Username",font=('Segoe UI',10,'bold'),bg='black',fg='white')
login_window_lblpassword=Label(login_window,text="Password",font=('Segoe UI',10,'bold'),bg='black',fg='white')

login_window_btnLogin=Button(login_window,text="Login",font=('Segoe UI',10,'bold'),command=btLogin,bg='black',fg='white',relief='flat',activeforeground='red',activebackground='black')
login_window_btnBack=Button(login_window,text="Back",font=('Segoe UI',10,'bold'),command=btnBack,bg='black',fg='white',relief='flat',activeforeground='red',activebackground='black')

login_window_textPassword=Entry(login_window,show="*",bd=5,font=('Segoe UI',10,'bold'),bg='black',fg='white',relief='groove')
login_window_textUsername=Entry(login_window,bd=5,font=('Segoe UI',10,'bold'),bg='black',fg='white',relief='groove')


exitimgz = Image.open("exit.png")
exitimgz=exitimgz.resize((20,20),Image.ANTIALIAS)
photoimgz=ImageTk.PhotoImage(exitimgz)

login_window_btnExit=Button(login_window,height=20,width=20, image = photoimgz,command=loginExit,bg='black',relief='flat',activebackground='black').grid(row=0,column=2,sticky="e")
logintitle.grid(row=0,column=0,sticky="w")

login_window_lblusername.grid(row=4,column=0,pady=20,padx=10)
login_window_textUsername.grid(row=4,column=1,pady=20,padx=10)
login_window_textUsername.focus()


login_window_lblpassword.grid(row=5,column=0,pady=20,padx=10)
login_window_textPassword.grid(row=5,column=1,pady=20,padx=10)
login_window_textPassword.focus()


#login_window.bind('<Return>',btLogin())
login_window_btnLogin.grid(row=6,column=0,pady=20,padx=10)
login_window_btnBack.grid(row=6,column=1,padx=10)
login_window.withdraw()


#registerwindow
reg_window=Toplevel(root)
reg_window.configure(bg='black')
reg_window.resizable(False,False)
reg_window.title("Register")
reg_window.geometry("405x220+400+200")
reg_window.overrideredirect(True)

registertitle=Label(reg_window,text="Heart Disease Prediction System",font=('Segoe UI',10,'bold'),bg='black',fg='white')
reg_window_lblusername=Label(reg_window,text="Username",font=('Segoe UI',10,'bold'),bg='black',fg='white')
reg_window_lblpassword=Label(reg_window,text="Password",font=('Segoe UI',10,'bold'),bg='black',fg='white')
reg_window_btnregister=Button(reg_window,text="Register",font=('Segoe UI',10,'bold'),command=btRegister,bg='black',fg='white',relief='flat',activeforeground='red',activebackground='black')
reg_window_btnBack=Button(reg_window,text="Back",font=('Segoe UI',10,'bold'),command=btnBack,bg='black',fg='white',relief='flat',activeforeground='red',activebackground='black')


reg_window_textPassword=Entry(reg_window,show="*",bd=5,font=('Segoe UI',10,'bold'),bg='black',fg='white',relief='groove')
reg_window_textUsername=Entry(reg_window,bd=5,font=('Segoe UI',10,'bold'),bg='black',fg='white',relief='groove')
exitimgr = Image.open("exit.png")
exitimgr=exitimgr.resize((20,20),Image.ANTIALIAS)

photoimgr=ImageTk.PhotoImage(exitimgr)
reg_window_btnExit=Button(reg_window,height=20,width=20, image = photoimgr,command=regExit,bg='black',relief='flat',activebackground='black').grid(row=0,column=2,sticky="e")
registertitle.grid(row=0,column=0,sticky="w")

reg_window_lblusername.grid(row=4,column=0,pady=20,padx=10)
reg_window_textUsername.grid(row=4,column=1,pady=20,padx=10)
reg_window_textUsername.focus()

reg_window_lblpassword.grid(row=5,column=0,pady=20,padx=10)
reg_window_textPassword.grid(row=5,column=1,pady=20,padx=10)
reg_window_textPassword.focus()

#reg_window.bind('<Return>',btRegister())
reg_window_btnregister.grid(row=6,column=0,pady=20,padx=10)
reg_window_btnBack.grid(row=6,column=1,padx=10)
reg_window.withdraw()


def mod():
    def heart_disease(new_input):
        df=pd.read_csv(r"dataset.csv")
        df.count().isnull()
        df.describe()
        x= df.drop('target',axis=1)
        y=df['target']
        model= ExtraTreesClassifier()
        model.fit(x,y)
        feat_importances = pd.Series(model.feature_importances_, index=x.columns)
        randomforest_classifier= RandomForestClassifier(n_estimators=100)
        score=cross_val_score(randomforest_classifier,x,y,cv=15)
        acc=score.mean()
        op=model.predict(new_input)
        com=[op,acc]
        return com


    window = Toplevel(root)
    window.geometry('690x550+400+200')
    window.overrideredirect(True)
    window.configure(bg='black')
    titlez=Label(window,text="Heart Disease Prediction System",font=('Segoe UI',10,'bold'),bg='black',fg='white').grid(row=0,column=1,sticky="w")
    w_btnExit=Button(window,height=20,width=20, image = photoimgr,command=lambda:[window.destroy(),w_Exit()],bg='black',relief='flat',activebackground='black').grid(row=0,column=3,sticky="e")
    

    lbl = Label(window, text="Enter the following parameters",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=2, row=1,padx=10,pady=10)


    lbl = Label(window, text="Age",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=2)
    
    
    age = Entry(window,width=20,bg='black',fg='white')
    age.grid(column=3, row=2)
    age.focus()
    


    lbl = Label(window, text="Gender(m=1,f=0)",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=3)
    
    sex = Entry(window,width=20,bg='black',fg='white')
    sex.grid(column=3, row=3)
    sex.focus()

    lbl = Label(window, text="BMI",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=4)
    
    bmi = Entry(window,width=20,bg='black',fg='white')
    bmi.grid(column=3, row=4)
    bmi.focus()


    lbl = Label(window, text="Chest Pain Level(0-3)",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=5)
    
    cp = Entry(window,width=20,bg='black',fg='white')
    cp.grid(column=3, row=5)
    cp.focus()

    


    lbl = Label(window, text="Systolic Blood Pressure(mm Hg)",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=6)
    
    bps = Entry(window,width=20,bg='black',fg='white')
    bps.grid(column=3, row=6)
    bps.focus()


    lbl = Label(window, text="Diastolic Blood Pressure(mm Hg)",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=7)
    
    dp = Entry(window,width=20,bg='black',fg='white')
    dp.grid(column=3, row=7)
    dp.focus()


    lbl = Label(window, text="Cholesterol (mg/dl)",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=8)
    
    chol = Entry(window,width=20,bg='black',fg='white')
    chol.grid(column=3, row=8)
    chol.focus()


    lbl = Label(window, text="(Fasting Sugar Blood > 120 mg/dl) (1 = true; 0 = false)",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=9)
    
    fbs = Entry(window,width=20,bg='black',fg='white')
    fbs.grid(column=3, row=9)
    fbs.focus()


    lbl = Label(window, text="resting electrocardiographic results",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=10)
    
    ecg = Entry(window,width=20,bg='black',fg='white')
    ecg.grid(column=3, row=10)
    ecg.focus()


    lbl = Label(window, text="maximum heart rate achieved",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=11)
    
    mhr = Entry(window,width=20,bg='black',fg='white')
    mhr.grid(column=3, row=11)
    mhr.focus()


    lbl = Label(window, text="exercise induced angina (1 = yes; 0 = no)",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=12)
    
    eia = Entry(window,width=20,bg='black',fg='white')
    eia.grid(column=3, row=12)
    eia.focus()


    lbl = Label(window, text="ST depression induced by exercise relative to rest",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=13)
    
    st = Entry(window,width=20,bg='black',fg='white')
    st.grid(column=3, row=13)
    st.focus()


    lbl = Label(window, text="the slope of the peak exercise ST segment",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=14)

    slope = Entry(window,width=20,bg='black',fg='white')
    slope.grid(column=3, row=14)
    slope.focus()


    lbl = Label(window, text="number of major vessels (0-3) colored by flourosopy",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=15)
    
    ca = Entry(window,width=20,bg='black',fg='white')
    ca.grid(column=3, row=15)
    ca.focus()


    lbl = Label(window, text=" A blood disorder called thalassemia \n (3 = normal; 6 = fixed defect; 7 = reversable defect)",font=('Segoe UI',10,'bold'),bg='black',fg='white')
    lbl.grid(column=1, row=16)
    
    thal = Entry(window,width=20,bg='black',fg='white')
    thal.grid(column=3, row=16)
    thal.focus()

    
    def calculate():
        new_input=[age.get(),sex.get(),cp.get(),bps.get(),chol.get(),fbs.get(),ecg.get(),mhr.get(),eia.get(),st.get(),slope.get(),ca.get(),thal.get()]

    #     listToStr = ' ,'.join(map(str, new_input)) 
    #     inp.configure(text= "you entered: "+listToStr )
        new_input= np.reshape(new_input,(1,-1))
        d=heart_disease(new_input)
        ans=d[0]
        #score=cross_val_score(randomforest_classifier,x,y,cv=15)
        sc=str(d[1]*100)

        if(ans==1):
            s='You have a Heart Disease'
            ot.configure(fg='red')
        else:
            s="You are in perfect health"
            ot.configure(fg='green')
        ot.configure(text="Result: " + s + "\n(accuracy ="+ sc +"% )" )
        ot.grid(column=1, row=18)

    #window.bind('<Return>', calculate)
    btn = Button(window, text="submit",command=calculate,font=('Segoe UI',10,'bold'),bg='black',fg='white',activebackground='black',activeforeground='red',relief='flat')
    btn.grid(column=3, row=17)
    ot = Label(window, text="",font=('Segoe UI',10,'bold'),bg='black',fg='white',relief=RAISED)
    ot.grid_forget()
    


        
root.mainloop()



