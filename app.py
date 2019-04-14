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


@app.route("/done/<task>/")
def mark_as_done(task):
	task_to_update = task.replace("-", " ")

	with sqlite3.connect("database.db") as con:
		cur = con.cursor()
		cur.execute("UPDATE todo SET status = 1 WHERE task = ?",(task_to_update,) )

	con.commit()

	return render_template("result_archived.html", msg=task_to_update)
	con.close()


@app.route('/archive')
def archive():
	con = sqlite3.connect("database.db")
	con.row_factory = sqlite3.Row
	cur = con.cursor()
	cur.execute("select * from todo")
	rows = cur.fetchall();
	return render_template('archive.html', rows=rows)

@app.route("/clearhistory")
def clear_history():
	with sqlite3.connect("database.db") as con:
		cur = con.cursor()
		cur.execute("DELETE FROM todo WHERE status = 1")

	con.commit()

	return render_template("archive.html")
	con.close()

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