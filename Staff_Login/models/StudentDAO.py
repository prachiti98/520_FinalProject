class StudentDAO():
	def __init__(self, DAO):
		self.db = DAO
		
	def addStudent(self,studentName,email,mobile,studentUsername,password):
		q = self.db.query("INSERT INTO students(studentName, email, mobile, studentUsername, password) VALUES('{}', '{}', '{}', '{}', '{}');".format(studentName, email, mobile, studentUsername, password))
		self.db.commit()
		return q
	
	def getUser(self,studentUsername):
		result,h = self.db.query("SELECT * FROM students WHERE studentUsername = '{}'".format(studentUsername))
		return result,h
	
        