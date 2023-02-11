import mysql.connector
import glob
import json
import csv
from io import StringIO
import itertools
import hashlib
import os
import cryptography
from cryptography.fernet import Fernet
from math import pow

class database:

    def __init__(self, purge = False):

        # Grab information from the configuration file
        self.database       = 'db'
        self.host           = '127.0.0.1'
        self.user           = 'master'
        self.port           = 3306
        self.password       = 'master'
        self.tables         = ['institutions', 'positions', 'experiences', 'skills','feedback', 'users']
        
        # NEW IN HW 3-----------------------------------------------------------------
        self.encryption     =  {   'oneway': {'salt' : b'averysaltysailortookalongwalkoffashortbridge',
                                                 'n' : int(pow(2,5)),
                                                 'r' : 9,
                                                 'p' : 1
                                             },
                                'reversible': { 'key' : '7pK_fnSKIjZKuv_Gwc--sZEMKn2zc8VvD6zS96XcNHE='}
                                }
        #-----------------------------------------------------------------------------

    def query(self, query = "SELECT * FROM users", parameters = None):

        cnx = mysql.connector.connect(host     = self.host,
                                      user     = self.user,
                                      password = self.password,
                                      port     = self.port,
                                      database = self.database,
                                      charset  = 'latin1'
                                     )


        if parameters is not None:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query, parameters)
        else:
            cur = cnx.cursor(dictionary=True)
            cur.execute(query)

        # Fetch one result
        row = cur.fetchall()
        cnx.commit()

        if "INSERT" in query:
            cur.execute("SELECT LAST_INSERT_ID()")
            row = cur.fetchall()
            cnx.commit()
        cur.close()
        cnx.close()
        return row

    def about(self, nested=False):    
        query = """select concat(col.table_schema, '.', col.table_name) as 'table',
                          col.column_name                               as column_name,
                          col.column_key                                as is_key,
                          col.column_comment                            as column_comment,
                          kcu.referenced_column_name                    as fk_column_name,
                          kcu.referenced_table_name                     as fk_table_name
                    from information_schema.columns col
                    join information_schema.tables tab on col.table_schema = tab.table_schema and col.table_name = tab.table_name
                    left join information_schema.key_column_usage kcu on col.table_schema = kcu.table_schema
                                                                     and col.table_name = kcu.table_name
                                                                     and col.column_name = kcu.column_name
                                                                     and kcu.referenced_table_schema is not null
                    where col.table_schema not in('information_schema','sys', 'mysql', 'performance_schema')
                                              and tab.table_type = 'BASE TABLE'
                    order by col.table_schema, col.table_name, col.ordinal_position;"""
        results = self.query(query)
        if nested == False:
            return results

        table_info = {}
        for row in results:
            table_info[row['table']] = {} if table_info.get(row['table']) is None else table_info[row['table']]
            table_info[row['table']][row['column_name']] = {} if table_info.get(row['table']).get(row['column_name']) is None else table_info[row['table']][row['column_name']]
            table_info[row['table']][row['column_name']]['column_comment']     = row['column_comment']
            table_info[row['table']][row['column_name']]['fk_column_name']     = row['fk_column_name']
            table_info[row['table']][row['column_name']]['fk_table_name']      = row['fk_table_name']
            table_info[row['table']][row['column_name']]['is_key']             = row['is_key']
            table_info[row['table']][row['column_name']]['table']              = row['table']
        return table_info



    def createTables(self, purge=False, data_path = 'flask_app/database/'):
        print('I create and populate database tables.')
        
        table_list = ['institutions','positions', 'experiences', 'skills', 'feedback', 'users']
        
        for table in table_list[::-1]:
            self.query('DROP TABLE IF EXISTS {};'.format(table))

        for table in table_list:  
            sql_file = open(data_path + "create_tables/" + table + ".sql")
            sql = sql_file.read()
            sql = sql.replace("\n", " ")
            self.query(sql)

        csv_list = ['institutions','positions', 'experiences', 'skills']
        for table in csv_list:
            csv_file = open(data_path + "initial_data/" + table + ".csv")
            reader = csv.reader(csv_file)
            columns = next(reader, None)
            parameters = []
            for line in reader:
                parameters.append(line)
            self.insertRows(table, columns, parameters)
        


    def insertRows(self, table='table', columns=['x','y'], parameters=[['v11','v12'],['v21','v22']]):
        print('I insert things into the database.')
        tup_col = str(tuple(columns))
        x = tup_col.replace("'", "").replace('"', "")
        x = "INSERT INTO {} (".format(table)
        for column in columns:
            x += column + ','
        x = x[:-1] + ") VALUES ("
        for parameter in parameters:
            string = ''
            string = x
            for i in range(len(parameter)):
                parameter[i] = parameter[i].strip()
                if parameter[i].isdigit():
                    parameter[i] = int(parameter[i])
                    string += str(parameter[i]) + ","
                elif parameter[i] == 'NULL':
                    string += parameter[i] + ","
                    parameter[i] = None
                else:
                    string += '"' + parameter[i] + '"' + ","
            query_str = (string[:-1] + ");")
            self.query(query_str)




    def getResumeData(self):
        tables = ['institutions','positions', 'experiences', 'skills']

        institutions_list = self.query("SELECT * FROM {}".format(tables[0]))
        positions_list = self.query("SELECT * FROM {}".format(tables[1]))
        experiences_list = self.query("SELECT * FROM {}".format(tables[2]))
        skills_list = self.query("SELECT * FROM {}".format(tables[3]))

        resume_dict = {}

        for institutions_dict in institutions_list:
            institutions_num = 0
            for key, value in institutions_dict.items():
                if key == "inst_id":
                    institutions_num = value
                    resume_dict[institutions_num] = {}
                else:
                    resume_dict[institutions_num][key] = value
            resume_dict[institutions_num]['positions'] = {}
            for positions_dict in positions_list:
                if positions_dict['inst_id'] != institutions_num:
                    continue
                position_num = 0
                for key, value in positions_dict.items():
                    if key == "position_id":
                        position_num = value
                        resume_dict[institutions_num]['positions'][position_num] = {}
                    else:
                        resume_dict[institutions_num]['positions'][position_num][key] = value
                resume_dict[institutions_num]['positions'][position_num]['experiences'] = {}
                for experiences_dict in experiences_list:
                    if experiences_dict['position_id'] != position_num:
                        continue
                    experience_num = 0
                    for key, value in experiences_dict.items():
                        if key == 'experience_id':
                            experience_num = value
                            resume_dict[institutions_num]['positions'][position_num]['experiences'][experience_num] = {}
                        else:
                            resume_dict[institutions_num]['positions'][position_num]['experiences'][experience_num][key] = value
                    resume_dict[institutions_num]['positions'][position_num]['experiences'][experience_num]['skills'] = {}
                    for skills_dict in skills_list:
                        if skills_dict['experience_id'] != experience_num:
                            continue
                        skills_num = 0
                        for key, value in skills_dict.items():
                            if key == 'skill_id':
                                skills_num = value
                                resume_dict[institutions_num]['positions'][position_num]['experiences'][experience_num]["skills"][skills_num] = {}
                            else:
                                resume_dict[institutions_num]['positions'][position_num]['experiences'][experience_num]["skills"][skills_num][key] = value
                                      
        return resume_dict

