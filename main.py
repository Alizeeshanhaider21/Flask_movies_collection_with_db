from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviesinfo.db'
app.app_context().push()
# Creating an SQLAlchemy instance
db = SQLAlchemy(app)

# CREATE TABLE
class moviesData(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String(20), unique=False, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(100), unique=False, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    reviews = db.Column(db.String(20), unique=False, nullable=False)
    img_url = db.Column(db.String(50), unique=False, nullable=False)

@app.route("/")
def home():
    data = moviesData.query.all()
    return render_template("index.html",movies=data)
@app.route("/add", methods=["POST",'GET'])
def add():
    if request.method=='POST':
        name = request.form.get("title")
        year = request.form.get("year")
        description = request.form.get("description")
        rating = request.form.get("rating")
        ranking = request.form.get("ranking")
        reviews = request.form.get("reviews")
        imageurl = request.form.get("imageurl")
        
        # print(name,year,description,rating,ranking,reviews,imageurl)
        
        if name != '' and year != '' and description != '':
            p = moviesData(movie_name=name, year=year, description=description,rating=rating,ranking=ranking,reviews=reviews,img_url=imageurl)
          
            db.session.add(p)
            db.session.commit()
            return redirect('/')
    
    return render_template("add.html")
@app.route("/edit/<int:id>", methods=["POST","GET"])
def edit(id):
    data = moviesData.query.get(id)
    # print(data.img_url)
    if request.method=='POST':
           
            
        if request.form.get("title") != '' and request.form.get("year") != '' and request.form.get("description") != '':
            data.movie_name=request.form.get("title")
            data.year = request.form.get("year") 
            data.description = request.form.get("description")
            data.rating = request.form.get("rating")
            data.ranking = request.form.get("ranking")
            data.reviews = request.form.get("reviews")
            data.img_url = request.form.get("imageurl")
            print(data.movie_name,data.year,data.description ,data.rating,data.ranking,data.reviews,data.img_url)
            db.session.commit()
            return redirect('/')
        else:
            print('Data not ok')
    return render_template("edit.html",movie=data)
@app.route('/delete/<int:id>')
def erase(id):
    # Deletes the data on the basis of unique id and 
    # redirects to home page
    data = moviesData.query.get(id)
    db.session.delete(data)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
   