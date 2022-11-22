from config import mysql as cfg
import pymysql

def connect():
    return pymysql.connect(host=cfg['location'], user=cfg['user'], password=cfg['password'], database=cfg['database'])
