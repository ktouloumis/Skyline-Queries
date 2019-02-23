from flask import Flask, render_template, request, redirect, session
from flask_mail import Mail, Message
import answers.preprocserver as prec
import time
import fcntl
import json
import ast

#preprocess server
prec.preprocess()

#initialize flask app



app = Flask(__name__)



app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'kostasdelft8@gmail.com'
app.config['MAIL_PASSWORD'] = 'passwordforthesis261992'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False



app.secret_key = "something-from-os.urandom(24)"

#session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config["SESSION_PERMANENT"] = False

mail = Mail(app)

@app.route('/')
def home():
    #clear session
    session.clear()
    return render_template('homepage.html')

@app.route('/userinfo')
def userinfo():
    return render_template('userinfo.html')

@app.route('/userdata', methods = ['POST'])
def userdata():

    #assign id to user
    data_folder = prec.os.path.join("mysite", "answers")
    filename = prec.os.path.join(data_folder, "systemlog.dat")

    dict={}
    with open(filename, "r+", encoding="utf-8") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        x = [l.strip() for l in file]
        for line in x :
            print(line)
            whip = ast.literal_eval(line)
            userid = int(whip['totalusers'])
            session['userid'] = userid+1
            dict['totalusers'] = str(userid+1)
            dict['totaltries'] = whip['totaltries']
            dict['totaltime'] = whip['totaltime']

        file.seek(0)
        file.truncate(0)
        file.write(json.dumps(dict))

        fcntl.flock(file, fcntl.LOCK_UN)

    #initialize number of attempts and group
    session['tries'] = '0'
    session['group'] = prec.algs[int(session['userid'])%7]

    #personal details from form
    personalinfo = {}
    if request.method == 'POST':
        age = request.form['age']
        gender = request.form['gender']

        education = request.form['education']
        prior = request.form['prior']

        personalinfo['userid'] = session['userid']
        personalinfo['age'] = age
        personalinfo['gender'] = gender
        personalinfo['education'] = education
        personalinfo['prior'] = prior


    #save personal details to datafile
    data_folder = prec.os.path.join("mysite", "answers")
    filename = prec.os.path.join(data_folder, "personalinfo.dat")

    with open(filename, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(personalinfo))
        f.write("\n")
        fcntl.flock(f, fcntl.LOCK_UN)

    return redirect("/dataset")

@app.route('/dataset')
def dataset():
    return render_template('dataset.html')

@app.route('/searchdata', methods = ['POST', 'GET'])
def searchdata():
    resdf = prec.searchdf(request.form, prec.df)

    #query results for html
    items = prec.load_previtems(resdf)
    stable = prec.PrevTable(items)

    return render_template('dataset.html', prevtable = stable, numofres=len(resdf))

@app.route('/begin')
def begin():
    return render_template('begin.html')

@app.route('/task')
def task():
    #initialize task starting time
    session['start_time'] = time.time()

    #initialize flag pressed "Show" button to False
    session['showed'] = False

    return render_template('task.html', desc=prec.task, numofres=0, redsize = 0)

@app.route('/searchreduced', methods = ['POST', 'GET'])
def searchreduced():
    #get current time
    session['current_time'] = time.time()

    #increase the number of searching attempts
    session['tries'] = json.dumps(int(session['tries'])+1)

    #get dataframe to search
    sdf = prec.getdf(session['group'])

    #search for query results on entire dataset
    resdf = prec.searchdf(request.form, prec.df)

    #search reduced set
    reduceddf = prec.searchdf(request.form, sdf)

    #load items for html
    dataitems = prec.load_items(resdf)
    reduceditems = prec.load_previtems(reduceddf)

    datatable = prec.ItemTable(dataitems)
    redtable = prec.PrevTable(reduceditems)

    #dictionary to save details for attempt
    dicttry = {}
    dicttry['userid'] = session['userid']
    dicttry['nresults'] = len(resdf)
    dicttry['time'] = str(round(session['current_time']-session['start_time'], 2))
    dicttry['filters'] = dict(request.form)
    dicttry['showed'] = session['showed']
    dicttry['redlen'] = len(reduceddf)
    dicttry['try'] = session['tries']

    session['filteredsize'] = len(resdf)
    #save filters in session variable
    session['filters'] = request.form

    #write dictionary to data file
    data_folder = prec.os.path.join("mysite", "answers")
    filename = prec.os.path.join(data_folder, "attempts.dat")
    with open(filename, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(dicttry))
        f.write("\n")
        fcntl.flock(f, fcntl.LOCK_UN)

    if session['showed'] == False:
        return render_template( 'task.html', desc = prec.task, redtable=redtable, numofres=len(resdf), redsize = len(reduceddf))
    else:
        return render_template( 'task.html', desc = prec.task, redtable = redtable, datatable = datatable, numofres=len(resdf), redsize = len(reduceddf))

