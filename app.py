from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__)
#DATABASE = 'database.db'

'''conn = sqlite3.connect('database.db')
print("Opened database successfully")

conn.execute('CREATE TABLE todo (task TEXT, status INTEGER DEFAULT 0)')
print("Table created successfully")
conn.close()'''

@app.route('/newtask')
def new_task():
   return render_template('newtask.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
	if request.method == 'POST':
		task = request.form['task']

		with sqlite3.connect("database.db") as con:
			cur = con.cursor()
			cur.execute("INSERT INTO todo (task) VALUES (?)",(task,) )

		con.commit()
		msg = "Record successfully added"
		
		'''except:
			con.rollback()
			msg = "error in insert operation"'''

		return render_template("result.html",msg = msg)
		con.close()

@app.route('/archive')
def archive():
   return render_template('archive.html')

@app.route("/")
def index():
	con = sqlite3.connect("database.db")
	con.row_factory = sqlite3.Row

	cur = con.cursor()
	cur.execute("select * from todo")

	rows = cur.fetchall(); 
	return render_template("index.html",rows = rows)

if __name__ == "__main__":
	app.run(debug=True)