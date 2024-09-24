from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.db.models import F
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views import generic
from .forms import QuestionForm, ChoiceFormSet, ChoiceForm
from .models import Choice, Question
from django.utils import timezone

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return all questions ordered by publication date (latest first).
        """
        return Question.objects.order_by("-pub_date")

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

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

class AddQuestionView(View):
    template_name = 'polls/add_question.html'

    def get(self, request):
        question_form = QuestionForm()
        formset = ChoiceFormSet(queryset=Choice.objects.none(), prefix='form')
        return render(request, self.template_name, {'question_form': question_form, 'formset': formset})

    def post(self, request):
        question_form = QuestionForm(request.POST)
        formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none(), prefix='form')

        if question_form.is_valid() and formset.is_valid():
            valid_choices = [form for form in formset if form.cleaned_data.get('choice_text', '').strip()]
            if len(valid_choices) < 3:
                return render(request, self.template_name, {
                    'question_form': question_form,
                    'formset': formset,
                    'error_message': "You must enter at least 3 valid choices.",
                })

            question = question_form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()

            for form in valid_choices:
                choice = form.save(commit=False)
                choice.question = question
                choice.save()

            return redirect(reverse('polls:index'))

        return render(request, self.template_name, {'question_form': question_form, 'formset': formset})