rom typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'employeeDatabase'
mysql.init_app(app)




@app.route('/api/v1/employeeInformation', methods=['GET'])
def api_browse()-> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeBioStats')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/employeeInformation/<int:id>', methods=['GET'])
def api_retrieve(id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM employeeBioStats WHERE id=%s', id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/api/v1/employeeInformation', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Name'], content['Sex'], content['Age'],
                 content['Height_in'], content['Weight_lbs'])
    sql_insert_query = """INSERT INTO employeeBioStats (Name, Sex, Age, Height_inches, Weight_lbs) VALUES (%s, %s,%s, %s,%s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/employeeInformation/<int:id>', methods=['PUT'])
def api_edit(id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Name'], content['Sex'], content['Age'],
                 content['Height_inches'], content['Weight_lbs'],id)
    sql_update_query = """UPDATE employeeBioStats e SET e.Name = %s, e.Sex = %s,e.Age = %s, e.Height_inches = %s, e.Weight_lbs = 
    %s WHERE e.id = %s"""
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp

@app.route('/api/v1/employees/<int:id>', methods=['DELETE'])
def api_delete(id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM employeeBioStats WHERE id = %s """
    cursor.execute(sql_delete_query, id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)