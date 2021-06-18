
def sendemail(to,subject,message,name):

    import win32com.client as win32
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.To = to
    mail.Subject = subject
    mail.Body = 'Message body'
    mail.HTMLBody = '<h2>Dear ' +name+ ',</h2>' +"<br> We have received your query and we'll be reaching out to you shortly. <br><br> Submitted query: "+ message + " <br><br> Thanks,<br> Tree Geolocation Finder"

    mail.Send()


