from app import app
from flaskext.mysql import MySQL

MySQL = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'apzx0dfd6'
app.config['MYSQL_DATABASE_DB'] = 'badminton_reservation'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)