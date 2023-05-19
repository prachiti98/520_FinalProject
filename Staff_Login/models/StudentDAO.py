
class StudentDAO():
	def __init__(self, DAO):
		self.db = DAO
		

	# def list(self):
	# 	users = self.db.query("select @table.id,@table.name,@table.email,@table.bio,@table.mob,@table.lock,@table.created_at,count(reserve.book_id) as books_owned from @table LEFT JOIN reserve ON reserve.user_id=@table.id GROUP BY reserve.user_id").fetchall()

	# 	return users

	# def getById(self, id):
	# 	q = self.db.query("select * from @table where id='{}'".format(id))

	# 	user = q.fetchone()

	# 	return user

	# def getUsersByBook(self, book_id):
	# 	q = self.db.query("select * from @table LEFT JOIN reserve ON reserve.user_id = @table.id WHERE reserve.book_id={}".format(book_id))

	# 	user = q.fetchall()

	# 	return user

	# def getByEmail(self, email):
	# 	q = self.db.query("select * from @table where email='{}'".format(email))

	# 	user = q.fetchone()

	# 	return user

	# def add(self, user):
	# 	name = user['name']
	# 	email = user['email']
	# 	password = user['password']

	# 	q = self.db.query("INSERT INTO @table (name, email, password) VALUES('{}', '{}', '{}');".format(name, email, password))
	# 	self.db.commit()
		
	# 	return q


	# def update(self, user, _id):
	# 	name = user['name']
	# 	email = user['email']
	# 	password = user['password']
	# 	bio = user['bio']

	# 	q = self.db.query("UPDATE @table SET name = '{}', email='{}', password='{}', bio='{}' WHERE id={}".format(name, email, password, bio, _id))
	# 	self.db.commit()
		
	# 	return q
	def addStudent(self,studentName,email,mobile,studentUsername,password):
		q = self.db.db.query("INSERT INTO students(studentName, email, mobile, studentUsername, password) VALUES('{}', '{}', '{}', '{}', '{}');".format(studentName, email, mobile, studentUsername, password))
		self.db.db.commit()
		return q
	
	def getUser(self,studentUsername):
		result,h = self.db.db.query("SELECT * FROM students WHERE studentUsername = '{}'".format(studentUsername))
		
		return result,h
	
	def getBooks(self):
		result,h = self.db.db.query("SELECT bookName, sum(available) AS count FROM books GROUP BY bookName")
		
		return result,h
        