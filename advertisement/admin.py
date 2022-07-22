from django.contrib import admin
from advertisement.models import Advertisement, Category
from users.models import User, Location

admin.site.register(Advertisement)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Location)



