# email_sender
Django 3.2.9 is a service for sending emails with an html template. Simple and fast. No frills

<h3>INSTALL</h3>

1. Download the repository
2. Rename .end.dist to .env and fill in with your data. I am from Russia, so I work with the help of mail from the great Yandex. If you use another mail, then Google the settings for your mail service. After all, this is Django, everything is on the Internet. I think you can do it without my help
3. Go to http://domen_or_ip/index then fill out the form and after sending the form, the mailing list will begin

<h3>IMPORTANT</h3>
It is important that you fill out the form correctly. As it is written in the description, this is a simple tool and it is not adaptive. Review the information about each of the fields before use.

<h2>Form fields (index/)</h2>

1. Template. Expects a file from you .html with css embedded in it. html mailing requires the introduction of css into the template itself, if your css is a separate file, nothing will work.
2. Emails. Expects a text file from you with a list of target addresses for mailing. important!!!! Each address must be from a new line. Your text file should contain a column with emails, where each one starts from a new line
3. Subject. Everything is simple. Enter a subject for your email.
4. Enter an email to receive a newsletter report. If everything is OK, then they will tell you. If there are problems, they will tell you about it.

<h3>The author does not provide for data storage. Downloaded templates and address lists are deleted in mailer.mixins.dispatcher. Other data is not stored at all and is used only during one specific mailing.</h3>
