from django.db import models

# Create your models here.

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    last_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Pass(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SecNotes(models.Model):
    id = models.AutoField(primary_key=True)
    notename = models.CharField(max_length=100)
    content = models.CharField(max_length=100)
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Cards(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    card_number = models.CharField(max_length=100)
    card_type = models.CharField(max_length=100)
    card_cvv = models.CharField(max_length=100)
    card_exp = models.CharField(max_length=100)
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Files(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='files/')
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name