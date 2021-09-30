import smtplib, ssl

# class for running the moss script in parallel
class Email:

    # constructor
    def __init__(self, emails, reportName):
        self.reportName = reportName
        self.emails = emails
    
    # send the emails
    def send(self):
        port = 465  # For SSL
        smtp_server = "smtp.gmail.com"
        sender_email = "cscmailaddress@gmail.com"  # Enter your address
        #receiver_email = self.emails  # Enter receiver address
        password = 'cscmail123'
        message = f"Subject: {self.reportName} Job Complete"
        try:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                for receiver_email in self.emails:
                    server.sendmail(sender_email, receiver_email, message)
            return True
        except:
            print("Email failed to send")
            return False

