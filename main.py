from flask import Flask, flash, render_template,redirect, request, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from wtforms import StringField, BooleanField, PasswordField, RadioField, DateField, FloatField
from wtforms.validators import URL, Length, InputRequired
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import os
from graph import Plot

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

Bootstrap(app)
db = SQLAlchemy(app)
db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

class Users(UserMixin, db.Model):
    '''
    Creates a Database to store an User's username and Password
    '''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

class SignUpForm(FlaskForm):
    '''
    The form to Sign-Up for the user in Pixela 
    '''
    username = StringField(label='Username(No charecters / spaces - all lowercase)', validators=[InputRequired()])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=4)])
    age = BooleanField(label='Yes, I accept the Terms and Conditions & I\'m above age 18.', validators=[InputRequired()])

class LoginForm(FlaskForm):
    '''
    The form to Login to a session in Pixela
    '''
    username = StringField(label='Username', validators=[InputRequired()])
    password = PasswordField(label='Password', validators=[InputRequired(), Length(min=4)])
    remember = BooleanField(label='Remember me')

class GraphForm(FlaskForm):
    '''
    The form used to Create a Graph in Pixela
    '''
    graph_id = StringField(label='Graph ID* (No spaces / charecters)', validators=[InputRequired(), Length(min=1, max=16)])
    graph_name = StringField(label='Name of the Graph*', validators=[InputRequired()])
    graph_unit = StringField(label='Unit to be measured*', validators=[InputRequired()])
    graph_type = RadioField(label='Value to be Measured*', choices=['int', 'float'], validators=[InputRequired()])
    graph_color = RadioField(label='Color of the Graph*', 
    choices=[('shibafu', 'Green'), ('momiji','Red'), ('sora','Blue'), ('ichou','Yellow'), ('ajisai','Purple'), ('kuro','Black')])

class ViewGraph(FlaskForm):
    """ 
    Form used to View the Created graph
    """
    v_id = StringField(label='Graph ID', validators=[InputRequired(), Length(min=1, max=16)])

class AddPixel(FlaskForm):
    """
    Form used to add a pixel to the graph
    """
    date = DateField(label='Date - to add/update the pixel', validators=[InputRequired()])
    quantity = FloatField(label='Quantity', validators=[InputRequired()],)

class DelPixel(FlaskForm):
    """
    Form used to delete a pixel on the graph
    """
    date = DateField(label='Date - to delete the pixel', validators=[InputRequired()])

CREATE_USER = "https://pixe.la/v1/users"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/signup/", methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = Users(username=form.username.data.lower(), password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Welcome, succesfully registered! Please, Login below.")
        return redirect (url_for('login'))
    return render_template('signup.html', form=form)

@app.route("/login/", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data.lower()).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                
                create_user = {
                    "token": current_user.password,
                    "username": current_user.username.lower(),
                    "agreeTermsOfService": "yes",
                    "notMinor": "yes"
                    }    
                response = requests.post(CREATE_USER, json=create_user)
                msg = response.json()
                if msg.get('isSuccess'):
                    return redirect(url_for('profile'))
                else:
                    flash(f"{msg.get('message')}")
                    return render_template('login.html', form=form)
            else:
                flash("Invalid password, please try again!")
                return render_template('login.html', form=form)
        else:
            flash("Invalid username, please sign up!")
            return render_template('login.html', form=form)
    return render_template('login.html', form=form)

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return render_template('index.html')

