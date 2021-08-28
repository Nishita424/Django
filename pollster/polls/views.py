from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Question, Choice

# Get questions and display them
def index(request):
    latest_questions = Question.objects.order_by('-pub_date')
    context = {'latest_questions': latest_questions}
    return render(request, 'polls/index.html', context)
    
# Show specific question and choices
def detail(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request, 'polls/detail.html', {'question': question})
    
# Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'polls/results.html', {'question': question})
    
# Vote
def vote(request, question_id):
    # print(request)  # <WSGIRequest: POST '/polls/6/vote/'>
    # print("here", request.POST['choice']) # POST name=value => choice=13
    
    try:
        selected_choice = Choice.objects.filter(question__id=question_id).get(id=request.POST['choice'])
    except (KeyError):
        question = get_object_or_404(Question, id=question_id)
        return render(request, 'polls/detail.html', {
            'question': question, 'errorMessage': 'You did not select a choice'
        })
    selected_choice.votes += 1
    selected_choice.save()
    
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
