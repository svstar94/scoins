import pymysql

def conn():
    return pymysql.connect(host='ssacdb',
                            port=3306,
                            user='sosin',
                            passwd='1234',
                            db='SCOIN',
                            charset='utf8')

def select(DB, table, column):
    cursor = DB.cursor()
    sql_qr = """
        SELECT {0} FROM {1}
    """.format(column, table)
    cursor.execute(sql_qr)
    return cursor.fetchall()

def insert(DB, table, columns, values):
    cursor = DB.cursor()
    sql_qr2 = """
        INSERT INTO {0}({1})
        VALUES ({2})
    """.format(table, columns, values)
    cursor.execute(sql_qr2)
    DB.commit()

def insert(DB, table, columns, values):
    cursor = DB.cursor()
    sql_qr2 = """
        INSERT INTO {0}({1})
        VALUES ({2})
    """.format(table, columns, values)
    cursor.execute(sql_qr2)
    DB.commit()

def update(DB, table, set_content, where_content):
    cursor = DB.cursor()
    sql_qr3 = """
        UPDATE {0}
        SET {1}
        WHERE {2}
    """.format(table, set_content, where_content)
    cursor.execute(sql_qr3)
    DB.commit()

def delete(DB, table, where_content):
    cursor = DB.cursor()
    sql_qr4 = """
        DELETE FROM {0} WHERE {1}
    """.format(table, where_content)
    cursor.execute(sql_qr4)
    DB.commit()

# class Python2DB():

#     def __init__(self):
#         self.EF_DB = pymysql.connect(host='localhost',
#                                 port=3306,
#                                 user='root',
#                                 passwd='1234',
#                                 db='SCOIN',
#                                 charset='utf8')

#         # self.cursor = self.EF_DB.cursor()

#     def select(self, table, column):
#         self.cursor = self.EF_DB.cursor()
#         sql_qr = """
#             SELECT {0} FROM {1}
#         """.format(column, table)
#         self.cursor.execute(sql_qr)
#         return self.cursor.fetchall()

#     def insert(self, table, columns, values):
#         self.cursor = self.EF_DB.cursor()
#         sql_qr2 = """
#             INSERT INTO {0}({1})
#             VALUES ({2})
#         """.format(table, columns, values)
#         self.cursor.execute(sql_qr2)
#         self.EF_DB.commit()

#     def update(self, table, set_content, where_content):
#         self.cursor = self.EF_DB.cursor()
#         sql_qr3 = """
#             UPDATE {0}
#             SET {1}
#             WHERE {2}
#         """.format(table, set_content, where_content)
#         self.cursor.execute(sql_qr3)
#         self.EF_DB.commit()

#     def delete(self, table, where_content):
#         self.cursor = self.EF_DB.cursor()
#         sql_qr4 = """
#             DELETE FROM {0} WHERE {1}
#         """.format(table, where_content)
#         self.cursor.execute(sql_qr4)
#         self.EF_DB.commit()