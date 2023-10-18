from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message
from mailchimpanimation import email_to_audience

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

# Create a dictionary to map inputs to policy recommendations
policy_recommendations = {
    'EMPLOYED': [
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.')
    ],
    'SELF-EMPLOYED': [
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.'),
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.')
    ],
    'UNEMPLOYED': [],
    'RETIRED': [],

    'SINGLE': [],
    'MARRIED': [
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.'),
        ('PERSONAL ARTICLES POLICY', 'Protect your valuable possessions with personal articles insurance. It ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.')
    ],
    'ENGAGED': [
        ('PERSONAL ARTICLES POLICY', 'Protect your valuable possessions with personal articles insurance. It ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.')
    ],

    'YesChildren': [
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.'),
        ('HOSPITAL INCOME POLICY', 'Hospital income insurance provides financial support during hospital stays, easing the burden of medical bills and allowing you to focus on your recovery or providing care for an injured family member. Most policies allow you to add your children as a rider. Consider this, especially if you have an active child who plays sports.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.'),
        ('PERSONAL LIABILITY UMBRELLA POLICY', 'A personal liability umbrella policy is crucial because it provides extra protection beyond your standard insurance coverage. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.')
    ],
    'NoChildren': [],

    'YesPets': [
        ('PET MEDICAL INSURANCE', 'Pet medical insurance provides peace of mind, ensuring your furry friend gets the best care without breaking the bank in unexpected emergencies.'),
        ('PERSONAL LIABILITY UMBRELLA POLICY', 'A personal liability umbrella policy is crucial because it provides extra protection beyond your standard insurance coverage. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.')
    ],
    'NoPets': [],

    'YesVehicle': [
        ('AUTO INSURANCE', 'Auto insurance provides financial protection and peace of mind, ensuring you wont bear the burden of costly accidents or damages on your own.')
    ],
    'NoVehicle': [],

    'YesHouse': [
        ('HOMEOWNERS INSURANCE POLICY', 'Homeowners insurance provides financial protection, ensuring that your home and belongings are covered in case of unexpected disasters or accidents, giving you peace of mind.'),
        ('HOSPITAL INCOME POLICY', 'Hospital income insurance provides financial support during hospital stays, easing the burden of medical bills and allowing you to focus on your recovery or providing care for an injured family member. Most policies allow you to add your children as a rider. Consider this, especially if you have an active child who plays sports.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.')
    ],
    'NoHouse': [
        ('RENTERS INSURANCE', 'Renters insurance provides affordable peace of mind, ensuring your belongings are protected in case of unexpected events like fire, theft, or natural disasters. It also covers liability if someone is injured in your residence. For a small monthly fee, you can safeguard your financial future and replace your possessions, making it a smart and responsible choice for any renter.')
    ],

    'YesRentalProperty': [
        ('RENTAL PROPERTY INSURANCE', 'Protect your investment and peace of mind with rental property insurance. It shields you from unexpected disasters, covering damage, liability, and lost rental income. Dont risk financial ruin; safeguard your property and income as soon as possible.'),
        ('PERSONAL LIABILITY UMBRELLA POLICY', 'A personal liability umbrella policy is crucial because it provides extra protection beyond your standard insurance coverage. Imagine a scenario where your child accidentally injures a friend while playing, or your pet causes harm to someone.')
    ],
    'NoRentalProperty': [],

    'YesJewelryFirearms': [
        ('PERSONAL ARTICLES POLICY', 'Protect your valuable possessions with personal articles insurance. It ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.')
    ],
    'NoJewelryFirearms': [],

    'JOB CHANGE': [
        ('401K ROLLOVER', 'Rollover your 401(k) for control and growth. By transferring it to a new account, you unlock the power to manage your retirement savings on your terms. Choose investments that align with your goals, avoid fees, and consolidate multiple accounts for simplicity. Seize the opportunity to secure a brighter financial future.'),
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.')
    ],

    'UPCOMING MARRIAGE': [
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.'),
        ('PERSONAL ARTICLES POLICY', 'Protect your valuable possessions with personal articles insurance. It ensures that your cherished items, from jewelry to electronics, are safeguarded against theft, loss, or damage, providing peace of mind.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.')
    ],

    'BUYING A HOME': [
        ('HOMEOWNERS INSURANCE POLICY', 'Homeowners insurance provides financial protection, ensuring that your home and belongings are covered in case of unexpected disasters or accidents, giving you peace of mind.'),
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.'),
        ('HOSPITAL INCOME POLICY', 'Hospital income insurance provides financial support during hospital stays, easing the burden of medical bills and allowing you to focus on your recovery or providing care for an injured family member. Most policies allow you to add your children as a rider. Consider this, especially if you have an active child who plays sports.')
    ],

    'BUYING A NEW VEHICLE': [
        ('AUTO INSURANCE', 'Auto insurance provides financial protection and peace of mind, ensuring you wont bear the burden of costly accidents or damages on your own.'),
        ('DISABILITY INSURANCE', 'Protect your income and peace of mind with disability insurance. Short-term covers temporary injuries, while long-term safeguards against extended illnesses, ensuring financial stability during tough times.'),
        ('LIFE INSURANCE', 'Life insurance provides financial security for your loved ones. In the event of your passing, it preserves the memory of your legacy by covering expenses, paying off debts, offering peace of mind, and ensuring generational wealth creation.')
    ]
}


