from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import json
import collections
import sqlite3 as sql
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/enternew')
def new_user():
   return render_template('user.html')

@app.route('/add',methods = ['POST'])
@cross_origin()
def add():
   if request.method == 'POST':
      try:
        content = request.json
        name = content['name']
        grade = content['grade']

        print(name)
        print(grade)

        with sql.connect("database.db") as con:
          cur = con.cursor()

          cur.execute("INSERT INTO users (name,grade) VALUES (?,?)",(name,grade) )

          con.commit()
          msg = "Record successfully added"
          print(msg)

      except:
         con.rollback()
         msg = "error in insert operation"
         print(msg)

      finally:
        con.close()
        # return render_template("result.html",msg = msg)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

@app.route('/list')
@cross_origin()
def list():
  try:
      con = sql.connect("database.db")
      con.row_factory = sql.Row

      cur = con.cursor()
      cur.execute("select * from users")

      result_list = cur.fetchall();
      print(result_list)
      # return render_template("list.html",rows = rows)

      objects_list = []
      for row in result_list:
        d = collections.OrderedDict()
        d['id'] = row[0]
        d['name'] = row[1]
        d['grade'] = row[2]
        objects_list.append(d)

  except:
    con.close()
  finally:
    con.close()
    return json.dumps(objects_list), 200, {'ContentType':'application/json'}

@app.route('/delete/<id>')
def delete(id=None):
   return str(id)

if __name__ == '__main__':
    app.run(debug=True)
