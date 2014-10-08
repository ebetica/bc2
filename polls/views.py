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
        p = context['poll']
        total = p.voter_set.count()
        context['total'] = total
        choices = context['poll'].choice_set.all()
        if p.type in [p.SIMPLE, p.MULTI]:
            context['map'] = sorted([(choice, choice.vote_set.count()) for choice in choices],
                                    key=lambda x: x[1],
                                    reverse=True)
        elif p.type == p.RANKED:
            losers = []
            winners = []
            rest = [choice for choice in p.choice_set.all()]
            test = []
            while rest:
                ctr = {r:[0 for i in rest] for r in rest}
                for voter in p.voter_set.all():
                    votes = [vote for vote in voter.vote_set.all()]
                    votes.sort(key=lambda vote: vote.ranking)
                    ind = 0
                    for i in votes:
                        c = i.choice
                        if c in rest:
                            ctr[c][ind] = ctr[c][ind] + 1
                            ind+=1
                ranking = sorted(ctr.items(), key=lambda x: x[1], reverse=True)
                if ranking[0][1][0] > total/2:
                    winners.append(ranking[0][0])
                    rest.remove(ranking[0][0])
                else:
                    losers.append(ranking[-1][0])
                    rest.remove(ranking[-1][0])
                test.append(ctr)
            ranking = winners + list(reversed(losers))
            respective_votes = [", ".join(
                [str(choice.vote_set.filter(ranking=k).count()) for k in range(len(ranking))])
                                for i,choice in enumerate(ranking)
                               ]
            context['map'] = zip(ranking, respective_votes)

        return context

def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    if p.type in [p.SIMPLE, p.MULTI]:
        try:
            choice_ids = request.POST.getlist('choice')
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
                voter.save()
            for vote in voter.vote_set.all():
                vote.delete()
            for id in choice_ids:
                choice = p.choice_set.get(pk=id)
                vote = Vote(voter=voter)
                vote.choice = choice
                vote.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
    elif p.type == p.RANKED:
        try:
            voter = Voter.objects.get(user=request.user, poll=p)
        except Voter.DoesNotExist:
            voter = Voter(poll=p, user=request.user)
            voter.save()
        for vote in voter.vote_set.all():
            vote.delete()
        rank = request.POST.get('rank').split(',')
        for i,e in enumerate(rank):
            choice = p.choice_set.get(pk=e)
            vote = Vote(voter=voter)
            vote.choice = choice
            vote.ranking = i;
            vote.save()
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))
    else:
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "Poll not implemented :(",
            })


