from django.contrib.auth.models import User
from django.db import models


class Poll(models.Model):
    question = models.CharField(max_length=200)
    start_date = models.DateTimeField('Starting Date')
    end_date = models.DateTimeField('Ending Date')
    SIMPLE = 'S'
    MULTI = 'M'
    RANKED = 'R'
    TYPES = (
        (SIMPLE, 'Simple'),
        (MULTI, 'Multiple Choice'),
        (RANKED, 'Ranked Choice'),
    )
    type = models.CharField(max_length=1, choices=TYPES)

    def __unicode__(self):
        return self.question


class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice_text = models.CharField(max_length=200)

    def __unicode__(self):
        return self.choice_text

class Voter(models.Model):
    poll = models.ForeignKey(Poll)
    user = models.ForeignKey(User)

class Vote(models.Model):
    voter = models.ForeignKey(Voter)
    choice = models.ForeignKey(Choice)
    ranking = models.IntegerField(default=0)
