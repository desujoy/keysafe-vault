from django.contrib import admin
from .models import PassDB,SecNotesDB,CardsDB, FileDB

admin.site.register(PassDB)
admin.site.register(SecNotesDB)
admin.site.register(CardsDB)
admin.site.register(FileDB)


# Register your models here.
