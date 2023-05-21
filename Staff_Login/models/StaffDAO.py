class StaffDAO:
    def __init__(self,DAO):
        self.db = DAO
        self.db.table = "staff" 
	
    def add_staff(self,staffName, staffUsername, password):
        self.db.query("INSERT INTO @table (staffName, staffUsername, password) VALUES('{}', '{}', '{}')".format(staffName, staffUsername, password))
        self.db.commit()

    def getUser(self,staffUsername):
        result,h = self.db.query("SELECT * FROM staff WHERE staffUsername = '{}'".format(staffUsername))
        return result,h
    

