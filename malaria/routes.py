from flask import Flask, render_template, request, redirect,  flash, abort, url_for

from malaria import app,mail

from malaria.models import *

from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from PIL import Image
from flask_mail import Message
from datetime import datetime,date







@app.route('/',methods=['GET','POST'])
def index():
    return render_template("index.html")


@app.route('/about',methods=['GET','POST'])
def about():
    return render_template("about.html")

@app.route('/services',methods=['GET','POST'])
def services():
    return render_template("services.html")    


@app.route('/con',methods=['GET','POST'])
def con():
  

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        text = request.form['message']
        my_data = contact(name=name,email=email,number=number,text=text)
        db.session.add(my_data) 
        db.session.commit()
        f="Message Sent Successfully"
        return render_template("cont.html",f=f)
    return render_template("cont.html")



def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


@app.route('/feedback',methods=['GET','POST'])
def feedback():
    c=registration.query.filter_by(id=current_user.id).first()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        text = request.form['message']
        my_data = contact(name=name,email=email,number=number,text=text)
        db.session.add(my_data) 
        db.session.commit()
        f="Message Sent Successfully"
        return render_template("feedback.html",f=f,c=c)
    return render_template("feedback.html",c=c)



@login_required
@app.route('/feedbackview',methods=["GET","POST"])
def feedbackview():
    obj = contact.query.all()
    return render_template("feedbackview.html",obj=obj) 




@login_required
@app.route('/take_test',methods=["GET","POST"])
def take_test():
    obj = registration.query.filter_by(usertype="patient",lid=current_user.id).all()
    return render_template("take_test.html",obj=obj) 


@login_required
@app.route('/test_rep/<int:id>',methods=["GET","POST"])
def test_rep(id):
    r=registration.query.filter_by(id=id).first()
    obj = Test.query.filter_by(uid=r.id).all()
    
    return render_template("test_rep.html",obj=obj,r=r) 



@login_required
@app.route('/atest_rep/<int:id>',methods=["GET","POST"])
def atest_rep(id):
    r=registration.query.filter_by(id=id).first()
    obj = Test.query.filter_by(uid=r.id).all()
    
    return render_template("atest_rep.html",obj=obj,r=r) 


@login_required
@app.route('/ptest_rep/<int:id>',methods=["GET","POST"])
def ptest_rep(id):
    r=registration.query.filter_by(id=id).first()
    obj = Test.query.filter_by(uid=r.id).all()
    
    return render_template("ptest_rep.html",obj=obj,r=r) 


@login_required
@app.route('/a_rep/<int:id>',methods=["GET","POST"])
def a_rep(id):
    t = Test.query.filter_by(id=id).first()
    p=registration.query.filter_by(id=t.uid).first()
    
    
    return render_template("a_rep.html",t=t,p=p) 


@login_required
@app.route('/l_rep/<int:id>',methods=["GET","POST"])
def l_rep(id):
    t = Test.query.filter_by(id=id).first()
    p=registration.query.filter_by(id=t.uid).first()
    
    
    return render_template("l_rep.html",t=t,p=p) 


@login_required
@app.route('/p_rep/<int:id>',methods=["GET","POST"])
def p_rep(id):
    t = Test.query.filter_by(id=id).first()
    p=registration.query.filter_by(id=t.uid).first()
    
    
    return render_template("p_rep.html",t=t,p=p) 






@login_required
@app.route('/viewpatient',methods=["GET","POST"])
def viewpatient():
    obj = registration.query.filter_by(usertype="patient").all()
    
    return render_template("viewpatient.html",obj=obj)

@login_required
@app.route('/viewpatient_for_labtec',methods=["GET","POST"])
def viewpatient_for_labtec():
    obj = registration.query.filter_by(usertype="patient",lid=current_user.id).all()
    return render_template("viewpatient_for_labtec.html",obj=obj)


@login_required
@app.route('/viewlabtec',methods=["GET","POST"])
def viewlabtec():
    obj = registration.query.filter_by(usertype="labtec").all()
    return render_template("viewlabtec.html",obj=obj)




@app.route('/labtec_reg',methods=['GET','POST'])
def labtec_reg():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address=request.form['address']
        number = request.form['number']
        password = request.form['password']
        # confirm_password = request.form['confirm_password']
        my_data = registration(name=name,email=email,number=number,address=address,dob=password,password=password,usertype="labtec")
        db.session.add(my_data) 
        db.session.commit()
        # ad_sendmail(email,password)
        return redirect('/viewlabtec')
    return render_template("labtec_reg.html")



# def ad_sendmail(email,password):
#     msg = Message(' Successfully Added',recipients=[email])
#     msg.body = f''' You can login using your Email ID and  Your Password is, {password}  '''
#     mail.send(msg)



@app.route('/patient_reg',methods=['GET','POST'])
def patient_reg():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address=request.form['address']
        number = request.form['number']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        # confirm_password = request.form['confirm_password']
        my_data = registration(name=name,age=age,gender=gender,email=email,lid=current_user.id,number=number,address=address,password=password,dob=password,usertype="patient")
        db.session.add(my_data) 
        db.session.commit()
        # ad_sendmail(email,password)
        return redirect('/viewpatient_for_labtec')
    return render_template("patient_reg.html")





