from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'klajdokfjwoeijoigjodjf5498wfej38eruf9'

# Configure Flask-Mail for sending emails
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "expenditure.cob@gmail.com"

app.config['MAIL_PASSWORD'] = "hrhdkdiwwzungmjz"

app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
         name = request.form['name']
         age = request.form['age']
         occupation = request.form['occupation']
         email = request.form['email']
         pets = request.form['pets']
         marital_status = request.form['marital_status']
         children = request.form['children']
         vehicle = request.form['vehicle']
         house = request.form['house']
         rental_property = request.form['rental_property']
         jewelry_firearms = request.form['jewelry_firearms']
         life_events = request.form.getlist('life_events')


         msg = Message("P.I.P.R.E Results | The Agent's Office", sender='expenditure.cob@gmail.com', recipients=[email,'expenditure.cob@gmail.com'])  # Replace with recipient email
       
       
        # msg.body = f"Email: {email}\nMessage: {occupation}"
        # msg.html = render_template('emailtemplate.html',  # Set the HTML content with variables
        #      email=email,  occupation=occupation)
         message = f"Name: {name}\nAge: {age}\nOccupation: {occupation}\nEmail: {email}\nMarital Status: {marital_status}\nChildren: {children}\nPets: {pets}\nVehicle: {vehicle}\nHouse: {house}\nRental Property: {rental_property}\nJewelry/Firearms: {jewelry_firearms}\nLife Events: {', '.join(life_events)}"

         msg.body = message

        # Render the email template and pass the variables
         msg.html = render_template('emailtemplate.html', name=name,age=age, occupation=occupation, email=email,  pets=pets,marital_status=marital_status, children=children, vehicle=vehicle, house=house, rental_property=rental_property, jewelry_firearms=jewelry_firearms, life_events=life_events)



         try:
             mail.send(msg)
            # flash('Order placed, check your email.', 'success')
         except Exception as e:
            # flash('Invalid password', 'error')
            print(e)

         return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'ELKJ65496-+6/8*8+9+*-/88+*-/8*sdv78587'  # Replace with your secret key
    app.run(debug=False)
