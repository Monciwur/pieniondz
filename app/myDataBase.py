import sqlite3
import sys
import os

class DataBase():
	def __init__(self):
		self.dbPath = "dataBase.db"
		if not os.path.isfile(self.dbPath):
			self.createNewDB()

	def createNewDB(self):
		try:
			self.connection = sqlite3.connect(self.dbPath)
			self.cursorobj = self.connection.cursor()
			query = '''CREATE TABLE payments
					 (ID INTEGER PRIMARY KEY,
					 username varchar(15) NOT NULL,
					 product varchar(60) NOT NULL,
					 price integer(8) NOT NULL,
					 konChkBox integer(1) NOT NULL,
					 matChkBox integer(1) NOT NULL,
					 szyChkBox integer(1) NOT NULL,
					 payTime varchar(18) NOT NULL)'''
			self.cursorobj.execute(query)
			self.connection.commit()
		except:
			sys.exit(1)

	def executeFetchall(self, query, para):
		try:
			self.connection = sqlite3.connect(self.dbPath)
			self.cursorobj = self.connection.cursor()
			self.cursorobj.execute(query, para)
			self.result = self.cursorobj.fetchall()
			self.connection.commit()
			return self.result
		except:
			return None

	def executeFetchone(self, query, para):
		try:
			self.connection = sqlite3.connect(self.dbPath)
			self.cursorobj = self.connection.cursor()
			self.cursorobj.execute(query, para)
			self.result = self.cursorobj.fetchone()
			self.connection.commit()
			return self.result
		except:
			return None

	def createProduct(self, username, product, price, konChkBox, matChkBox, szyChkBox, payTime):
		query = ''' INSERT INTO payments (username, product, price, konChkBox, matChkBox, szyChkBox, payTime) VALUES (?, ?, ?, ?, ?, ?, ?) '''
		self.executeFetchall(query, (username, product, price, konChkBox, matChkBox, szyChkBox, payTime))

	def showHistory(self):
		query = '''SELECT username, product, price, konChkBox, matChkBox, szyChkBox, payTime FROM payments'''
		result = self.executeFetchall(query, ())
		if result is None:
			return False
		else:
			return result

	def exitDataBase(self):
		self.connection.close()
