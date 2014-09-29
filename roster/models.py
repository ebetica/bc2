from django.db import models
from django.contrib.auth.models import User


class Resident(models.Model):
    user = models.ForeignKey(User, primary_key=True)
    PETERS = 'PE'
    ROGERS = 'RO'
    HOMLES = 'HO'
    TUCKER = 'TU'
    HARRISON = 'HA'
    MCGUFFEY = 'MC'
    GILDERSLEEVE = 'GI'
    VENABLE = 'VE'
    DAVIS = 'DA'
    MALLET = 'MA'
    LONG = 'LO'
    SMITH = 'SM'
    PORTALS = (
        (PETERS, 'Peters'),
        (ROGERS, 'Rogers'),
        (HOMLES, 'Holmes'),
        (TUCKER, 'Tucker'),
        (HARRISON, 'Harrison'),
        (MCGUFFEY, 'McGuffey'),
        (GILDERSLEEVE, 'Gildersleeve'),
        (VENABLE, 'Venable'),
        (DAVIS, 'Davis'),
        (MALLET, 'Mallet'),
        (LONG, 'Long'),
        (SMITH, 'Smith'),
    )
    portal = models.CharField(max_length=2, choices=PORTALS)
    room_number = models.CharField(max_length=10)
    room_subnumber = models.CharField(max_length=2)

    def __unicode__(self):
        return self.user.__unicode__()


class GovboardPosition(models.Model):
    position_max = models.IntegerField(default=1)
    position_name = models.CharField(max_length=10, primary_key=True)

    def __unicode__(self):
        return "%s (%d)" % (self.position_name, self.position_max)

    def members(self):
        return GovboardMember.objects.filter(position=self)


class GovboardMember(models.Model):
    user = models.ForeignKey(User, primary_key=True)
    position = models.ForeignKey(GovboardPosition)

