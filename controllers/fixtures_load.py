#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__, template_folder='templates')

@fixtures_load.route('/base/init')
def fct_fixtures_load():
    mycursor = get_db().cursor()
    file = open('sql_projet.sql', 'r')
    sql = file.read().replace(',\n', ',').replace('VALUES\n', 'VALUES').replace('(\n', '(').replace('    ', ' ').replace(')\n', ')').split('\n')
    file.close()
    sql = [i for i in sql if i != '']
    print(sql)
    for line in sql:
        mycursor.execute(line)
    get_db().commit()

    return redirect('/')
