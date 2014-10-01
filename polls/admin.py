from django.contrib import admin
from polls.models import Poll, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
	(None,               {'fields': ['type', 'question', 'max_choices']}),
	('Date information', {'fields': ['start_date', 'end_date']}),
    ]
    list_display = ('question', 'start_date', 'end_date')
    inlines = [ChoiceInline]
    list_filter = ['start_date']
    search_fields = ['question']


admin.site.register(Poll, PollAdmin)
