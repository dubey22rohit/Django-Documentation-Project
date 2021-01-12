from django.shortcuts import render,get_object_or_404
from django.http import Http404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Question,Choice
from django.db.models import F#Used to counter the race around condition
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_questions_list'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


# def index(request):
#     latest_questions_list = Question.objects.order_by('-pub_date')[:5]
#     #template = loader.get_template('polls/index.html')
#     context = {
#         'latest_questions_list' : latest_questions_list,
#     }
#     #output = ' ,'.join([q.question_text for q in latest_questions_list])
#     #return HttpResponse(template.render(context,request))
#     return render(request,'polls/index.html',context)

# def detail(request,question_id):
#     return HttpResponse("You are viewing question %s" %question_id)

# def results(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)#QUestion.object.get(pk=question_id)
#     return render(request,'polls/results.html',{'question':question})

def vote(request,question_id):
    question = get_object_or_404(Question,pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError,Choice.DoesNotExist):
        return render(request,'polls/detail.html',{'question':question,'error_message':"You didn't select anything!"})    
    else:
        selected_choice.votes= F('votes')+1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))    


# def detail(request,question_id):
#     question = get_object_or_404(Question,pk=question_id)
#     return render(request,"polls/detail.html",{"question":question})

# def detail(request,question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except:
#         raise Http404("Question Does not exist")
#     return render(request,'polls/detail.html',{'question':question})
