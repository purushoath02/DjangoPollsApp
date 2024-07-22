from django.http import Http404
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template import loader
from .models import Question, Choice
from django.core.serializers import serialize
import json
from django.urls import reverse
def index(request):
    template = 'polls/index.html'
    return render(request,template)

def get_questions(request):
    question_list = Question.objects.order_by("-pub_date")[:5]

    list =[]
    for question in question_list:
        question_data = {
            'q_id':question.id,
            'question_text': question.question_text,
            'pub_date': question.pub_date.strftime('%Y-%m-%d %H:%M:%S')  # Format pub_date as string
        }
        list.append(question_data)
    return JsonResponse({'questions': list})



def detail(request, question_id):
    try:
        question = Question.objects.get(pk = question_id)
        # choices = Choice.objects.get(question_id = question_id)
        # print(choices)
        print(question)
    except Question.DoesNotExist:
        raise Http404("Question Does Not exist")

    return render(request, 'polls/detail.html',{'question':question})


def get_poll(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesnotExist:
        raise Http404("Question does not exist")
    return JsonResponse({'question'})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
