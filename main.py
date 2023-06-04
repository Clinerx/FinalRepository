from flask import Flask, make_response, jsonify, Response, request
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

USER_DATA = {"Login": "Login"}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] = 'apzx0dfd6'
app.config['MYSQL_DB'] = 'badmiton_reservation'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def hello_world():
    return "<p>This is my list!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data

@app.route("/players", methods=["GET"])
@auth.login_required
def get_players():
    data = data_fetch("""SELECT * FROM players""")
    return make_response(jsonify(data), 200)


@app.route("/players/<int:id>", methods=["GET"])
@auth.login_required
def get_players_by_id(id):
    data = data_fetch("""SELECT * FROM players WHERE players_id = {}""".format(id))
    myResponse = make_response(jsonify(data))
    return myResponse
    

@app.route("/players", methods=['POST'])
@auth.login_required
def add_player():
    cur = mysql.connection.cursor()
    json = request.get_json(force=True)
    players_name = json["players_name"]
    players_email = json["players_email"]
    players_contact = json["players_contact"]
    cur.execute(
        """ INSERT INTO players (players_name, players_email, players_contact) VALUE (%s, %s, %s)""", (players_name, players_email, players_contact),
    )
    mysql.connection.commit()
    _response = jsonify("player added successfully!")
    _response.status_code = 200
    cur.close()
    return _response

@app.route("/players/<int:id>", methods=["PUT"])
@auth.login_required
def update_song_by_id(id):
    cur = mysql.connection.cursor()
    json = request.get_json(force=True)
    players_name = json["players_name"]
    players_email = json["players_email"]
    players_contact = json["players_contact"]
    cur.execute(""" UPDATE players SET players_name = %s, players_email = %s, players_contact = %s WHERE players_id = %s""", (players_name, players_email, players_contact, id))
    mysql.connection.commit()
    _response = jsonify("Player updated successfully!")
    _response.status_code = 200
    cur.close()
    return _response
        
        
        

@app.route("/players/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_song(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM players WHERE players_id = %s""", (id,))
    mysql.connection.commit()
    cur.close()
    return make_response(jsonify({"message": "player deleted successfully"}), 200)
    


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == "__main__":
    app.run(debug=True)