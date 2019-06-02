import time

def today():
    # returns the number of days since the epoch
    return int(time.time()) // (60 * 60 * 24)

def getid(conn, table):
    # returns a unique card id
    maxid = conn.execute(f'select max(id) from {table}').fetchone()[0]
    return maxid + 1 if maxid is not None else 1

def validate_dotted_name(name):
    """If @name is not a valid dotted name, a ValueError is
    raised. Otherwise, a list of the names is returned"""
    names = name.split()
    for name in names:
        if not name:
            raise ValueError(f'Invalid dotted name: "{name}"')
    return names
        
