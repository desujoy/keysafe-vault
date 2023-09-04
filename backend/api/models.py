from django.db import models

# Create your models here.

class PassDB(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SecNotesDB(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    notes = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class CardsDB(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=100)
    card_type = models.CharField(max_length=100)
    card_cvv = models.CharField(max_length=100)
    card_exp = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class FileDB(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')
    encryptedFileName = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name