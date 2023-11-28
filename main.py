from flask import Flask, render_template, redirect
import datetime
import ast
import validators
global occasions
occasions = []

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

with open('db.txt', 'r', encoding='utf8') as file:

    occasions = ast.literal_eval( file.read() )
    print(occasions)


c = 0
for i in occasions:
    e = i["date"] # '17.01.2022'
    res = datetime.datetime.now() - datetime.datetime.strptime(e, '%d.%m.%Y')  # 7 days, 7:27:30.668602
    print( res.days )
    if res.days >= 14:
        occasions.pop(c)
        with open('db.txt', 'w', encoding='utf8') as file:
            file.write(str(occasions))
    c += 1

print(occasions)
# regex [0-9] [a-d]
# https://domen.com/l/45fdgf


# http://127.0.0.1:3007/savelink/dfgsdf43/https%3A%2F%2Fdeveloper.mozilla.org%2Fen-US%2Fdocs%2FWeb%2FJavaScript%2FReference%2FGlobal_Objects%2F
@app.route("/savelink/<short>/<long>")
def savelink(short, long):
    short = short.replace('↔', '/')
    long = long.replace('↔', '/')
    if not validators.url(long):
        return {'status': 'url error'}
    if len(short) < 2 or len(short) > 15:
        return {'status': 'short error'}
    for i in occasions:
        if i["short"] == short:
            return {'status': 'unique error'}

    print('good')
    try:
        print('process save link')
        mon = datetime.datetime.today().month
        day = datetime.datetime.today().day
        year = datetime.datetime.today().year
        occasions.append({'long': long, 'short': short, 'date': f'{day}.{mon}.{year}'})
        with open('db.txt', 'w', encoding='utf8') as file:
            file.write(str(occasions))
        return {'status': 'ok'}
    except:
        return {'status': 'error'}
    finally:
        print('finish')



@app.route("/l/<link>")
def lhandler(link):

    for i in occasions:
        if i["short"] == link:
            print(i["long"])
            return redirect(i['long'], code=302)
    return {'code': "404"}





@app.route("/handler/<link>")
def handler(link):
    # https://goolge.com/l;aksdjfhsadgfkjh34534.3w453k4jh.345jh/kjhdsfjkh345/
    # https://hander.com/45fdgf
    # 17.10.2023

    return render_template("handler.html", link=link)

app.run('127.0.0.1', 3007, debug=True)

