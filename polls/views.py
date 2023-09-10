from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from .models import Choice, Question


class IndexView(generic.ListView):
    """
    Display the latest five questions.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """
    Display a question and its choices.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handel the Get request for the detail view.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs["pk"])
        except Http404:
            messages.error(request,
                           f"Poll number {kwargs['pk']} does not exists.")
            return redirect("polls:index")
        if not question.is_published():
            messages.error(request,
                           f"Poll number {question.id} Already closed.")
            return redirect("polls:index")
        return render(request, self.template_name, {"question": question})


class ResultsView(generic.DetailView):
    """
    Display the results of a question.
    """
    model = Question
    template_name = 'polls/results.html'

    def get(self, request, *args, **kwargs):
        """
        Handel the Get request for the results view.
        """
        try:
            question = get_object_or_404(Question, pk=kwargs["pk"])
        except Http404:
            messages.error(request,
                           f"Poll number {kwargs['pk']} does not exists.")
            return redirect("polls:index")
        if not question.is_published():
            messages.error(request,
                           f"Poll number {question.id} Already closed.")
            return redirect("polls:index")
        return render(request, self.template_name, {"question": question})


def vote(request, question_id):
    """
    Handles the user's vote for a poll question.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,)))