@app.route("/profile/", methods=['GET', 'POST'])
@login_required
def profile():
    form1 = GraphForm()
    form2 = ViewGraph()
    name = current_user.username
    token = current_user.password
    headers = {"X-USER-TOKEN": token,}
    
    # Create Graph
    if "form1" in request.form and form1.validate_on_submit():
        token = current_user.password
        params = {
            'id' : form1.graph_id.data.lower(),
            'name' : form1.graph_name.data,
            'unit' : form1.graph_unit.data,
            'type' : form1.graph_type.data,
            'color' : form1.graph_color.data,
        }
        
        response = requests.post(url=f'https://pixe.la/v1/users/{name}/graphs', json=params, headers=headers)
        msg = response.json()
        if msg.get('isSuccess'):
            flash("Graph has been created sucessfully. Use 'View Graph' to view it!")
        else:
            flash(f"{msg.get('message')}")
        return render_template('profile.html', form1=form1, form2=form2, name=name)

    # View Graph
    if "form2" in request.form and form2.validate_on_submit():
        return redirect(url_for('graph', graph_id=form2.v_id.data)) 
    
    return render_template('profile.html', form1=form1, form2=form2, name=name)

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/graph/<graph_id>", methods=['GET', 'POST'])
@login_required
def graph(graph_id):
    form3 = AddPixel()     
    form8 = DelPixel()
    name = current_user.username
    token = current_user.password
    image_params = {'appearance':'dark'}
    headers = {"X-USER-TOKEN": token,}
    
    # Get the svg image
    try:
        picture = requests.get(url=f'https://pixe.la/v1/users/{name}/graphs/{graph_id}', params=image_params)
        image = picture.text
        picture.raise_for_status()
    except requests.exceptions.HTTPError:
        flash("The Graph ID doesn't exist")
        return redirect(url_for('profile'))

    # Get the name of the graph
    details = requests.get(url=f'https://pixe.la/v1/users/{name}/graphs/', headers=headers)
    image_details = details.json()
    for item in image_details.get('graphs'):
        if item.get('id') == graph_id:
            plot = Plot(idx=item.get('id'), name=item.get('name'), unit=item.get('unit'), 
            typex=item.get('type'))

    # Add Pixel
    if "form3" in request.form and form3.validate_on_submit():
        
        if plot.type == float:
            pixel_param = {
                "date": (form3.date.data).strftime('%Y%m%d'),
                "quantity": str(form3.quantity.data),
            }
        else:
            pixel_param = {
                "date": (form3.date.data).strftime('%Y%m%d'),
                "quantity": str(int(form3.quantity.data)),
            }

        requests.post(url=f'https://pixe.la/v1/users/{name}/graphs/{graph_id}', json=pixel_param, headers=headers)
        flash("Pixel Added succesfully! Please refresh if you don't yet see it on the plot.")
        
        return render_template('graph.html', image=image, form3=form3, plot=plot, form8=form8)

    # Update Pixel
    if "form4" in request.form and form3.validate_on_submit():
        
        if plot.type == float:        
            update_pixel ={
                "quantity": str(form3.quantity.data),
            }
        else:
            update_pixel ={
                "quantity": str(int(form3.quantity.data)),
            }

        f = requests.put(url=f'https://pixe.la/v1/users/{name}/graphs/{graph_id}/{(form3.date.data).strftime("%Y%m%d")}', json=update_pixel, headers=headers)
        flash("Pixel Updated succesfully! Please refresh if you don't yet see it on the plot.")
        return render_template('graph.html', image=image, form3=form3, plot=plot, form8=form8)

    # Delete Pixel
    if "form8" in request.form and form8.validate_on_submit():
        g =requests.delete(url=f'https://pixe.la/v1/users/{name}/graphs/{graph_id}/{(form3.date.data).strftime("%Y%m%d")}', headers=headers)
        flash("Pixel Updated succesfully! Please refresh if you don't yet see it on the plot.")
        return render_template('graph.html', image=image, form3=form3, plot=plot, form8=form8)

    return render_template('graph.html', image=image, form3=form3, plot=plot, form8=form8)

@app.route('/delete_profile/<name>')
@login_required
def delete_profile(name):
    headers = {"X-USER-TOKEN": current_user.password,}
    requests.delete(url=f'https://pixe.la/v1/users/{current_user.username}', headers=headers)
    delete_user = Users.query.filter_by(username=name).first()
    db.session.delete(delete_user)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/delete_graph/<graph_id>')
@login_required
def delete_graph(graph_id):
    headers = {"X-USER-TOKEN": current_user.password,}
    requests.delete(url=f'https://pixe.la/v1/users/{current_user.username}/graphs/{graph_id}', headers=headers)
    return redirect(url_for('profile'))

@app.errorhandler(401)
def custom_401(error):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True)
