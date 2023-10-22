import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError

def send_email_to_mailchimp(html_content, recipient_email):
    # Initialize the Mailchimp Transactional API client with your API key
    mailchimp = MailchimpTransactional.Client("md-8XoACn0ktDO71KiOOBdgWg")

    # Construct the email message
    message = {
        "from_email": "office@theagentsoffice.com",
        "subject": "P.I.P.R.E Results | The Agent's Office",
        "html": html_content,
        "to": [
            {
                "email": recipient_email,
                "type": "to"
            }
        ]
    }

    try:
        response = mailchimp.messages.send({"message": message})
        print('API called successfully: {}'.format(response))
        return True
    except ApiClientError as error:
        print('An exception occurred: {}'.format(error.text))
        return False
