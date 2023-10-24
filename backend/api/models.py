from django.db import models

# Create your models here.

class Users(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    token = models.TextField(unique=True)
    verification_string = models.TextField(unique=True)
    last_login = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Pass(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.TextField()
    password = models.TextField()
    username = models.TextField()
    website = models.TextField()
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class SecNotes(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    notename = models.TextField()
    content = models.TextField()
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Cards(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.TextField()
    card_number = models.TextField()
    card_type = models.TextField()
    card_cvv = models.TextField()
    card_exp = models.TextField()
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Files(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.TextField()
    file = models.FileField(upload_to='files/')
    encrypted_file_name = models.TextField(null=True)
    owner_id = models.ForeignKey(Users, on_delete=models.CASCADE)

    def __str__(self):
        return self.name