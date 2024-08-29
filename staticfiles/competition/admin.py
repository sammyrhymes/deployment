from django.contrib import admin
from .models import Competition, Entry, Winner, BasketItem, MpesaTransaction, CompetitionImage


class CompetitionImageInline(admin.TabularInline):
    model = CompetitionImage
    extra = 1  # Number of extra forms to display for adding new images

class CompetitionAdmin(admin.ModelAdmin):
    inlines = [CompetitionImageInline]

admin.site.register(Competition)
admin.site.register(Entry)
admin.site.register(Winner)
admin.site.register(BasketItem)
admin.site.register(MpesaTransaction)
# admin.site.register(CompetitionAdmin)
admin.site.register(CompetitionImage)
