from __init__ import app
from flask import Flask, abort, jsonify, redirect, request, url_for
from dbcontroller import *
from auth import *
from auth_decorator import login_required

# ROUTING API
@app.route('/resepku', methods=['POST'])
@app.route('/resepku/<int:id>', methods=['PUT', 'DELETE', 'GET'])
# @login_required
def resepku(id=None):
    if request.method == 'POST':
        return add_recipe()
    elif request.method == 'PUT':
        return update_recipe(id)
    elif request.method == 'DELETE':
        return delete_recipe(id)
    elif request.method == 'GET':
        return get_recipe(id)


# ROUTING WEBPAGE SELAIN API
@app.route('/', methods=['GET'])
def root():
    return "ResepKita API"

@app.route('/homepage', methods=['GET'])
# @login_required
def homepage():
    return render_template("index.html")

@app.route('/homepage/get', methods=['GET', 'POST'])
@login_required
def homepage_get():
    data = ''
    if request.method == 'POST':
        details = request.form
        resepid = details['resepid']
    
        data = get_recipe(resepid)
    return render_template("getindex.html", data = data)

@app.route('/homepage/delete', methods=['POST', 'GET'])
@login_required
def homepage_delete():
    data = ''
    if request.method == 'POST':
        details = request.form
        resepid = details['resepid']
    
        data = delete_recipe(resepid)
    return render_template("delindex.html", data = data)

@app.route('/homepage/add', methods=['POST', 'GET'])
@login_required
def homepage_add():
    data = ''
    if request.method == 'POST':
        return add_recipe()
    return render_template("addindex.html", data = data)

@app.route('/homepage/update', methods=['POST', 'GET'])
@login_required
def homepage_update():
    data = []
    if request.method == 'POST':
        details = request.form
        resepid = details['resepid']

        print(resepid)
    
        data = get_recipe(resepid)

        return redirect(url_for('homepage_update_form', id = resepid, data = data))
    
    return render_template("updindex.html", data = data)

@app.route('/homepage/update/done/<id>/<data>', methods=['POST', 'GET'])
@login_required
def homepage_update_form(id, data):
    if request.method == "POST":
        print("masuk")
        return update_recipe(id)
    return render_template("updindex2.html", data = data)

@app.route('/login')
def login():
    return login_funct()

@app.route('/authorize')
def authorize():
    return authorize_funct()

@app.route('/logout')
def logout():
    return logout_funct()

@app.route('/register')
def register():
    return render_template("register.html")


# RUNNER
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)

# RUNNER
# if __name__ == '__main__':
#     app.run(debug=True)