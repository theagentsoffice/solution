import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError


mailchimp = MailchimpTransactional.Client("md-8XoACn0ktDO71KiOOBdgWg")
message = {
    "from_email": "george@theagentsoffice.com",
    "subject": "Hello world",
    "text": "Welcome to Mailchimp Transactional!",
    "to": [
      {
        "email": "expenditure.cob@gmail.com",
        "type": "to"
      }
    ]
}

def run():
  try:
    response = mailchimp.messages.send({"message":message})
    print('API called successfully: {}'.format(response))
  except ApiClientError as error:
    print('An exception occurred: {}'.format(error.text))

run()
  
  