import functools
import os
import random

from flask import *
from werkzeug.utils import secure_filename

from src.dbconnection import *

app = Flask(__name__)
app.secret_key="1234"

def login_required(func):
	@functools.wraps(func)
	def secure_function():
		if "lid" not in session:
			return render_template('login_index.html')
		return func()
	return secure_function

@app.route('/')
def hello_world():
    return render_template('login_index.html')

@app.route("/login",methods=['post'])
def login():
    username=request.form['textfield']
    password=request.form['textfield2']
    qry="SELECT * FROM `login` WHERE `username`=%s AND `password`=%s"
    val=(username,password)
    res=selectone(qry,val)
    if res is None:
        return '''<script>alert("Invalid username or password");window.location="/"</script>'''
    elif res['type']=='admin':
        session['lid'] = res['l_id']
        return '''<script>alert("Welcome Admin");window.location="/admin_home"</script>'''
    elif res['type'] == 'hospital':
        session['lid'] = res['l_id']
        return '''<script>alert("Welcome Hospital");window.location="/hospital_home"</script>'''
    elif res['type'] == 'doctor':
        session['lid'] = res['l_id']
        return '''<script>alert("Welcome Doctor");window.location="/doctor_home"</script>'''
    elif res['type'] == 'user':
        session['lid'] = res['l_id']
        return '''<script>alert("Welcome User");window.location="/user_home"</script>'''
    else:
        return '''<script>alert("Invalid");window.location="/"</script>'''

@app.route('/logout')
@login_required
def logout():
	session.clear()
	return redirect('/')

#=================================================ADMIN========================================

@app.route('/admin_home')
@login_required
def admin_home():
    return render_template('admin/admin_index.html')

@app.route('/verify_hospital')
@login_required
def verify_hospital():
    q="select `hospital`.*,`login`.* from `hospital` join `login` on `hospital`.`lid`=`login`.`l_id`"
    res=selectall(q)
    return render_template('admin/verify_hospital.html', data=res)

@app.route('/accept_hos')
@login_required
def accept_hos():
    id=request.args.get('id')
    qry="UPDATE `login` SET `type`='hospital' WHERE `l_id`=%s"
    res=iud(qry,id)
    return '''<script>alert("Approved");window.location="/verify_hospital#about"  </script>'''

@app.route('/reject_hos')
@login_required
def reject_hos():
    id=request.args.get('id')
    qry="UPDATE `login` SET `type`='Rejected' WHERE `l_id`=%s"
    res=iud(qry,id)
    return '''<script>alert("Rejected");window.location="/verify_hospital#about"  </script>'''

@app.route('/view_users')
@login_required
def view_users():
    q="select * from `user`"
    res=selectall(q)
    return render_template('admin/view_users.html',data=res)

@app.route('/view_rating')
@login_required
def view_rating():
    q="select `rating`.*,`user`.*,`doctor`.`fname` as drfname,`doctor`.`lname` as drlname from `rating` join `user` on `rating`.`uid`=`user`.`l_id` join `doctor` on `doctor`.l_id= `rating`.`dr_id`"
    res=selectall(q)
    return render_template('admin/view_rating.html',data=res)

@app.route('/view_complaint')
@login_required
def view_complaint():
    qry = "SELECT `complaint`.*,`user`.* FROM `complaint` INNER JOIN `user` ON `complaint`.`uid`=`user`.`l_id` "
    res=selectall(qry)
    return render_template('admin/view_complaint.html',data=res)

@app.route('/sent_reply')
@login_required
def sent_reply():
    id=request.args.get('id')
    session['comid']=id
    return render_template("admin/sent_reply.html")

@app.route('/sent_reply_post',methods=['post'])
@login_required
def sent_reply_post():
    com = request.form['textfield']
    qry = "update `complaint` set `reply`=%s where `c_id`=%s"
    val = (com,str(session['comid']))
    iud(qry, val)
    return '''<script>alert("Reply sent successfully");window.location="/view_complaint#about"</script>'''

#=================================================HOSPITAL==============================================================

@app.route('/hospital_home')
@login_required
def hospital_home():
    return render_template('hop/hospital_index.html')

@app.route('/hos_register')
def hos_register():
    return render_template('hop/reg_index.html')

