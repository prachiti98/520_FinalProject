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
		result,h = self.db.query_data("SELECT transaction_id,book_id FROM transactions WHERE studentUsername= '"+str(student_id)+"' AND bookName= '"+str(book_name)+"' AND Done IS NULL")
		return result,h
	
	def update_transaction(self,student_id,book_id):
		self.db.query("UPDATE transactions SET Done = 1  WHERE book_id = " +str(book_id)+" AND studentUsername= '"+str(student_id)+"' ")
		self.db.commit()
	
	def get_return_date(self,student_id,book_id):
		result,h = self.db.query_data("SELECT returnDate FROM transactions WHERE studentUsername = '" +str(student_id)+"' AND book_id= "+str(book_id)+" AND Done IS NULL")         
		return result,h
	
	def update_fine(self,transaction_id,amount_to_be_added_to_fine):
		self.db.query("UPDATE transactions SET fine="+str(amount_to_be_added_to_fine)+" WHERE transaction_id= "+str(transaction_id)+" ")   
		self.db.commit()      
	
	def issue_book(self,student_id,staffUsername,bookName,book_id):
		query = "INSERT INTO transactions (studentUsername, staffUsername, bookName, book_id) VALUES ('{}', '{}', '{}', {})"
		formatted_query = query.format(student_id, staffUsername, bookName,book_id)
		self.db.query(formatted_query)   
		self.db.commit()     

	def get_all_fines(self):
		result,h = self.db.query_data("SELECT studentUsername, fine  FROM transactions where fine > 0 GROUP BY studentusername,fine")         
		return result,h

	def get_fine(self,student_id):
		result,h = self.db.query_data("SELECT studentUsername,SUM(fine) AS fine FROM transactions where studentUsername='"+str(student_id)+"' GROUP BY studentUsername")         
		return result,h

	def get_fine_transactions(self,student_id):
		result,h = self.db.query_data("SELECT transaction_id,studentUsername,fine FROM transactions where fine>0")         
		return result,h
	
	def analyse_data(self):
		result,h = self.db.query_data("SELECT studentUsername,count(*) AS 'num',sum(fine) AS fine FROM transactions GROUP BY studentUsername")
		return result,h

	def update_return_date(self,return_date,student_id,transaction_id):
		self.db.query("UPDATE transactions SET returnDate='"+str(return_date) +"' where studentUsername='"+str(student_id)+"' AND transaction_id  "+str(transaction_id))
		self.db.commit()


