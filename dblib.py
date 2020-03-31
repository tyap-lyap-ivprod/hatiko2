import sqlite3

class dbLib:
    def __init__(self):
        self.conn = sqlite3.connect("hz.db")
        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("SELECT * FROM appointment LIMIT 1")
            self.cursor.fetchall()
        except sqlite3.OperationalError:
            self.cursor.execute("""CREATE TABLE appointment ( 
                                       id INTEGER PRIMARY KEY,
                                       fio TEXT NOT NULL,
                                       birthdate TEXT NOT NULL,
                                       addr TEXT,
                                       distr TEXT,
                                       phone TEXT,
                                       service TEXT,
                                       symptoms TEXT,
                                       diagnoz TEXT,
                                       create_date TEXT NOT NULL,
                                       create_time TEXT NOT NULL,
                                       del INTEGER DEFAULT 0,
                                       paramtb TEXT
                                   );""")

			
	
    def addRecord(self, fio='', birthdate='', addr='', distr='', phone='', service='', symptoms='', diagnoz='', paramtb=''):
        mkrec = """INSERT INTO appointment (fio, birthdate, addr, distr, phone, service, symptoms, diagnoz, create_date, create_time, paramtb) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', date('now'), time('now'), '%s');"""
        self.cursor.execute(mkrec % (fio, birthdate, distr, addr, phone, service, symptoms, diagnoz, paramtb))
        self.conn.commit()
        mkrec = """SELECT * FROM appointment ORDER BY id DESC LIMIT 0"""
        self.cursor.execute(mkrec)
        return self.cursor.fetchall()
        
		
    def getAllRecords(self, limit=(False, 0, 0)):
        if not limit[0]:
            req = """SELECT * FROM appointment ORDER BY id DESC;"""
        else:
            req = """SELECT * FROM appointment ORDER BY id DESC LIMIT %d, %d;""" % (limit[1], limit[2])
        self.cursor.execute(req)
        x = self.cursor.fetchall()
        return x
  
    def getFields(self, *names):
        req = "SELECT "
        for i in names:
            req += i + ","
        req = req[:-1]
        req += " FROM appointment;"
        print(req)
        self.cursor.execute(req)
        return self.cursor.fetchall()

    def getNotDeleted(self, limit=(False, 0, 0)):
        if not limit[0]:
            req = """SELECT * FROM appointment WHERE del = 0 ORDER BY id DESC;"""
        else:
            req = """SELECT * FROM appointment WHERE del = 0 ORDER BY id DESC LIMIT %d, %d;""" % (limit[1], limit[2])
        self.cursor.execute(req)
        x = self.cursor.fetchall()
        return x

    def deleteRecord(self, idr):
        req = """UPDATE appointment SET del = 1 WHERE id = %d;""" % (int(idr))
        self.cursor.execute(req)
        self.conn.commit()
        req = """SELECT * from appointment WHERE id = %d ORDER BY id DESC;""" % (int(idr))
        self.cursor.execute(req)
        return self.cursor.fetchall()
    
    def search(self, idr='-1', fio='', birthdate='', addr='', distr='', phone='', service='', symptoms='', diagnoz='', paramtb=''):
        if idr == "-1":
            idr = "(\n"
        else:
            idr = """(id LIKE %s\nAND""" % (idr)
        req = """
		SELECT * FROM appointment 
		    WHERE 
		        %s(fio LIKE '%%%s%%'
		        AND birthdate LIKE '%%%s%%'
		        AND addr LIKE '%%%s%%'
                        AND disrt LIKE '%%%s%%'
		        AND phone LIKE '%%%s%%'
                        AND service LIKE '%%%s%%'
                        AND diagnoz LIKE '%%%s%%'
                        AND paramtb LIKE '%%%s%%'
                        fio TEXT NOT NULL,
		        )) AND del = 0
		 ORDER BY id DESC;
		""" % (idr, fio, birthdate, addr, distr, addresses, phone, service, symptoms, diagnoz, paramtb)
        print(req)
        self.cursor.execute(req)
        return self.cursor.fetchall()
		
if __name__ == '__main__':
	db = dbLib()
	db.addRecord(
	    str(input("fio:")), 
	    str(input("birthdate:")),
	    str(input("addr:")),
	    str(input("distr")),
            str(input("phone")),
            str(input("service")),
            str(input("diagnoz")),
            str(input("paramtb")),
	)
	print(db.getNotDeleted())

