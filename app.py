from flask import Flask,render_template,request,redirect,url_for,session,flash
from flask import send_file
from flask_session import Session
from flask_mysqldb import MySQL
from io import BytesIO
#create a flask object
'''app = Flask(__name__)
#we will give routing
@app.route('/')
def hello():
    return "Hey all how are you?"
#run the applictn
@app.route('/home')
def new():
    return render_template('index.html')

app.run()'''
app = Flask(__name__)
#start confgrng database
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "geethaabhima"
app.config['MYSQL_DB'] = 'spm' #create database spm
app.config['SESSION_TYPE']='filesystem'
#we will give a secret key
app.secret_key = "@hkdjhc" #alphanumeric
Session(app)
mysql = MySQL(app)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register',methods=['GET','POST'])
def register():
    #print(request.form)
    if request.method == "POST":
        #print(request.form['id'])
        rollno = request.form['id']
        name = request.form['name']
        group = request.form['group']
        password = request.form['password']
        code = request.form['code']
        ccode = "amrn"
        if code == ccode:
            cursor = mysql.connection.cursor()
            cursor.execute('insert into students values(%s,%s,%s,%s)',
                           (rollno,name,group,password))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('login'))
            #return "Details registered"
        else:
            return "Invalid college code"
    return render_template('register.html')
@app.route('/login',methods=['GET','POST'])
def login():
    '''if session.get('user'):
        return redirect(url_for('home'))'''
    if request.method=="POST":
        rollno = request.form['id']
        password = request.form['password']
        cursor = mysql.connection.cursor()
        cursor.execute('select rollno from students')
        users=cursor.fetchall()
        #print(users)
        if (int(rollno),) in users:
            cursor.execute('select password from students where rollno=%s',[rollno])
            a_password = cursor.fetchone()[0]
            if password == a_password:
                session['user'] = rollno
                return redirect(url_for('home'))
            else:
                return "Invalid password"
        else:
            return "invalid rollno"
    return render_template('login.html')
@app.route('/Studenthome')
def home():
    if session.get('user'):
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('login'))
    else:
        return 'Session popped already'
@app.route('/noteshome')
def notes():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from notes where rollno = %s',[session.get('user')])
        data=cursor.fetchall()
        #we give data as source for template
        return render_template('addnotetable.html',data=data)
    else:
        return redirect(url_for('login'))
@app.route('/addnotes',methods=['GET','POST'])
def addnotes():
    if session.get('user'):
        if request.method == 'POST':
            title=request.form['title']
            content = request.form['content']
            cursor = mysql.connection.cursor()
            cursor.execute('insert into notes(rollno,title,content) values(%s,%s,%s)',[session.get('user'),title,content])
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for('notes'))
        return render_template('notes.html')
    else:
        return redirect(url_for('login'))
@app.route('/readnotes/<int:nid>')
def readnote(nid):
    if session.get('user'):
        cursor = mysql.connection.cursor()
        cursor.execute('select title,content from notes where nid=%s',[nid])
        notes=cursor.fetchone()
        cursor.close()
        return render_template('readnotes.html',
                               notes=notes)
    else:
        return redirect(url_for('login'))
@app.route('/deletenotes/<int:nid>')
def deletenote(nid):
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('delete from notes where nid=%s',[nid])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('notes'))
    else:
        return redirect(url_for('login'))
@app.route('/updatenotes/<int:nid>',
           methods=['GET','POST'])
def updatenote(nid):
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select title,content from notes where nid=%s',[nid])
        notes=cursor.fetchone()
        cursor.close()
        if request.method=='POST':
            title = request.form['title']
            content = request.form['content']
            cursor = mysql.connection.cursor()
            cursor.execute('update notes set title=%s,content=%s where nid=%s',[title,content,nid])
            mysql.connection.commit()
            return redirect(url_for('notes'))
        return render_template('updatenotes.html',notes=notes)
    else:
        return redirect(url_for('login'))
@app.route('/filehome',methods=['GET','POST'])
def filehome():
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select * from files where rollno=%s',[session.get('user')])
        filesdata=cursor.fetchall()
        cursor.close()
        if request.method=='POST':
            file=request.files['file']
            filename=file.filename
            fileupload=file.read()
            cursor=mysql.connection.cursor()
            cursor.execute('insert into files(rollno,filename,fileupload)\
values(%s,%s,%s)',[session.get('user'),filename,fileupload])
            mysql.connection.commit()
            #we add these lines to make visible
            cursor.execute('select * from files \
where rollno =%s',[session.get('user')])
            filesdata = cursor.fetchall()
            cursor.close()
        return render_template('fileuploadtable.html',
                               filesdata=filesdata)
    else:
        return redirect(url_for('login'))
@app.route('/readfile/<int:fid>')
def readfile(fid):
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('select filename,fileupload from files \
where fid=%s',[fid])
        filesdata=cursor.fetchone()
        cvt_bytes= BytesIO(filesdata[1])
        return send_file(cvt_bytes,
                         download_name=filesdata[0])
    else:
        return redirect(url_for('login'))
@app.route('/deletefile/<int:fid>')
def deletefile(fid):
    if session.get('user'):
        cursor=mysql.connection.cursor()
        cursor.execute('delete from files where fid=%s',[fid])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('filehome'))
    else:
        return redirect(url_for('login'))
app.run()






