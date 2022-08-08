from django.core.mail import send_mail
from django.template import loader
import smtplib
from .DAO import DAO


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
        fmail = "guru2611199@gmail.com"
        msg = 'Subject: {}\n\n{}'.format(subjectText, emailBodyText)
        vGroupEmailList = vDAO.GetGroupEmailList(GroupName)
        print("########################", vGroupEmailList)
        if (server_ssl != None):
            for vQueryData in vGroupEmailList:
                print("sending email to ", vQueryData[0].UserName)    
            
                server_ssl.sendmail(fmail, vQueryData[0].UserName, msg)
                
            #server_ssl.close()
            return True
            self.send_single(vQueryData[0].UserName, subjectText, emailBodyText)
        return True
