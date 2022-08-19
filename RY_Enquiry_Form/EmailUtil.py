from django.core.mail import send_mail
from django.template import loader
import smtplib
from .DAO import DAO
#from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
import base64
from django.core.mail import EmailMultiAlternatives


class EMAIL_UTIL:

    server_ssl = None

    def __init__(self):

        global server_ssl

        uname = 'guru2611199@gmail.com'
        pwd = 'evmfpjbqyoihhhbl'
        server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server_ssl.ehlo()
        server_ssl.login(uname, pwd)
        print("Email settings loaded , all set to send email")

    # send to single email id

    def send_single(self, toSingleEmail, subjectText, emailBodyText):
        global server_ssl
        fmail = "guru2611199@gmail.com"
        msg = 'Subject: {}\n\n{}'.format(subjectText, emailBodyText)

        if (server_ssl != None):
            server_ssl.sendmail(fmail, toSingleEmail, msg)
            server_ssl.close()
            return True

        return False

    # send to the groups

    def send_group(self, GroupName, subjectText, emailBodyText):
        global server_ssl

        vDAO = DAO("dao")

        # vGroupEmailList will return a list of email id of that group which should be
        # looped and call sendmail method

        subject = subjectText
        email_list = []
        
        message = ''
        vGroupEmailList = vDAO.GetGroupEmailList(GroupName)
        for vQueryData in vGroupEmailList:
                print("sending email to ", vQueryData[0].UserName)
                email_list.append(vQueryData[0].UserName)
        mail = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, email_list)
        mail.attach_alternative(emailBodyText, 'text/html')
        mail.send()
            # self.send_single(vQueryData[0].UserName, subjectText, emailBodyText)
        return True

    def send_po(self, subject, message, files):
        mail = EmailMultiAlternatives(subject, message, settings.EMAIL_HOST_USER, [
                            'dhineshofficial99@gmail.com'])
        for f in files:
            mail.attach(f.name, f.read(), f.content_type)
        mail.send()
        return True

    def send_activation_code(self, email):
        sample_string_bytes = email.encode("ascii")
        base64_bytes = base64.b64encode(sample_string_bytes)
        base64_string = base64_bytes.decode("ascii")
        subject = 'activation mail'
        email_list = []
        email_list.append(email)
        message = 'Hi,'+'\nPlease click on the link to confirm your registration, ' + \
            '\nhttp://103.86.176.153/activate/'+base64_string
        mail = EmailMultiAlternatives(
            subject, message, settings.EMAIL_HOST_USER, email_list)
        mail.send()
        return True
