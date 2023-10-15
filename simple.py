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
        email = request.form['email']
        phone = request.form['phone']
        date = request.form['date']
        time = request.form['time']
        message = request.form['message']

        msg = Message('New Reservation Request', sender='expenditure.cob@gmail.com', recipients=[email,'expenditure.cob@gmail.com'])  # Replace with recipient email
       
       
        msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nDate: {date}\nTime: {time}\nMessage: {message}"
        msg.html = render_template('email_template.html',  # Set the HTML content with variables
            name=name, email=email, phone=phone, date=date,time=time, message=message)


        try:
            mail.send(msg)
            flash('Order placed, check your email.', 'success')
        except Exception as e:
            flash('Invalid password', 'error')

        return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'ELKJ65496-+6/8*8+9+*-/88+*-/8*sdv78587'  # Replace with your secret key
    app.run(debug=False)
