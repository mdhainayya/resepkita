import json
from flask import Flask, abort, jsonify, redirect, request, url_for, session, render_template
from flask_mysqldb import MySQL
from __init__ import mysql

# FUNCTION

# Menambahkan resep baru
def add_recipe():
    data = []
    bahan = []
    
    if request.json:
        request.get_json(force = True)
        id = 8
        nama = request.json["nama"]
        bahan = request.json["bahan"]
        langkah = request.json["langkah"]
        tipe = request.json["tipe"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO resep (id, nama, bahan, langkah, tipe) VALUES (%s, %s, %s, %s, %s)", [id, nama, bahan, langkah, tipe])
    else:
        details = request.form
        id = 8
        nama = details["nama"]
        bahan_form = details["bahan"]
        langkah = details["langkah"]
        tipe = details["tipe"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO resep (id, nama, bahan, langkah, tipe) VALUES (%s, %s, %s, %s, %s)", [id, nama, bahan_form, langkah, tipe])
    
    
    data = {
        'code': 201,
        'message': 'Resep berhasil ditambahkan',
        'data': nama
    }

    cur.execute("INSERT INTO log (method, tag, response, timestamp) VALUES ('POST', 'resep', %s, CURRENT_TIMESTAMP())", [data['code']])
    
    mysql.connection.commit()
    cur.close()

    if bahan:
        return data
    else:
        return render_template("addindex.html", data = data)

# Mengubah resep
def update_recipe(resepid):
    data = []
    bahan = []
    
    if request.json:
        request.get_json(force = True)
        bahan = request.json["bahan"]
        langkah = request.json["langkah"]
        tipe = request.json["tipe"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM resep WHERE resepid = %s", [resepid])
        record = cur.fetchone()

        if record:
            cur.execute("UPDATE resep SET bahan = %s, langkah = %s, tipe = %s  WHERE resepid = %s", [bahan, langkah, tipe, resepid])
                    
            data = {
                'code': 200,
                'message': 'Resep berhasil diperbarui',
                'data': get_recipe(resepid)['data']
            }
        else:
            data = {
                'code': 401,
                'message': 'Resep tidak ditemukan',
                'data': ''
            }

    else:
        details = request.form
        bahan_form = details["bahan"]
        langkah = details["langkah"]
        tipe = details["tipe"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM resep WHERE resepid = %s", [resepid])
        record = cur.fetchone()

        if record:
            cur.execute("UPDATE resep SET bahan = %s, langkah = %s, tipe = %s  WHERE resepid = %s", [bahan_form, langkah, tipe, resepid])
                    
            data = {
                'code': 200,
                'message': 'Resep berhasil diperbarui',
                'data': get_recipe(resepid)['data']
            }
        else:
            data = {
                'code': 401,
                'message': 'Resep tidak ditemukan',
                'data': ''
            }

    
    cur.execute("INSERT INTO log (method, tag, response, timestamp) VALUES ('PUT', 'resep', %s, CURRENT_TIMESTAMP())", [data['code']])
        
    mysql.connection.commit()
    cur.close()

    if bahan:
        return data
    else:
        return render_template("updindex2.html", data = data)

# Menghapus resep
def delete_recipe(resepid):
    data = []

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM resep WHERE resepid = %s", [resepid])
    record = cur.fetchone()

    if record:
        cur.execute("DELETE FROM resep WHERE resepid = %s", [resepid])
            
        data = {
            'code': 200,
            'message': 'Resep berhasil dihapus',
            'data': ''
        }
    else:
        data = {
            'code': 401,
            'message': 'Resep tidak ditemukan',
            'data': ''
        }

    cur.execute("INSERT INTO log (method, tag, response, timestamp) VALUES ('DELETE', 'resep', %s, CURRENT_TIMESTAMP())", [data['code']])
    
    mysql.connection.commit()
    cur.close()

    return data

# Melihat resep detail untuk suatu resep
def get_recipe(resepid):
    data = []

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM resep WHERE resepid = %s", [resepid])
    record = cur.fetchone()

    if record:
        record_data = resep_format(record)
        data = {
            'code': 200,
            'message': 'Resep berhasil didapatkan',
            'data': record_data
        }
    else:
        data = {
            'code': 401,
            'message': 'Resep tidak ada',
            'data': ''
        }
    cur.execute("INSERT INTO log (method, tag, response, timestamp) VALUES ('GET', 'resep', %s, CURRENT_TIMESTAMP())", [data['code']])
        
    mysql.connection.commit()
    cur.close()

    return data

# Transformasi resep
def resep_format(data):
    api_data = {
        'nama': data[5],
        'bahan': data[2],
        'langkah': data[3],
        'tipe': data[4]
    }
    return api_data

def transform(data):
    array = []
    for i in data:
        array.append(resep_format(i))
    return array