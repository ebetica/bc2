from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from polls.models import Poll, Choice, Voter, Vote


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        return Poll.objects.filter(start_date__lte=timezone.now()).filter(end_date__gte=timezone.now()).order_by('start_date').reverse()


class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Poll.objects.filter(start_date__lte=timezone.now()).filter(end_date__gte=timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        choices = context['poll'].choice_set.all()
        context['map'] = {choice.choice_text: len(choice.vote_set.all()) for choice in choices}
        return context

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    if p.type == p.SIMPLE:
        try:
            selected_choice = p.choice_set.get(pk=request.POST['choice'])
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the poll voting form.
            return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
            })
        else:
            try:
                voter = Voter.objects.get(user=request.user, poll=p)
            except Voter.DoesNotExist:
                voter = Voter(poll=p, user=request.user)
            try:
                vote = Vote.objects.get(voter=voter)
            except Vote.DoesNotExist:
                vote = Vote(voter=voter)
            voter.save()
            vote.choice = selected_choice
            vote.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
