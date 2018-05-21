import os
import smtplib

from getpass import getpass
from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


"""
You'll probably have to go to your Google account and enable less secure apps.
WARNING: DO NOT fill these variables and put them in a public repo.
"""
MY_EMAIL = ''
MY_PASSWORD = ''

TEMPLATES_DIR = './templates/'


def get_contacts(filename):
    """
    Return three lists names, emails, links containing names, email addresses
    and links read from a file specified by filename.
    TODO(gus): make this more flexible.
    """
    
    names = []
    emails = []
    links = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
            links.append(a_contact.split()[2])
    return names, emails, links


def read_template(filename):
    """
    Returns a Template object comprising the contents of the 
    file specified by filename.
    """
    
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def get_credentials():
    if MY_EMAIL and MY_PASSWORD:
        return MY_EMAIL, MY_PASSWORD

    email = input('What\'s your email? ')
    password = getpass(prompt='What\'s your password? ')
    return email, password


def get_message_info():
    templates = os.listdir(TEMPLATES_DIR)
    for i, f in enumerate(templates): 
        print(str(i) + '. ' +  f)

    template_index = int(input('Select your template: '))
    template = read_template(TEMPLATES_DIR +  templates[template_index])

    # TODO(gus): put this in a better place.
    titles = ['\"Nosso Feedback na sua Missão #3 🏔\"']
    for i, f in enumerate(titles): 
        print(str(i) + '. ' +  f)
    print(str(len(titles)) + '. For your custom subject')

    title_index = int(input('Select your subject: '))
    if title_index < len(titles):
        title = titles[title_index]
    else:
        title = input('Type your custom subject: ')

    return template, title


def main():
    sender_email, sender_password = get_credentials() # get email credentials
    names, emails, links = get_contacts('mycontacts.txt') # read contacts

    message_template, message_subject = get_message_info()

    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(sender_email, sender_password)

    # For each contact, send the email:
    for name, email, link in zip(names, emails, links):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name, PERSON_LINK=link)

        # Prints out the message body for our sake
        print(message)

        # # setup the parameters of the message
        # msg['From'] = sender_email
        # msg['To'] = email
        # msg['Subject'] = message_subject
        
        # # add in the message body
        # msg.attach(MIMEText(message, 'html'))
        
        # # send the message via the server set up earlier.
        # s.send_message(msg)
        del msg
        
    # Terminate the SMTP session and close the connection
    s.quit()


if __name__ == '__main__':
    main()