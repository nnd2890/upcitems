import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import AsIs
import urllib.parse
import os

urllib.parse.uses_netloc.append("postgres")
url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
dbConn = psycopg2.connect(database=url.path[1:], user=url.username, password=url.password, host=url.hostname,port=url.port)
dbCur = dbConn.cursor(cursor_factory=RealDictCursor)

def insert_dict_pg(dict, table):
    columns = dict.keys()
    values = [dict[column] for column in columns]
    insert_statement = 'insert into ' + table + ' (%s) values %s'
    dbCur.execute(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    dbConn.commit()
    print('Inserted to posgres ' + table)


def select_field_where(table, field, name):
    sql = "SELECT * FROM %s WHERE %s ='%s'" % (table, field, name)
    dbCur.execute(sql)
    myresult = dbCur.fetchone()
    return myresult


def update_row(table, dict, id):
    set = ', '.join('{}=%s'.format(k) for k in dict)
    values = tuple(dict[key] for key in dict)
    sql = "UPDATE {0} SET {1} WHERE id = '{2}'".format(table, set, id)
    dbCur.execute(sql, values)
    dbConn.commit()
    print("Updating to database Finished!")


def track_exists_pg(col, table, name):
    dbCur.execute("SELECT " + col + " FROM " + table + " WHERE " + col + " = %s", (name,))
    return dbCur.fetchone() is not None