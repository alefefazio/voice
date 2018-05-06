from django.contrib import admin

from core.models import ActivityLog, Todo, Personality, Question, Choice


class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ('type', 'logged_user', 'created_at')

# class TodoAdmin(admin.ModelAdmin):
#     list_display = ('description', 'done')

class PersonalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'abstract')

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice', 'Personality', 'Question')


admin.site.register(ActivityLog, ActivityLogAdmin)
admin.site.register(Personality, PersonalityAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
