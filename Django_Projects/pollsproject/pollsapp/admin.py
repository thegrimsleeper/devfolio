from django.contrib import admin
from .models import Question, Choice, UserProfile




# class ChoiceInline(admin.StackedInline):
# Vs. 
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):

    # update to view of 'question details' to Change order of fields
    # fields = ['pub_date', 'question_text']

    # update to view of 'question details'; fieldsets group fields via list of tuples : (title of fieldset, dict of fields list, template if custom)
    fieldsets = [
        (None,                  {'fields': ['question_text']}),
        ('Date Information',    {'fields': ['published_date'], 'classes': ['collapse']}),
    ]
    # The 'classes' key added above and inlines var below to include Choices in the quesitons detail/create view
    inlines = [ChoiceInline]

    # update to view of 'all questions' setting fields to be displayed; overrides the __str__ of model
    list_display = ('question_text', 'published_date',)

    # update to screen of 'all questions' allowing filters based on fields
    list_filter = ['published_date']

    # update to screen of 'all questions' providing search functionality
    search_fields = ['question_text']



admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(UserProfile)