@app.route('/showdata')
def showdata():

    #get filters
    if 'filters' not in session:
        #begin task again
        #session['start_time'] = time.time()

        #initialize flag pressed "Show" button to False
        session['showed'] = False

        return render_template('task.html', desc=prec.task, numofres=0, redsize=0)

    filters = session['filters']

    #get dataframe to search
    sdf = prec.getdf(session['group'])

    #query results on entire dataset
    resdf = prec.searchdf(filters, prec.df)

    #query results on reduced skyline set
    reduceddf = prec.searchdf(filters, sdf)

    #load items for html
    dataitems = prec.load_items(resdf)
    reduceditems = prec.load_previtems(reduceddf)

    datatable = prec.ItemTable(dataitems)
    redtable = prec.PrevTable(reduceditems)

    if session["showed"]==False:
        #set the flag showed to True
        session['showed'] = True

        #dictionary to save details of pressing the show button
        dictshow = {}
        dictshow['userid'] = session['userid']
        session['showtime'] = time.time()
        dictshow['time'] = round(session['showtime']-session['start_time'], 2)
        dictshow['attempt'] = session['tries']
        dictshow['datasize'] = len(resdf)

        #save dictionary to datafile
        data_folder = prec.os.path.join("mysite", "answers")
        filename = prec.os.path.join(data_folder, "showed.dat")
        with open(filename, 'a') as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(json.dumps(dictshow))
            f.write("\n")
            fcntl.flock(f, fcntl.LOCK_UN)

        return render_template('task.html', desc=prec.task, redtable=redtable, datatable=datatable,
                               numofres=len(resdf), redsize = len(reduceddf))
    else:
        return render_template('task.html', desc=prec.task, redtable=redtable, datatable=datatable,
                               numofres=len(resdf), redsize = len(reduceddf))


@app.route('/single_item/<int:id>')
def single_item(id):

    #compute user's total time on task
    session['endtime'] = time.time()
    session['totaltime'] = round(session['endtime']-session['start_time'],2)

    #display user's purchase item
    ch = prec.df.iloc[id]
    price = ch['price']
    body = ch['vehicleType']
    gear = ch['gearbox']
    hp = ch['powerPS']
    kil = ch['kilometer']
    fuel = ch['fuelType']
    damage = ch['notRepairedDamage']

    #append choice to dictionary
    fchoice = {}
    fchoice['userid'] = session['userid']
    fchoice['id'] = str(id)
    fchoice['price'] = str(price)
    fchoice['vehicleType'] = str(body)
    fchoice['gearbox'] = str(gear)
    fchoice['powerPS'] = str(hp)
    fchoice['kilometer'] = str(kil)
    fchoice['fuelType'] = str(fuel)
    fchoice['notRepairedDamage'] = str(damage)

    #save choice to dataframe
    data_folder = prec.os.path.join("mysite", "answers")
    filename = prec.os.path.join(data_folder, "choice.dat")

    with open(filename, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(fchoice))
        f.write("\n")
        fcntl.flock(f, fcntl.LOCK_UN)

    return render_template('decision.html', fueltype=fuel, bodystyle=body, gearbox=gear, damage=damage, mileage=kil, horsepower=hp, price=price )

@app.route('/questions')
def questions():
    return render_template('questionnaire.html')

@app.route('/questionnaire', methods = ['POST'])
def submitquestions():
    #dictionary for answers on Nasa TLX
    answers = {}
    answers['userid'] = session['userid']
    answers['mental'] = request.form['mental']
    answers['time'] = request.form['time']
    answers['frust'] = request.form['frust']
    answers['sat'] = request.form['sat']
    answers['help'] = request.form['help']
    answers['effort'] = request.form['effort']
    answers['comments'] = request.form['comments']

    #save answers on datafile
    data_folder = prec.os.path.join("mysite", "answers")
    filename = prec.os.path.join(data_folder, "NasaTlx.dat")

    #write answers on datafile
    with open(filename, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(answers))
        f.write("\n")
        fcntl.flock(f, fcntl.LOCK_UN)

    #save user details on datafile
    dictlog = {}
    dictlog['userid'] = session['userid']
    dictlog['totaltime'] = session['totaltime']
    dictlog['tries'] = session['tries']
    dictlog['group'] = session['group']
    dictlog['filteredsize'] = session['filteredsize']

    data_folder = prec.os.path.join("mysite", "answers")
    filename = prec.os.path.join(data_folder, "logusers.dat")

    with open(filename, 'a') as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(dictlog))
        f.write("\n")
        fcntl.flock(f, fcntl.LOCK_UN)

    return redirect('/goodbye')



@app.route('/goodbye', methods=['POST', 'GET'])
def goodbye():
    data_folder = prec.os.path.join("mysite", "answers")
    filename = prec.os.path.join(data_folder, "systemlog.dat")

    dicttotal={}
    with open(filename, "r+", encoding="utf-8") as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        x = [l.strip() for l in file]
        for line in x :
            print(line)
            whip = ast.literal_eval(line)

            totaltries = int(whip['totaltries'])
            totaltime = float(whip['totaltime'])

            dicttotal['totalusers'] = whip['totalusers']

            totaltries = totaltries+int(session['tries'])
            totaltime = round(totaltime+float(session['totaltime']),2)

            dicttotal['totaltries'] = str(totaltries)
            dicttotal['totaltime'] = str(totaltime)
            file.seek(0)
            file.truncate(0)
            file.write(json.dumps(dicttotal))

    return render_template('goodbye.html')

@app.route('/contact', methods=['POST'])
def contact():
    #return "In contact"
    address = request.form['address']
    text = request.form['comments']

    msg = Message('Reduce Sk', sender = 'kostasdelft8@gmail.com', recipients = ['kostasdelft8@gmail.com'])

    msg.body = address+"\n"+text
    mail.send(msg)
    return render_template('goodbye.html')

if __name__ == "__main__":
    #preprocserver.preprocess()

    #app.secret_key = '1234'

    #app.debug = True

    app.run()