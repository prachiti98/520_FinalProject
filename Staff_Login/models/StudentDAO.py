
class StudentDAO():
	def __init__(self, DAO):
		self.db = DAO
		
		
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
        