@app.route('/hos_register_post',methods=['post'])
def hos_register_post():
    name=request.form['textfield']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    phone = request.form['textfield7']
    email = request.form['textfield6']
    username = request.form['textfield8']
    password = request.form['textfield9']

    qry="INSERT INTO `login` (`username`,`password`,`type`) VALUES (%s,%s,'pending')"
    val=(username,password)
    res=iud(qry,val)

    qry1 = "insert into `hospital` values (null,%s,%s,%s,%s,%s,%s,%s)"
    val1=(str(res),name,place,post,pin,phone,email)
    iud(qry1,val1)

    return '''<script>alert("Registered Successfully");window.location='/'</script>'''

@app.route('/add_doctor',methods=['post'])
@login_required
def add_doctor():
    return render_template('hop/add_doctor.html')

@app.route('/add_doctor_post',methods=['post'])
@login_required
def add_doctor_post():
    fname = request.form['fname']
    lname = request.form['lname']
    gender = request.form['radiobutton']
    ql=request.form['textfield2']
    place=request.form['place']
    post=request.form['post']
    pin=request.form['pin']
    ph = request.form['phone']
    email = request.form['em']
    psw=random.randint(999,9999)

    qry="insert into `login` (`username`,`password`,`type`) values (%s,%s,'doctor')"
    val=(email,psw)
    id=iud(qry,val)

    q="INSERT INTO `doctor` (`l_id`,`hos_id`,`fname`,`lname`,`gender`,`place`,`post`,`pin`,`phone`,`email`,`qualification`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val1=(str(id),session['lid'],fname,lname,gender,place,post,pin,ph,email,ql)
    iud(q,val1)

    return '''<script>alert("Added successfully");window.location='/view_doctor#about'</script>'''

@app.route('/view_doctor')
@login_required
def view_doctor():
    qry="SELECT * FROM `doctor` where `hos_id`=%s"
    res=selectall2(qry,session['lid'])
    print(res)
    return render_template('hop/view_doctor.html',data=res)

@app.route('/edit_doctor')
@login_required
def edit_doctor():
    id=request.args.get('id')
    session['drlid']=id
    q="SELECT * FROM `doctor` WHERE `l_id`=%s"
    res=selectone(q,id)
    print(res)
    return render_template('hop/edit_doctor.html',data=res)

@app.route('/edit_doctor_post',methods=['post'])
@login_required
def edit_doctor_post():
    fname = request.form['fname']
    lname = request.form['lname']
    gender = request.form['radiobutton']
    ql=request.form['textfield2']
    place=request.form['place']
    post=request.form['post']
    pin=request.form['pin']
    ph = request.form['phone']
    email = request.form['em']

    q="UPDATE `doctor` SET `fname`=%s,`lname`=%s,`gender`=%s,`place`=%s,`post`=%s,`pin`=%s,`phone`=%s,`email`=%s,`qualification`=%s WHERE `l_id`=%s"
    val1=(fname,lname,gender,place,post,pin,ph,email,ql,str(session['drlid']))
    iud(q,val1)
    return '''<script>alert("Updated successfully");window.location='/view_doctor#about'</script>'''

@app.route('/delete_doctor')
@login_required
def delete_doctor():
    id=request.args.get('id')
    q="DELETE FROM `login` WHERE `l_id`=%s"
    iud(q,id)
    qry="DELETE FROM `doctor` WHERE `l_id`=%s"
    iud(qry,id)
    return '''<script>alert("Deleted successfully");window.location='/view_doctor#about'</script>'''

@app.route('/add_doctor_schedule')
@login_required
def add_doctor_schedule():
    return render_template('hop/add_doctor_schedule.html')

@app.route('/add_doctor_schedule_post', methods=['POST'])
@login_required
def add_doctor_schedule_post():
    day=request.form['select']
    frm=request.form['textfield2']
    to=request.form['textfield22']
    did=session['drid']
    qry="INSERT INTO `doc_shedule` VALUES (NULL,%s,%s,%s,%s)"
    val=(did,day,frm,to)
    iud(qry,val)
    return '''<script>alert("Added successfully");window.location='/view_doctor#about'</script>'''

@app.route('/view_doctor_schedule')
@login_required
def view_doctor_schedule():
    id=request.args.get('id')
    session['drid']=id
    q="SELECT * FROM `doc_shedule` WHERE `docid`=%s"
    res=selectall2(q,id)
    return render_template('hop/view_doctor_schedule.html',data=res)

