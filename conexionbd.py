import logging
import json
import sys
import time
from clases import encriptar
from datetime import datetime
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery, QSqlTableModel
from PyQt5.QtWidgets import QTableView, QApplication


hoy = time.strftime("%d/%m/%y")

current_date = datetime.now().strftime('%d-%m-%y')

logformatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger()

fileHandler = logging.FileHandler('logs/{}.log'.format(current_date))
fileHandler.setFormatter(logformatter)
fileHandler.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logformatter)
consoleHandler.setLevel(logging.INFO)

logger.addHandler(fileHandler)  # este escribe en el archivo
logger.addHandler(consoleHandler)
logger.setLevel(logging.INFO)

logging.info('This is a test logger.')

if len(sys.argv) != 2:
    logger.error('No config paremeter has supplied')
    sys.exit(1)

db_server = sys.argv[1]

""""
conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server="+db_host+";"
    "UID="+db_username+";"
    "PWD="+db_password+";"
    "Database="+db_db_name
)
"""


def connectionBD():
    try:
        config_file = 'config/{}/config.json'.format(db_server)
        with open(config_file) as json_data:
            config = json.load(json_data)
    except Exception as e:
        logger.error('No such config file has found: {}'.format(config_file))
        sys.exit(1)

    db_host = config['c_server']
    db_db_name = config['c_database']
    db_username = config['c_uid']
    db_password = config['c_pwd']

    connString = f'DRIVER={{SQL Server}};'\
                 f'SERVER={db_host};'\
                 f'DDATABASE={db_db_name};'\
                 f'UID={db_username};'\
                 f'PWD={db_password}'

    global db
    db = QSqlDatabase.addDatabase('QODBC')
    db.setDatabaseName(connString)

    if db.open():
        print('Conexion exitosa')
        return True
    else:
        print('Conexion fallida')
        print(db.lastError().text())
        return False


def consultaData(sqlStatement):
    print('Procesando Query...')
    query = QSqlQuery(db)
    query.prepare(sqlStatement)
    query.exec()

    model = QSqlQueryModel()
    model.setQuery(query)

    model2 = QSqlTableModel()
    model2.setTable("admusuario")
    model2.setEditStrategy(QSqlTableModel.OnManualSubmit)
    model2.select()
    print(model2)

    # view = QTableView()


def ejecutaQuery():
    print("Read")
    if connectionBD():
        SQL_STATEMENT = 'SELECT * FROM admusuario where usuario='
        dataView = consultaData(SQL_STATEMENT)
        dataView.show()


ejecutaQuery()


def displayData(sqlStatement):
    print('Procesando Query...')
    query = QSqlQuery(db)
    query.prepare(sqlStatement)
    query.exec()

    model = QSqlQueryModel()
    model.setQuery(query)

    view = QTableView()
    view.setModel(model)
    view.close()
    return view


def readData():
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        if connectionBD():
            SQL_STATEMENT = 'SELECT * FROM admusuario where usuario='
            dataView = displayData(SQL_STATEMENT)
            dataView.show()
        app.exit()
        app.exit(app.exec_())


def read(conn):
    print("Read")
    query = "Select usuario, clave, descripcion_usuario, fechacreacion, fechavencimiento, estado, email from admusuario"
    cursor = conn.cursor()
    cursor.execute(query)
    for row in cursor:
        print(f'row = {row}')
    print()


def create(conn):
    print("Create")
    cursor = conn.cursor()
    cursor.execute(
        'insert into admusuario(usuario, clave, descripcion_usuario, fechacreacion, fechavencimiento, estado, email) values (?,?,?,?,?,?,?)',
        ('18509118', encriptar.PassEncriptar('123456', 'E'), 'Administrador', hoy, '01/01/2030', 1, 'gerenciageneral.pe@niviglobal.com')
    )
    conn.commit()
    read(conn)


def update(conn, a, b):
    print("Update")
    cursor = conn.cursor()
    cursor.execute(
        'update admusuario set  clave = ? where usuario = ?;',
        (encriptar.PassEncriptar(a, 'E'), b)
    )
    conn.commit()
    read(conn)


def delete(conn):
    print("Delete")
    cursor = conn.cursor()
    cursor.execute(
        'delete from admusuario where usuario ="43185131"'
    )
    conn.commit()
    read(conn)


#readData()

#read(conn)
# update(conn, '123', '43185131')
# create(conn)
# delete(conn)

#conn.close()
