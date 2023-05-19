
class TransactionDAO():
	def __init__(self, DAO):
		self.db = DAO
		
	def getUser(self,studentUsername):
		result,h = self.db.db.query("SELECT * FROM transactions WHERE studentUsername = '{}'".format(studentUsername))
		
		return result,h
	
	def getFine(self,studentUsername):
		result,h = self.db.db.query("SELECT fine FROM transactions WHERE studentUsername = '{}'".format(studentUsername))
		
		return result,h