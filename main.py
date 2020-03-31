from bottle import route, request, run, response, template, redirect, static_file
import json
import dblib

decod = lambda x : x.encode("latin-1").decode("utf-8")

@route("/")
def index():
    return template("template/main.html")

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='static/')

@route('/page/<name>')
def return_pages(name):
    config = json.load(open('pages/'+str(name)+'.json','r'))
    colnames = []
    for i in config['colums']:
        for j in config['colums'][i]["include"]:
            if j not in colnames:
                colnames.append(j)
    struct = []
    for i in config['colums']:
        struct.append(0)
        
        for j in config['colums'][i]['include']:
            struct[-1] += 1

    print(struct)
    buf_bas = dblib.dbLib().getFields(*colnames)

    print(buf_bas)
    return template('template/table.html', config=config, bas=buf_bas, struct=struct)

run(host="0.0.0.0", port="80")
