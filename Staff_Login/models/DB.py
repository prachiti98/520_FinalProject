from flask_mysqldb import MySQL


class DB(object):
	"""Initialize mysql database """
	host = "localhost"
	user = "root"
	password = "msb1998"
	database = "library"
	table = ""

	def __init__(self, app):
		app.config["MYSQL_DATABASE_HOST"] = self.host
		app.config["MYSQL_DATABASE_USER"] = self.user
		app.config["MYSQL_DATABASE_PASSWORD"] = self.password
		app.config["MYSQL_DATABASE_DB"] = self.database
		app.config["MYSQL_CURSORCLASS"] = 'DictCursor'

		self.mysql = MySQL(app)

	def cur(self):
		return self.mysql.connection.cursor()

	def query(self, q):
		h = self.cur()
	
		# if (len(self.table)>0):
		# 	q = q.replace("@table", self.table)

		result = h.execute(q)

		return result,h
	
	def commit(self):
		self.query("COMMIT;")