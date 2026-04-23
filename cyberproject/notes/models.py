from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    # FLAW 3 (A02 Cryptographic Failures): Password stored in plaintext
    # FIX: Use Django's built-in make_password/check_password instead
    # from django.contrib.auth.hashers import make_password
    # password = models.CharField(max_length=255)  # store make_password(raw_password)
    password = models.CharField(max_length=100)

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

