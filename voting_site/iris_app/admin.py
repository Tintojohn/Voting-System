from django.contrib import admin
from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Voter)
admin.site.register(Add_Nominee)
admin.site.register(Votes)
admin.site.register(CreateElection)
admin.site.register(voting_count)
