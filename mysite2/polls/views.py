from django.http import HttpResponse,HttpResponseRedirect

from django.http import Http404
from django.template import loader
from django.shortcuts import render,get_object_or_404
from django.urls import reverse

from .models import Question,Choice
from django.db.models import F
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    def get_queryset(self):
        """return the last 10 published questions"""
        # return Question.objects.order_by("-pub_date")[:10]
        # filtering so that no future questions are included

        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:10]
    
        # Question.objects.filter(pub_date__lte=timezone.now()) 
        # returns a queryset containing Questions whose pub_date is less 
        # than or equal to - that is, earlier than or equal to - timezone.now.


# def index(request):
#     latest_question_list = Question.objects.order_by("-pub_date")
#     template = loader.get_template("polls/index.html")
#     context = {
#         "latest_question_list": latest_question_list,
#     }
    
#     return HttpResponse(template.render(context,request))

#     # return render( request,"polls/index.html", context) # can also use this


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    # even though future questions don’t appear in the index, 
    # users can still reach them if they know or guess the right URL. 
    # So we need to add a similar constraint to DetailView

    def get_queryset(self):
        """exclude question are not published yet"""
        return Question.objects.filter(pub_date__lte=timezone.now())

# def detail(request , question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question  does not exist")
    
#     # can also use this : 
#     # question = get_object_or_404(Question, pk=question_id)

#     return render(request,"polls/detail.html",{"question":question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

# def results(request , question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request , "polls/results.html",{"question":question})

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        # pk=request.POST["choice"] gives the string output of selected choice id
    except (KeyError, Choice.DoesNotExist): 
        # redisplay the question voting form
        
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "you didn't select a choice,",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.

        return HttpResponseRedirect(reverse("polls:results",args=(question.id,)))
        # HttpResponseRedirect takes a single argument: the URL to which the user will be redirected