from django.contrib import admin

from .models import Question,Choice     # edit


# Register your models here.


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model=Choice
    extra = 3

# admin.site.register(Question)   # edit
class QuestionAdmin(admin.ModelAdmin):
    # fields = ["pub_date","question_text"]
    fieldsets = [
        (None, {"fields":["question_text"]}),
        ("Date information", {"fields":
        ["pub_date"],"classes":["collapse"]}),
    ]
    inlines = [ChoiceInline]
    list_display = ["question_text","pub_date","was_published_recently"]
    list_filter=["pub_date"]   # adds filter sidebar for 
    search_fields=["question_text"]  # search field 
    list_per_page = 5   # pagination
# This tells Django: “Choice objects are edited on the Question admin page
#  By default, provide enough fields for 3 choices.”

admin.site.register(Question, QuestionAdmin)


# admin.site.register(Choice)   # edit


