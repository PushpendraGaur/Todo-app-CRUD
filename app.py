from flask import Flask,render_template,request
from werkzeug.utils import redirect
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)

myclient = MongoClient('localhost',27017)
mydb = myclient['tododb']
mycoll = mydb['todotable']



@app.route('/',methods = ['GET','POST'])
def home():
    todos = mycoll.find()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        mylist=[{"sno":mycoll.find().count()+1,"todotitle":title,"tododesc":description,"date":datetime.now(),"author":"Admin"}]
        mycoll.insert_many(mylist)
        

        return render_template('index.html',todos=todos)
    
    
    return render_template('index.html',todos=todos )
    

@app.route('/update/<int:sno>' , methods=['GET','POST'])
def update(sno):
    todo = mycoll.find_one({"sno":sno})
    if request.method =='POST':
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        todo = {"todotitle":title,"tododesc":description,"author":author}
        
        mycoll.update_one({"sno":sno},{"$set":todo})
        return redirect('/')
    return render_template('update.html',todo =todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = mycoll.find_one({"sno":sno})
    mycoll.delete_one(todo)
    return redirect('/')


if __name__=="__main__":
    app.run(debug=True)
