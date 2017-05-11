import pymysql.cursors
import sys
import itertools

class connectToMySQL():
    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        try:
            self.connection = pymysql.connect(host=self.host,
                                            user=self.user,
                                            password=self.password,
                                            db=self.db,
                                            charset='utf8mb4',
                                            cursorclass=pymysql.cursors.DictCursor)
        except:
            print('Error from ConnectMySQL !')
            print(sys.exc_info())
        self.executeResult = list()
    def executeSQL(self, sqlDict):
        # try:
            if sqlDict['type'] == "INSERT INTO":
                with self.connection.cursor() as cursor:
                    sql = 'INSERT INTO `{}` {} VALUES {} {}'.format(
                        sqlDict['targetTable'],
                        tuple(['`{}`'.format(column)
                               for column in sqlDict['targetColumns']]),
                        tuple(['`{}`'.format(column)
                               for column in sqlDict['targetValues']]),
                        sqlDict['addition']
                    ).strip()
                    cursor.execute(sql)
                    self.connection.commit()
                    self.connection.close()
            elif sqlDict['type'] == "SELECT":
                with self.connection.cursor() as cursor:
                    if sqlDict['targetColumns'] != '*':
                        sql = "SELECT {} FROM {} {}".format(
                            ','.join(['`{}`'.format(column)
                                    for column in sqlDict['targetColumns']]),
                            '`{}`'.format(sqlDict['targetTable']),
                            sqlDict['addition'],
                        ).strip()
                    else:
                        sql = "SELECT * FROM {} {}".format(
                            '`{}`'.format(sqlDict['targetTable']),
                            sqlDict['addition'],
                        ).strip()
                    print('\n\n', sql, '\n\n')
                    cursor.execute(sql)
                    self.executeResult = cursor.fetchall()
                    self.connection.close()
            elif sqlDict['type'] == "SELECT DISTINCT":
                with self.connection.cursor() as cursor:
                    sql = "SELECT DISTINCT {} FROM {} {}".format(
                        '`{}`'.format(sqlDict['targetColumn']),
                        '`data`',
                        sqlDict['addition']
                    ).strip()
                    cursor.execute(sql)
                    self.executeResult = list(filter(lambda x : x != '', sorted([list(result.values())[0] for result in cursor.fetchall()])))
                    self.connection.close()
            elif sqlDict['type'] == "UPDATE":
                # UPDATE "表格"
                # SET "欄位1" = [值1], "欄位2" = [值2]
                # WHERE "條件";
                pass
        # except:
            # print(sys.exc_info())
            # print('Error from executeSQL!')
    def insert(self):
        sql = "INSERT INTO `{targetTable}` {targetCloumns_tuple} VALUES {insertValues} {additions}"
        pass

    def select(self):
        sql = "SELECT {targetColumns} FROM {targetTable} {addition}"
        pass
    
    def update(self):
        pass

    def delete(self):
        pass

    def where(self, *args):
        pass

    def limit(self, start, each):
        return 'LIMIT {}, {}'.format(start, each)