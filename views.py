from flask import Flask, render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///Example.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO']=True

#@app.route('/')
#def hello():
#    return "Hello Test"

db = SQLAlchemy(app)

class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    category = db.Column(db.Text)
    price = db.Column(db.Integer)


@app.before_first_request
def init():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    datas = Movie.query.all()
    return render_template('search_result.html', lists = datas)


@app.route('/result', methods=['POST'])
def insert():
    name_txt = request.form['name']
    category_txt = request.form['category']
    price_txt = request.form['price']
    movie = Movie(name = name_txt, category = category_txt, price = price_txt)
    db.session.add(movie)
    db.session.commit()
    return redirect('/')


@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