#######################################################################################
# AUTHENTICATION RELATED
#######################################################################################
    def createUser(self, email='me@email.com', password='password', role='user'):
        select = list(self.query("SELECT email, role, password FROM users WHERE email = '{}';".format(email)))
        if len(select) != 0:
            return {'success': 0}
        self.query("INSERT INTO users (role, email, password) VALUES ('{}', '{}', '{}')".format(role, email, self.onewayEncrypt(password)))
        return {'success': 1}

    def authenticate(self, email='me@email.com', password='password'):
        select = list(self.query("SELECT email, role, password FROM users WHERE email = '{}';".format(email)))
        if len(select) == 0:
            return {'success': 0}
        print("Query information: ", select)
        if select[0]['password'] == self.onewayEncrypt(password):
            return {'success': 1}
        return {'success': 0}

    def onewayEncrypt(self, string):
        encrypted_string = hashlib.scrypt(string.encode('utf-8'),
                                          salt = self.encryption['oneway']['salt'],
                                          n    = self.encryption['oneway']['n'],
                                          r    = self.encryption['oneway']['r'],
                                          p    = self.encryption['oneway']['p']
                                          ).hex()
        return encrypted_string


    def reversibleEncrypt(self, type, message):
        fernet = Fernet(self.encryption['reversible']['key'])
        
        if type == 'encrypt':
            message = fernet.encrypt(message.encode())
        elif type == 'decrypt':
            message = fernet.decrypt(message).decode()

        return message


