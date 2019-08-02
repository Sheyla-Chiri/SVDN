# -*- encoding: utf-8 -*-
# ------------------------------------------------------------------------#
# Programa: SVDN ENTERPRISE 1.0			                                  #
# ------------------------------------------------------------------------#
# Propósito: conexion a la BD                                             #
# ------------------------------------------------------------------------#
# Autor: Sheyla Chiri                                                     #
# ------------------------------------------------------------------------#
# Fecha: 31/07/2019                                                       #
# ------------------------------------------------------------------------#

import logging
import json
import sys
from datetime import datetime
from PyQt5.QtSql import QSqlDatabase, QSqlQuery


def conexion():           # funcion para realizarconsulta
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

    # Se leen los datos del archivo config.json

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

    # conectamos a la BD
    connString = f'DRIVER={{SQL Server}};' \
        f'SERVER={db_host};' \
        f'DDATABASE={db_db_name};' \
        f'UID={db_username};' \
        f'PWD={db_password}'

    global db
    db = QSqlDatabase.addDatabase('QODBC')
    db.setDatabaseName(connString)

    if db.open():
        print('Conexion exitosa')
    else:
        print('Conexion fallida')
        print(db.lastError().text())
        return False


def consultas(consulta):
    conexion()
    # segun yo checa si la primera palabra del la consulta el select
    if QSqlQuery.isSelect(consulta):
        # realiza la consulta y lo almacena en query
        query = QSqlQuery(db)
        query.prepare(consulta)
        query.exec()
        print(query.exec)
    # si no es select hace las modificaciones a la BD
    else:
        # hace efectiva la escritura de los datos
        query = QSqlQuery(db)
        query.prepare(consulta)
        query.exec()
        # datos se vuelve en nada
