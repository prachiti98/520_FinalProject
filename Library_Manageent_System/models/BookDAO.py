class BookDAO():
    def __init__(self, DAO):
        self.db = DAO
        self.db.table = "books"

    def getBooks(self):
        result,h = self.db.query("SELECT bookName, sum(available) AS count FROM books GROUP BY bookName")
        return result,h
    
    def unavailable_books(self):
        result,h = self.db.query_data("SELECT bookName from books where available = 0 group by bookName")
        return result,h
        
    def getStaffBooks(self):
        result,h = self.db.query("SELECT bookName, author, count(bookName) AS count, sum(available) as available FROM books GROUP BY bookName, author ORDER BY count(bookName) DESC")
        return result,h
    
    def add_book(self, bookName, author):
        self.db.query("INSERT INTO books( bookName, author) VALUES('{}', '{}')".format(bookName, author)) 
        self.db.commit()

    def delete_book(self, bookName, author):
        self.db.query("DELETE FROM @table WHERE bookName = {} AND  author = {}".format(bookName, author)) 
    

    def get_issue_book(self,bookName):
        print("SELECT * FROM @table WHERE bookName = {} AND available = 1 LIMIT 1".format(bookName))
        result,h = self.db.query_data("SELECT * FROM @table WHERE bookName = '{}' AND available = 1 LIMIT 1".format(bookName)) 
        return result,h
    
    def issue_book(self,book):
        self.db.query("UPDATE @table SET available = 0 WHERE book_id = "+str(book['book_id'])+"")
        self.db.commit()

    def set_availble(self,book_id):
        self.db.query("UPDATE @table SET available = 1 where book_id = "+str(book_id)+" ")
        self.db.commit()

    def search_book(self,name):
        result,h = self.db.query_data("SELECT bookName, author, count(bookName) AS count, sum(available) as available FROM books WHERE bookName LIKE '%{}%' GROUP BY bookName, author ORDER BY count(bookName) DESC".format(name))
        return result,h