@app.route('/delete_doctor_schedule')
@login_required
def delete_doctor_schedule():
    id=request.args.get('id')
    qry="DELETE FROM `doc_shedule` WHERE `id`=%s"
    iud(qry,id)
    return '''<script>alert("Deleted successfully");window.location='/view_doctor#about'</script>'''

@app.route('/hos_view_rating')
@login_required
def hos_view_rating():
    q="select `rating`.*,`user`.*,`doctor`.`fname` as drfname,`doctor`.`lname` as drlname from `rating` join `user` on `rating`.`uid`=`user`.`l_id` join `doctor` on `doctor`.l_id= `rating`.`dr_id` WHERE `doctor`.`hos_id`=%s"
    res=selectall2(q,session['lid'])
    return render_template('hop/view_rating.html',data=res)

#==========================================================DOCTOR=======================================================

@app.route('/doctor_home')
@login_required
def doctor_home():
    return render_template('doctor/doctor_index.html')

@app.route('/doc_view_rating')
@login_required
def doc_view_rating():
    q="select `rating`.*,`user`.*,`doctor`.`fname` as drfname,`doctor`.`lname` as drlname from `rating` join `user` on `rating`.`uid`=`user`.`l_id` join `doctor` on `doctor`.l_id= `rating`.`dr_id` WHERE `doctor`.`l_id`=%s"
    res=selectall2(q,session['lid'])
    return render_template('doctor/view_rating.html',data=res)

@app.route('/doctor_view_schedule')
@login_required
def doctor_view_schedule():
    q="SELECT * FROM `doc_shedule` WHERE `docid`=%s"
    res=selectall2(q,session['lid'])
    return render_template('doctor/view_doctor_schedule.html',data=res)

@app.route('/view_patients')
@login_required
def view_patients():
    q="SELECT `user`.*,`booking`.*,`doc_shedule`.* FROM `user` JOIN `booking` ON `booking`.`p_id`=`user`.`l_id` JOIN `doc_shedule` ON `booking`.`s_id`=`doc_shedule`.`id` WHERE `doc_shedule`.`docid`=%s"
    res=selectall2(q,session['lid'])
    return render_template('doctor/view_users.html',data=res)

@app.route('/dr_view_report')
@login_required
def dr_view_report():
    pid=request.args.get('id')
    session['pid']=pid
    q="SELECT `health_record`.*,`user`.* FROM `health_record` JOIN `user` ON `health_record`.`p_id`=`user`.`l_id` WHERE `health_record`.`d_id`=%s"
    res=selectall2(q,str(session['lid']))
    return render_template('doctor/dr_view_report.html',data=res)

@app.route('/add_report')
@login_required
def add_report():
    return render_template('doctor/add_report.html')

@app.route('/add_report_post', methods=['POST'])
@login_required
def add_report_post():
    pid=str(session['pid'])

    report = request.files['file']
    import time
    ext=report.filename.split(".")[-1]
    fn=time.strftime("%Y%m%d_%H%M%S")+"."+ext
    report.save("static/report/"+fn)

    q="INSERT INTO `health_record` VALUES (NULL,%s,%s,%s,CURDATE())"
    val=(pid,str(session['lid']),fn)
    iud(q,val)
    return "<script>alert('Added successfully');window.location='/dr_view_report?id="+str(session['pid'])+"#about'</script>"

#=========================================================USER==========================================================

@app.route('/user_home')
@login_required
def user_home():
    return render_template('user/user_index.html')

@app.route('/user_reg_index')
def user_reg_index():
    return render_template('user/user_reg_index.html')

@app.route('/user_register_post', methods=['POST'])
def user_register_post():
    fname = request.form['textfield']
    lname = request.form['textfield2']
    place = request.form['textfield3']
    post = request.form['textfield4']
    pin = request.form['textfield5']
    phone = request.form['textfield7']
    email = request.form['textfield6']
    username = request.form['textfield8']
    password = request.form['textfield9']
    gen=request.form['radiobutton']

    qry = "INSERT INTO `login` (`username`,`password`,`type`) VALUES (%s,%s,'user')"
    val = (username, password)
    res = iud(qry, val)

    qry1 = " INSERT INTO `user` VALUES (NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val1 = (str(res),fname,lname,gen,place,post,pin,phone,email)
    iud(qry1, val1)

    return '''<script>alert("Registered Successfully");window.location='/'</script>'''

