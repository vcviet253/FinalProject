import random
import string

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from validate_email import validate_email

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from app.models import BallotRegister, Ballot


def encrypt(plaintext, password):
    f = Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'staticsalt', iterations=1000, backend=default_backend()).derive(password.encode())))
    return f.encrypt(plaintext.encode()).decode()

def decrypt(ciphertext, password):
    f = Fernet(base64.urlsafe_b64encode(PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=b'staticsalt', iterations=1000, backend=default_backend()).derive(password.encode())))
    return f.decrypt(ciphertext.encode()).decode()

# Convert csv file to list of email
def handle_uploaded_files(file):
    results = []
    for row in file:
        line = str(row, 'utf-8')
        results.append(line.strip())
    return results

# Get a list of voter and register them to ballot in database, send email to each user
def register_email_to_ballot(email_list, ballot_id):
    ballot = Ballot.objects.get(pk=ballot_id)
    for email in email_list:
        print(email)
        user = User.objects.filter(email=email).first()
        # if User.objects.filter(email=email).exists():
        if user is not None:  # user existed
            # If user is already invited to vote
            if BallotRegister.objects.filter(user=user, ballot=ballot).exists():
                pass

            # register user to ballot, invite to vote
            else:
                ballot_register = BallotRegister.objects.create(user=user, ballot=ballot, voted=False)
                sendEmail = EmailMessage('You are invited to vote',
                                         'You are invited to vote in ballot' + ballot.ballot_name, to=[email])
                sendEmail.send()
        elif user is None:  # no user with email entered
            # Create username
            username = email.split("@", 1)[0]
            extra = 0
            while User.objects.filter(username=username).exists():
                username = username + str(extra)
                extra += 1

            # Generate password
            stringLength = 8
            lettersAndDigits = string.ascii_letters + string.digits
            password = ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))
            new_user = User.objects.create_user(username=username, email=email, password=password)

            # Generate new account then send username, password to user email
            # Send email step
            message = 'You are invited to vote in ballot' + ballot.ballot_name +'.Your account credentials. Username: ' + username + ' . Password: ' + password + '. Please save these information.'
            sendEmail = EmailMessage('You are invited to vote', message, to=[email])
            sendEmail.send()

            # Register this user to ballot
            ballot_register = BallotRegister.objects.create(user=new_user, ballot=ballot, voted=False)