@app.route('/delete_user/<int:id>', methods = ['GET','POST'])
def delete_user(id):

    delet = registration.query.get_or_404(id)
    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/viewlabtec')
    except:
        return 'There was a problem deleting that task'




@app.route('/delete_us/<int:id>', methods = ['GET','POST'])
def delete_us(id):

    delet = registration.query.get_or_404(id)
    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/viewpatient_for_labtec')
    except:
        return 'There was a problem deleting that task'       




@app.route('/editpatient_forlabtec/<int:id>',methods=["GET","POST"])
def editpatient_forlabtec(id):
    c= registration.query.get_or_404(id)
    if request.method == 'POST':
        c.name =  request.form['name']
        c.address =  request.form['address']
        c.email =  request.form['email']
        c.number =  request.form['number']
        c.age =  request.form['age']
        c.gender =  request.form['gender']
        db.session.commit()
        return redirect('/viewpatient_for_labtec')
    else:
        return render_template('editpatient_forlabtec.html',c=c)


@app.route('/editpatient/<int:id>',methods=["GET","POST"])
def edit_patient(id):
    c= registration.query.get_or_404(id)
    if request.method == 'POST':
        c.name =  request.form['name']
        c.address =  request.form['address']
        c.email =  request.form['email']
        c.number =  request.form['number']
        db.session.commit()
        return redirect('/viewpatent')
    else:
        return render_template('editpatient.html',c=c)        


@app.route('/editlabtec/<int:id>',methods=["GET","POST"])
def edit_labtec(id):
    c= registration.query.get_or_404(id)
    if request.method == 'POST':
        c.name =  request.form['name']
        c.address =  request.form['address']
        c.email =  request.form['email']
        c.number =  request.form['number']
        db.session.commit()
        return redirect('/viewlabtec')
    else:
        return render_template('editlabtec.html',c=c)   


@app.route('/lab_profile',methods=["GET","POST"])
def lab_profile():
    c= registration.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        c.name =  request.form['name']
        c.address =  request.form['address']
        c.email =  request.form['email']
        c.number =  request.form['number']
        db.session.commit()
        f="Profile Updated Successfully"
        return render_template('lprofile.html',f=f,c=c)
    else:
        return render_template('lab_profile.html',c=c)  


@app.route('/change_pass',methods=["GET","POST"])
def change_pass():
    c= registration.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        password =  request.form['password']
        cpass =  request.form['cpass']
        if password==cpass:
            c.password=password
            db.session.commit()
            flash('Password Updated Successfully.You can Login using New Password')
            return redirect('/login')
            
        else:
            f="Password Not Match"
            return render_template('change_pass.html',c=c,f=f)  

        
    else:
        return render_template('change_pass.html',c=c)  




@app.route('/pchange_pass',methods=["GET","POST"])
def pchange_pass():
    c= registration.query.filter_by(id=current_user.id).first()
    if request.method == 'POST':
        password =  request.form['password']
        cpass =  request.form['cpass']
        if password==cpass:
            c.password=password
            db.session.commit()
            flash('Password Updated Successfully.You can Login using New Password')
            return redirect('/login')
            
        else:
            f="Password Not Match"
            return render_template('pchange_pass.html',c=c,f=f)  

        
    else:
        return render_template('pchange_pass.html',c=c)  


@app.route('/lprofile',methods=["GET","POST"])
def lprofile():
    c= registration.query.filter_by(id=current_user.id).first()
    return render_template('lprofile.html',c=c) 



@app.route('/userpage/<int:id>',methods=['GET','POST'])
def userpage(id):
    return render_template("userpage.html")


@app.route('/adminpage',methods=['GET','POST'])
def adminpage():
    return render_template("adminpage.html")

@app.route('/adminlayout',methods=['GET','POST'])
def adminpagelayout():
    return render_template("adminpagelayout.html")

@app.route('/labtecpage/<int:id>',methods=['GET','POST'])
def labtecpage(id):
    return render_template("labtecpage.html")

@app.route('/labteclayout',methods=['GET','POST'])
def labtecpagelayout():
    return render_template("labteclayout.html")
   

@app.route('/patientpage/<int:id>',methods=['GET','POST'])
def patientpage(id):
    return render_template("patientpage.html")

@app.route('/patientlayout',methods=['GET','POST'])
def patientpagelayout():
    return render_template("patientlayout.html")



@app.route('/login', methods=["GET","POST"])
def login():

   
    if request.method=="POST":
         username=request.form['email']
         password=request.form['password']
         admin = registration.query.filter_by(email=username, password=password,usertype='admin').first()

         
         labtec=registration.query.filter_by(email=username, password=password, usertype='labtec').first() or registration.query.filter_by(email=username, dob=password, usertype='labtec').first()
         
         patient=registration.query.filter_by(email=username,password=password, usertype='patient').first() or registration.query.filter_by(email=username, dob=password, usertype='patient').first()

         if admin:
             login_user(admin)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/adminpage') 
         
         elif labtec:
             login_user(labtec)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/labtecpage/'+str(labtec.id)) 

         elif patient:
             login_user(patient)
             next_page = request.args.get('next')
             return redirect(next_page) if next_page else redirect('/patientpage/'+str(patient.id)) 
         

         else:
             d="Invalid Username or Password!"
             return render_template("login.html",d=d)
    return render_template("login.html")



@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')

  