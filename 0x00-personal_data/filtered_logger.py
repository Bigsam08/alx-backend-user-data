#!/usr/bin/env python3
''' filter_drum function that returns a log message obfuscated'''
import re
import logging
from typing import List
import mysql.connector
import os

PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        ''' initialize class,
        accept a list of string fields
         '''
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''filter_datum to filter incoming logs
        values for fields in fields is filtered '''
        msg = super(RedactingFormatter, self).format(record)
        text = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return text


def filter_datum(fields, readaction, message, seperator):
    return re.sub(f'({"|".join(fields)})=.*?(?={seperator}|$)',
                  f'\\1={readaction}', message)


def get_logger() -> logging.Logger:
    ''' takes no arguments and return logging.Logger object'''
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    streamHandler = logging.StreamHandler()
    logger.propagate = False
    streamHandler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streamHandler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    ''' conncet to database'''
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', '')
    db_user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_pwd = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')

    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
        )
    return connection


def main():
    ''' obatain database connection using get_db function
    and retrive all rows in the users table'''
    logger = get_logger()
    logger.setLevel(logging.INFO)

    db = get_db()
    cur = db.cursor()
    cur.execute('SELECT * FROM users')
    rows = cur.fetchall()
    for row in rows:
        msg = "; ".join([f'{field}={row[field]}' for field in row.keys()])
        logger.info(filter_datum(PII_FIELDS, RedactingFormatter.REDACTION,
                                 msg, RedactingFormatter.SEPARATOR))


if __name__ == '__main__':
    main()
