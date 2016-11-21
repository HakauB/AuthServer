import sqlite3

class sqlActions:

    @staticmethod
    def add_Motion(db, devId, timestamp, now, data):
        conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        c = conn.cursor()
        entryTuple = (timeStamp, now, devId)
        dataTuple = (data)
        print entryTuple
        print data[0]
        if len(data) == 1:
            c.execute('pragma foreign_keys')
            c.execute('begin')
            try:
                c.execute('INSERT INTO entry VALUES(?, ?, ?, (select max(seq) from entry) + 1)', entryTuple)
                c.execute('INSERT INTO motion VALUES(?, ?, ?, ?, ?, ?, ?, ?, ? , (select max(seq) from entry))', dataTuple)
                conn.commit()
                print("L0")
            except:
                try:
                    try:
                        c.execute('INSERT INTO entry VALUES(?, ?, ?, 0)', entryTuple)
                        c.execute('INSERT INTO motion VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, (select max(seq) from entry))', dataTuple)
                        conn.commit()
                        print("L1")
                    finally:
                        a=1 # Do Nothing
                except:
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60
                    print('INSERT failed')
        else:
            print("Wrong data count: ", len(data))

    @staticmethod
    def add_Lux(db, devId, timestamp, now, data):
        conn = sqlite3.connect(db, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        c = conn.cursor()
        entryTuple = (timeStamp, now, devId)
        print entryTuple
        print data[0]
        if len(data) == 1:
            c.execute('pragma foreign_keys')
            c.execute('begin')
            try:
                c.execute('INSERT INTO entry VALUES(?, ?, ?, (select max(seq) from entry) + 1)', entryTuple)
                c.execute('INSERT INTO lux VALUES(?, (select max(seq) from entry))', (data[0],))
                conn.commit()
                print("L0")
            except:
                try:
                    try:
                        c.execute('INSERT INTO entry VALUES(?, ?, ?, 0)', entryTuple)
                        c.execute('INSERT INTO lux VALUES(?, (select max(seq) from entry))', (data[0],))
                        conn.commit()
                        print("L1")
                    finally:
                        a=1 # Do Nothing
                except:
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60
                    print('INSERT failed')
        else:
            print("Wrong data count: ", len(data))
        conn.close()
