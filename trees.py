from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField , DateField,BooleanField,SelectField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired
from interact_db import insert_new_request ,select_all_tasks , update_request, delete_all_task
import json
from flask import jsonify
from Tree_Utils import sendemail

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'

# Flask-Bootstrap requires this line
Bootstrap(app)

# with Flask-WTF, each web form is represented by a class
# "NameForm" can change; "(FlaskForm)" cannot
# see the route for "/" and "index.html" to see how this is used
class NameForm(FlaskForm):
    personname = StringField('Who planted this Tree ?', validators=[DataRequired()])
    species = StringField('Species:', validators=[DataRequired()])
    lat =   FloatField('Latitude:', validators=[DataRequired()], id='lat')
    lng = FloatField('Longitude', validators=[DataRequired()], id='lng')
    health= SelectField('Tree health:',choices=[('mature', 'Mature'), ('semi-mature', 'Semi-Mature '),('early','Early')], validators=[DataRequired()])
    height= StringField('Tree height:')
    date = DateField('Planted Date:', validators=[DataRequired()],id='date')
    ack = BooleanField('I acknowledge that the above details entered are best to my knowledge.', validators=[DataRequired()])

    submit = SubmitField('Submit')


class ContactForm(FlaskForm):
    Name = StringField('Your Name:', validators=[DataRequired()])
    Email = StringField('Your Email:', validators=[DataRequired()])
    Subject =   StringField('Subject:', validators=[DataRequired()])
    Message = StringField('Message',widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('Submit')


# all Flask routes below

@app.route('/add', methods=['GET', 'POST'])
def index():
    # names = get_names(ACTORS)
    # you must tell the variable 'form' what you named the class, above
    # 'form' is the variable name used in this template: index.html
    form = NameForm()
    message = ""
    if form.validate_on_submit():
        species = form.species.data
        lat= form.lat.data
        lng = form.lng.data
        health= form.health.data
        height= form.height.data
        date = form.date.data
        personname = form.personname.data
        # print(form.location.data)
        new_entry = (species,lat,lng,health,height,date,personname);
        trreeid = insert_new_request(new_entry)
        message = "Congrats, A Tree has been added in our database with id :  "+ str(trreeid) + "   \U0001F64B"
        # return redirect( url_for('home'))
        return render_template('index.html', form=form, message=message)
    return render_template('index.html', form=form, message=message)

@app.route('/', methods=['GET', 'POST'])
def home():

    form = ContactForm()

    if form.validate_on_submit():
        print ("here in submit")
        Name = form.Name.data
        Email = form.Email.data
        Subject =   form.Subject.data
        Message = form.Message.data
        sendemail(Email,Subject,Message,Name)
        

    all_tree_data = select_all_tasks()
    
    newlist = []
    for i in all_tree_data:
        newlist.append([i[1],i[2],i[3],i[4],i[5],i[6],i[7]])
    print(newlist)
    return render_template('multiplemarker.html',form=form,location = json.dumps(newlist))


@app.route('/flush')
def flush():
    delete_all_task()
    return redirect( url_for('home'))
# 2 routes to handle errors - they have templates too

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# keep this as is
if __name__ == '__main__':
    app.run(debug=True)
