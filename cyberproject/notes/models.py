from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    #Flaw no3 (Cryptographic Failures): Password is stored in plaintext
    password = models.CharField(max_length=100)

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()

