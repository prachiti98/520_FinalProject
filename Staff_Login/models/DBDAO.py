from copy import copy

# from Models.BookDAO import BookDAO
from models.StudentDAO import StudentDAO
# from Models.AdminDAO import AdminDAO

from models.DB import DB

class DBDAO(DB):
	def __init__(self, app):
		super(DBDAO, self).__init__(app)

		# self.book = BookDAO(copy(self))
		self.student = StudentDAO(copy(self))
		# self.admin = AdminDAO(copy(self))