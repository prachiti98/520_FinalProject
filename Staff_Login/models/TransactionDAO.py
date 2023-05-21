class TransactionDAO():
	def __init__(self, DAO):
		self.db = DAO
		
	def getUser(self,studentUsername):
		result,h = self.db.query("SELECT * FROM transactions WHERE studentUsername = '{}'".format(studentUsername))
		return result,h
	
	def getFine(self,studentUsername):
		result,h = self.db.query("SELECT fine FROM transactions WHERE studentUsername = '{}'".format(studentUsername))
		return result,h
	
	def getBook(self,student_id,book_name):
		result,h = self.db.query_data("SELECT book_id FROM transactions WHERE studentUsername= '"+str(student_id)+"' AND bookName= '"+str(book_name)+"' ")
		return result,h
	
	def update_transaction(self,student_id,book_id):
		self.db.query("UPDATE transactions SET Done = 1  WHERE book_id = " +str(book_id)+" AND studentUsername= "+str(student_id)+" ")
		self.db.commit()
	
	def get_return_date(self,student_id,book_id):
		result,h = self.db.query_data("SELECT returnDate FROM transactions WHERE studentUsername = '" +str(student_id)+"' AND book_id= "+str(book_id)+" ")         
		return result,h
	
	def update_fine(self,student_id,amount_to_be_added_to_fine):
		self.db.query("UPDATE transactions SET fine=fine+ "+str(amount_to_be_added_to_fine)+" studentUsername= '"+str(student_id)+"'  ")   
		self.db.commit()      
		