# Helper function to filter out repeated recommendations
def unique_recommendations(recommendations, existing_recommendations):
    return [r for r in recommendations if r not in existing_recommendations]

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

        # Update radio button values as per previous response
        children = request.form['children']
        vehicle = request.form['vehicle']
        house = request.form['house']
        rental_property = request.form['rental_property']
        jewelry_firearms = request.form['jewelry_firearms']
        life_events = request.form.getlist('life_events')

        state = request.form['state']

        # Generate policy recommendations based on user inputs
        recommendations = []

        # Occupation-based recommendations
        if occupation in policy_recommendations:
            recommendations.extend(policy_recommendations[occupation])

        # Marital status-based recommendations
        if marital_status in policy_recommendations:
            recommendations.extend(policy_recommendations[marital_status])

        # Children, Pets, Vehicle, House, Rental Property, Jewelry/Firearms recommendations
        recommendations.extend(policy_recommendations[children])
        recommendations.extend(policy_recommendations[pets])
        recommendations.extend(policy_recommendations[vehicle])
        recommendations.extend(policy_recommendations[house])
        recommendations.extend(policy_recommendations[rental_property])
        recommendations.extend(policy_recommendations[jewelry_firearms])

        # Life Events recommendations
        for event in life_events:
            if event in policy_recommendations:
                recommendations.extend(policy_recommendations[event])

        # Remove duplicate recommendations
        unique_recommendations = list(set(recommendations))

        # Prepare email body
        email_body = f"Name: {name}\nAge: {age}\nEmail: {email}\n\nRecommended Policies:\n"
        for policy, description in unique_recommendations:
            email_body += f"• {policy}: {description}\n"

        policy_data = [(policy[0], policy[1]) for policy in unique_recommendations]

        # Send email
        msg = Message("P.I.P.R.E Results | The Agent's Office", sender='expenditure.cob@gmail.com', recipients=[email, 'expenditure.cob@gmail.com'])
        msg.body = email_body
        msg.html = render_template('emailtemplate.html', name=name, age=age, occupation=occupation, recommendations=unique_recommendations, email=email, pets=pets, marital_status=marital_status, children=children, vehicle=vehicle, house=house, rental_property=rental_property, jewelry_firearms=jewelry_firearms, life_events=life_events, state=state,policy_data=policy_data)

        try:
            mail.send(msg)
        except Exception as e:
            print(e)
  
        policy_data = [(policy[0], policy[1]) for policy in unique_recommendations]
        api_key = '922d37aa34782b8362e5e7e51d312e04-us21'
        audience_id = '2fe94b29dd'
        #api_key = '922d37aa34782b8362e5e7e51d312e04-us21'




        email_to_audience(api_key, audience_id, email)


    return render_template('animation.html', policy_data=policy_data, name=name)



if __name__ == '__main__':
    app.run(debug=False)