@app.route('/view_hospital')
@login_required
def view_hospital():
    q="SELECT * FROM `hospital`"
    res=selectall(q)
    return render_template('user/view_hospital.html',data=res )

@app.route('/user_view_doctor')
@login_required
def user_view_doctor():
    id=request.args.get('id')
    session['hid']=id
    q="SELECT `doctor`.*,AVG(`rating`.`rating`) AS avgrating FROM `doctor` LEFT JOIN `rating` ON `doctor`.`l_id`=`rating`.`dr_id`  WHERE `doctor`.`hos_id`=%s  GROUP BY (`rating`.`dr_id`)"
    res=selectall2(q,id)
    return render_template('user/user_view_doctor.html',data=res)

@app.route('/user_view_doctor_schedule')
@login_required
def user_view_doctor_schedule():
    id=request.args.get('id')
    session['drid']=id
    q="SELECT * FROM `doc_shedule` WHERE `docid`=%s"
    res=selectall2(q,id)
    return render_template('user/user_view_doctor_schedule.html',data=res)

@app.route('/book_doctor')
@login_required
def book_doctor():
    id=request.args.get('id')
    session['shid']=id
    return render_template('user/book_doctor.html')

@app.route('/book_doctor_post',methods=['post'])
@login_required
def book_doctor_post():
    print(request.form)
    date=request.form['filefield']

    qrt="SELECT * FROM `booking` WHERE `s_id`=%s AND `date`=%s AND `p_id`=%s"
    val=(str(session['shid']),date,str(session['lid']))
    res=selectone(qrt,val)
    if res is None:
        q = "INSERT INTO `booking` VALUES (NULL,%s,%s,%s)"
        v = (str(session['shid']), str(session['lid']), date)
        iud(q, v)
        return "<script>alert('Booked successfully');window.location='/user_view_doctor_schedule?id="+str(session['drid'])+"#about'</script>"
    else:
        return "<script>alert('Alerady booked choose another date or schedule');window.location='/user_view_doctor_schedule?id="+str(session['drid'])+"#about'</script>"

@app.route('/user_view_report')
@login_required
def user_view_report():
    q="SELECT `health_record`.*,`doctor`.* FROM `health_record` JOIN `doctor` ON `health_record`.`d_id`=`doctor`.`l_id` WHERE `health_record`.`p_id`=%s"
    res=selectall2(q,str(session['lid']))
    return render_template('user/user_view_report.html',data=res)

@app.route('/view_reply')
@login_required
def view_reply():
    qry="SELECT * FROM `complaint` WHERE `uid`=%s"
    res=selectall2(qry,session['lid'])
    return render_template('user/view_reply.html',data=res)

@app.route('/send_complaint',methods=['post'])
@login_required
def send_complaint():
    return render_template('user/send_complaint.html')

@app.route('/send_complaint_post',methods=['post'])
@login_required
def send_complaint_post():
    complaint=request.form['filefield']
    qry="INSERT INTO `complaint` (`uid`,`complaint`,`date`,`reply`) VALUES (%s,%s,CURDATE(),'pending')"
    val=(session['lid'],complaint)
    res=iud(qry,val)
    return '''<script>alert("Send successfully");window.location='/view_reply#about'</script>'''

@app.route('/send_rating')
@login_required
def send_rating():
    did=request.args.get('id')
    session['did']=did
    return render_template('user/send_rating.html')

@app.route('/send_rating_post', methods=['POST'])
@login_required
def send_rating_post():
    rate=request.form['select']
    qry="INSERT INTO `rating` VALUES (NULL,%s,%s,%s,CURDATE())"
    val=(str(session['lid']),str(session['did']),rate)
    iud(qry,val)
    return "<script>alert('Send successfully');window.location='/user_view_doctor?id=" + str(session['hid']) + "#about'</script>"

@app.route('/predictt')
@login_required
def predictt():
    return render_template('user/predict.html')

@app.route('/predict_post', methods=['POST'])
@login_required
def predict_post():
    image = request.files['file']
    image.save(r"C:\Users\User\Desktop\eye_diseases\src\static\image\1.jpg")
    result=predict('static/image/1.jpg')
    return render_template('user/result.html',res=result)

app.run(debug=True)