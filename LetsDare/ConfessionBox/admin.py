from django.contrib import admin
from ConfessionBox.models import User, CnfBox, Result, AnsOfCnfBox

# Register your models here.
admin.site.register(User)
admin.site.register(CnfBox)
admin.site.register(Result)
admin.site.register(AnsOfCnfBox)