import time

def today():
    # returns the number of days since the epoch
    return int(time.time()) // (60 * 60 * 24)

def getid(conn, table):
    # returns a unique card id
    maxid = conn.execute(f'select max(id) from {table}').fetchone()[0]
    return maxid + 1 if maxid is not None else 1
