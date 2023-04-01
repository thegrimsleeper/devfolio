from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory, inlineformset_factory

from .models import Question, Choice, UserProfile
from .forms import QuestionForm

class IndexView(ListView):
    template_name = 'pollsapp/index.html'
    model = Question
    paginate_by = 10

    def get_queryset(self):
        queryset = Question.objects.order_by("-published_date")
        return queryset


class SignUp(CreateView):
    template_name = 'pollsapp/signup.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('pollsapp:index_url')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

@login_required
def create_question(request):
    if request.method == "POST":
        question_form = QuestionForm(data=request.POST)
        choiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',), can_delete=False, extra=2)
        formset = choiceFormSet
        formset = formset(data=request.POST)

        if all([question_form.is_valid, formset.is_valid]):
            question = question_form.save(commit=False)
            question.author = UserProfile.objects.get(user=request.user)
            question.save() 
            for form in formset:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()
        # Change to vote page?
        return redirect(reverse('pollsapp:index_url')) 

    question_form = QuestionForm()
    choiceFormSet = inlineformset_factory(Question, Choice, fields=('choice_text',), can_delete=False, extra=2)
    formset = choiceFormSet
    context = {'question_form': question_form, 'formset': formset}
    return render(request, 'pollsapp/new_poll.html', context=context)


class PollView(LoginRequiredMixin, DetailView):
    template_name = 'pollsapp/vote.html'
    model = Question


def vote(request, pk):
    question = Question.objects.get(pk=pk)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'pollsapp/detail.html', context={'question': question, 'error_message': "You didn't select a choice"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('pollsapp:results_url', args=(question.id,)))


class ResultsView(DetailView):
    template_name = 'pollsapp/results.html'
    model = Question