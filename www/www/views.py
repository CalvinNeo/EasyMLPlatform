#coding:utf8
from django.http import HttpResponse
from django.shortcuts import render_to_response
import MySQLdb

def first_page(request):
    db = MySQLdb.connect(user='root', db='mlplatform', passwd='80868086', host='localhost')
    cursor = db.cursor()
    cursor.execute('SELECT * FROM dataset ORDER BY id')
    names = [row[0] for row in cursor.fetchall()]
    db.close()
    return render_to_response('list.html', {'names': names})