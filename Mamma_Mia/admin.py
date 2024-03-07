from django.contrib import admin
from Mamma_Mia.models import (Ingredient, Pizza, Topping,
                              Order, Idea, Comment, Complaint)


admin.site.register(Ingredient)
admin.site.register(Topping)
admin.site.register(Idea)
admin.site.register(Comment)
admin.site.register(Complaint)
admin.site.register(Order)
admin.site.register(Pizza)
