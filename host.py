from flask import Flask, render_template,request,jsonify
from flaskext.mysql import MySQL

app=Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'userlog'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)



@app.route("/")
def index():
	return render_template("name.html")


@app.route("/home",methods=['POST'])
def home():
	db=mysql.connect()
	cursor=db.cursor()
	cursor.execute("select * from `mouseapp` where name ='"+request.form['name']+"'")
	result=cursor.fetchone()
	if result is None:
		cursor.execute("insert into `mouseapp` (`name`,`status`) values ('"+request.form['name']+"' , 1) ")	
	else:
		cursor.execute("UPDATE `mouseapp` SET `status`=1,`other`='',lmark=0,rmark=0  WHERE `name`='"+request.form['name']+"'")
	db.commit()
	return render_template("index.html",user=request.form['name'])

@app.route("/online",methods=['POST','GET'])
def online():
	db=mysql.connect()
	cursor=db.cursor()
	cursor.execute("select `name` from `mouseapp` where status = 1 OR status= 2")
	result=cursor.fetchall()
	names=[]
	for i in result:
		names.append(i[0])
	db.close()
	return jsonify({"name":names})


# send challenge request
@app.route("/challenge/<name>by<user>",methods=['POST','GET'])
def challenge(name,user):
	db=mysql.connect()
	cursor=db.cursor()
	cursor.execute("UPDATE `mouseapp` SET `status`=2,`other`='"+user+"' WHERE `name`='"+name+"'")
	cursor.execute("UPDATE `mouseapp` SET `status`=2,`other`='"+name+"' WHERE `name`='"+user+"'")
	db.commit()
	db.close()
	return "connected"



@app.route("/alive/<user>",methods=['POST','GET'])
def alive(user):
	db=mysql.connect()
	cursor=db.cursor()
	cursor.execute("select `other` from `mouseapp` where `name`='"+user+"' AND status= 2")
	result=cursor.fetchone()
	
	if result is None:
		cursor.execute("select `name` from `mouseapp` where `other`='"+user+"' AND status= 2")
		result=cursor.fetchone()
		db.commit()
		db.close()
		if result is None:
			return "0"
		else:
			return result[0]
			
	else:
		db.commit()
		db.close()
		return result[0]

@app.route("/remarks/<myself>m<clicks>",methods=['POST','GET'])
def setclicks(myself,clicks):
	db=mysql.connect()
	cursor=db.cursor()
	cursor.execute("update `mouseapp` set lmark = '"+clicks+"' where name='"+myself+"'")
	db.commit()
	db.close()
	return "hello"

@app.route("/check/<myself>",methods=['POST','GET'])
def check(myself):
	db=mysql.connect()
	cursor=db.cursor()
	cursor.execute("select `lmark` from `mouseapp` where other ='"+myself+"'")
	result=cursor.fetchone()
	db.close()
	return str(result[0])


if __name__ == "__main__":
	app.run(host='0.0.0.0',port=80,debug=True)
