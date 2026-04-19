from django.contrib import admin
from mainApp.models import Story, StoryTranslation, Prompt, Difficulty, Language

# Register your models here.

class StoryTranslationInline(admin.TabularInline):
    model = StoryTranslation
    extra = 0

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    inlines = [StoryTranslationInline]

# admin.site.register(Story)
admin.site.register(StoryTranslation)
admin.site.register(Prompt)
admin.site.register(Difficulty)
admin.site.register(Language)
