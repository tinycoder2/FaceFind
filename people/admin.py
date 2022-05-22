from email.errors import MissingHeaderBodySeparatorDefect
from django.contrib import admin

# Register your models here.
from .models import MissingPerson, ReportedPerson

admin.site.register(MissingPerson)

admin.site.register(ReportedPerson)