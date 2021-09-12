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

@app.route('/update',methods = ['PUT'])
@cross_origin()
def update():
    try:
        content = request.json
        id = int(content['id'])
        name = content['name']
        en = content['en']
        ts = content['ts']
        math = content['math']

        d = collections.OrderedDict()

        with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("UPDATE students SET name=?,en=?,ts=?,math=? WHERE ID=?", (name,en,ts,math,id))

            con.commit()
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    except:
        con.rollback()
        # msg = "error in insert operation"
        # print(msg)
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

    finally:
        con.close()
        # return render_template("result.html",msg = msg)


@app.route('/add',methods = ['POST'])
@cross_origin()
def add():
    try:
        content = request.json
        name = content['name']
        en = content['en']
        ts = content['ts']
        math = content['math']

        with sql.connect("database.db") as con:
            cur = con.cursor()

            cur.execute("INSERT INTO students (name,en,ts,math) VALUES (?,?,?,?)",(name,en,ts,math) )

            con.commit()
            # msg = "Record successfully added"
            # print(msg)
            return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    except:
        con.rollback()
        # msg = "error in insert operation"
        # print(msg)
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

    finally:
        con.close()
        # return render_template("result.html",msg = msg)

@app.route('/list')
@cross_origin()
def list():
    try:
        con = sql.connect("database.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from students")

        result_list = cur.fetchall();
        # return render_template("list.html",rows = rows)

        objects_list = []
        for row in result_list:
            d = collections.OrderedDict()
            d['id'] = row[0]
            d['name'] = row[1]
            d['en'] = row[2]
            d['ts'] = row[3]
            d['math'] = row[4]
            objects_list.append(d)

        objects_list.sort(key=lambda  item: item['en'] + item['ts'] + item['math'], reverse=True)
        for i in range(len(objects_list)):
            print(i)

        return json.dumps(objects_list), 200, {'ContentType':'application/json'}

    except:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

    finally:
        con.close()

@app.route('/student/<id>')
def getStudent(id=None):
    try:
        con = sql.connect("database.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from students")

        result_list = cur.fetchall();
        # return render_template("list.html",rows = rows)
        d = collections.OrderedDict()
        for row in result_list:
            if str(row[0]) == id:
                d['id'] = row[0]
                d['name'] = row[1]
                d['en'] = row[2]
                d['ts'] = row[3]
                d['math'] = row[4]
        return json.dumps(d), 200, {'ContentType':'application/json'}

    except:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

    finally:
        con.close()

@app.route('/delete/<id>', methods = ['DELETE'])
def delete(id=None):
    try:
        con = sql.connect("database.db")
        con.row_factory = sql.Row
        cur = con.cursor()

        delstatmt = "DELETE FROM `students` WHERE id = ?"
        cur.execute(delstatmt, (id,))
        con.commit()

        return json.dumps({'success':True}), 200, {'ContentType':'application/json'}

    except:
        return json.dumps({'success':False}), 500, {'ContentType':'application/json'}

    finally:
        con.close()

if __name__ == '__main__':
    app.run(debug=True)
