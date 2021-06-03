from flask import Flask, render_template,request, session , redirect , url_for , g,flash, jsonify, make_response, json,flash
from flask_mail import Mail,Message
from flask_cors import CORS
from pusher import pusher
from flask_wtf import FlaskForm
from wtforms import (StringField ,PasswordField,SubmitField)
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError,DataRequired,InputRequired
import model
from flask_apscheduler import APScheduler
app = Flask(__name__)
mail = Mail(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
scheduler = APScheduler()
app.secret_key = 'mohsin5432'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_DEFAULT_SENDER'] = 'it.timepay@gmail.com'
app.config['MAIL_USERNAME'] = 'it.timepay@gmail.com'
app.config['MAIL_PASSWORD'] = 'Moh$in531'
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

pusher = pusher_client = pusher.Pusher(
    app_id = "1118828",
    key = "4f4c1cd696946236d54c",
    secret = "dee623f36d26edb30254",
    cluster = "ap1",
    ssl=True
)

username = ''
user = model.check_users()
admin = ''

class loginform(FlaskForm):
    username = StringField(validators=[DataRequired(message="enter username")],render_kw={"placeholder": "username"})
    password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "Password"})
    submit = SubmitField('submit')

class signupform(FlaskForm):
    username = StringField(validators=[DataRequired(message="enter username")],render_kw={"placeholder": "username"})
    email = EmailField(validators=[InputRequired()],render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[DataRequired()],render_kw={"placeholder": "Password"})
    submit = SubmitField('submit')

class newsletter(FlaskForm):
    email = EmailField(validators=[InputRequired()],render_kw={"placeholder": "Email"})
    submit = SubmitField('Submit')



@app.route('/',methods = ['GET'])
def home():
    if 'username' in session:
        g.user = session['username']
        pending=model.pendingtask(g.user)
        progress=model.progresstask(g.user)
        completed=model.completedtask(g.user)
        if not progress:
            pmsg = 'NO PROGRESS TASK'
        else:
            pmsg=""
        if not pending:
            dmsg = 'NO PENDING TASK'
        else:
            dmsg=""
        if not completed:
            cmsg = 'NO COMPLETED TASK'
        else:
            cmsg=""
        return render_template('homepage.html',pending=pending,progress=progress,completed=completed,pmsg=pmsg,dmsg=dmsg,cmsg=cmsg)
    return redirect(url_for('login'))


@app.route('/login',methods = ['GET' ,'POST'])
def login():
    username = False
    password = False
    form = loginform()
    nform = newsletter()
    sform = signupform()
    if request.method == 'GET':
        return render_template('login.html',form=form,nform=nform,sform=sform)

    else:
        session.pop('username', None)
        areyouuser = form.username.data
        pwd = model.pass_check(areyouuser)
        if form.password.data == pwd:
            session['username'] = form.username.data
            return redirect(url_for('home'))
    return render_template('login.html',form=form,nform=nform,sform=sform)


@app.before_request
def before_request():
    g.username = None
    if 'username' in session:
        g.username = session['username']


@app.route('/logout', methods = ['POST'])
def logout():
    session.pop('username' , None)
    return redirect(url_for('home'))


@app.route('/getsession')
def getsession():
    if 'username' in session:
        return session['username']
    return redirect(url_for('login'))


@app.route('/new/guest', methods=['POST'])
def guestUser():
	data = request.json

	pusher.trigger(u'general-channel', u'new-guest-details', {
		'name' : data['name'],
		'email' : data['email']
		})

	return json.dumps(data)


@app.route("/pusher/auth", methods=['POST'])
def pusher_authentication():
	auth = pusher.authenticate(channel=request.form['channel_name'],socket_id=request.form['socket_id'])
	return json.dumps(auth)


@app.route('/admin/livechat')
def adminchat():
	return render_template('adminchat.html')


@app.route('/signup',methods = ['POST'])

def signup():
    form = loginform()
    nform = newsletter()
    sform = signupform()
    email = sform.email.data
    username = sform.username.data
    password = sform.password.data
    agp = model.signup(email,username,password)
    if agp is True:
        msg = Message('TimePay', recipients=[sform.email.data])
        msg.body = "THANKS FOR SIGNING UP"
        mail.send(msg)
        message = "Signed up successfully"
    else:
        message = "USER Already Exist"
    return render_template('login.html',message = message,nform=nform,sform=sform,form=form)

@app.route('/addtask',methods = ['GET','POST'])
def addtask():
    if 'username' in session:
        if request.method == 'GET':
            return render_template('addtask.html')
        else:
            g.user = session['username']
            username = g.user
            email = model.email(g.user)
            subject = request.form["subject"]
            memo = request.form["memo"]
            status = "pending"
            date = request.form["date"]
            message = model.addtask(username,email,subject,memo,status,date)
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/start/<string:id_data>', methods = ['GET'])
def tdelete(id_data):
    model.start(id_data)
    return redirect(url_for('home'))

@app.route('/completed/<string:id_data>', methods = ['GET'])
def completed(id_data):
    model.completed(id_data)
    return redirect(url_for('home'))

@app.route('/delete/<string:id_data>', methods = ['GET'])
def delete(id_data):
    model.delete(id_data)
    return redirect(url_for('home'))




#for Newsletter



@app.route('/news',methods = ['POST'])

def news():
    form = loginform()
    nform = newsletter()
    email = nform.email.data
    con = model.news(email)
    if con is True:
        msg = Message('Welcome To TimePay', recipients=[nform.email.data])
        msg.body = "THANKS FOR SUBSCRIBING OUR NEWSLETTER WE WILL BE LAUNCHING SOON GREAT SERVICES"
        mail.send(msg)
        flash("THANKS FOR SUBSCRIBING")
    else:
        flash("YOU ARE Already SUBSCRIBED")
    return redirect(url_for('login'))



#admin section

@app.route('/admin',methods = ['GET','POST'])
def admin():
    if 'admin' in session:
        return redirect(url_for('adminpanel'))
    else:
        if request.method == 'GET':
            return render_template('adminlog.html')
        else:
            admin = request.form['user']
            password = request.form['password']
            db_pass = model.admpass_check(admin)
            if password == db_pass:
                session["admin"] = admin
                return redirect(url_for('adminpanel'))
            else:
                return redirect(url_for('admin'))


@app.route('/adminpanel',methods = ['GET','POST'])
def adminpanel():
    if 'admin' in session:
        mail = model.emails()
        return render_template('admin.html',mail=mail)
    return redirect(url_for('admin'))



@app.route('/logoutadm')
def logoutadm():
    session.pop('admin' , None)
    return redirect(url_for('admin'))


#remainder for task

def remainder():
    emails = model.remainder()
    if not emails:
        print("NO Email Found")
    else:
        with app.app_context():
            for mails in emails:
                msg = Message('TASK SUBMISSION DATE IS SO CLOSE', recipients=['{}'.format(mails[0])])
                msg.body = "HI there \n your task submission date is so close start your project"
                mail.send(msg)
                print("remainder email sended to :")
                print(mails[0])
        return True



if __name__ == '__main__':
    scheduler.add_job(id ='Scheduled task', func = remainder , trigger="interval" , hours = 20 )
    scheduler.start()
    app.run(port=8000 ,debug = True,use_reloader=False)
