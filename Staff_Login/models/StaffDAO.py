class StaffDAO:
    def __init__(self,DAO):
        self.db = DAO
        self.db.table = "staff" 
	
    def add(self,staffName, staffUsername, password):
        self.db.query("INSERT INTO @table (staffName, staffUsername, password) VALUES(%s, %s, %s)",(staffName, staffUsername, password))

    def getUser(self,staffUsername):
        result,h = self.db.query("SELECT * FROM staff WHERE staffUsername = '{}'".format(staffUsername))
        return result,h
    

