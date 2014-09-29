__author__ = 'zeming'

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.conf import settings
from roster.models import Resident

import csv
import re
import random
import string
import os

class Command(BaseCommand):
    args = "spreadsheet_name"
    help = ""

    def handle(self, *args, **options):
        self.stdout.write(os.path.join(settings.BASE_DIR, args[0]))
        with open(os.path.join(settings.BASE_DIR, args[0]), 'rb') as csvfile:
            rosterreader = csv.reader(csvfile)
            header = next(rosterreader)
            i_portal = None
            i_fname = None
            i_lname = None
            i_room = None
            i_email = None
            for i,e in enumerate(header):
                if re.search("building", e, flags=re.IGNORECASE):
                    i_portal = i
                elif e == "Room":
                    i_room = i
                elif re.search("last", e, flags=re.IGNORECASE):
                    i_lname = i
                elif re.search("first", e, flags=re.IGNORECASE):
                    i_fname = i
                elif re.search("mail", e, flags=re.IGNORECASE):
                    i_email = i
            if any([k==None for k in [i_portal,i_fname,i_lname, i_room, i_email]]):
                self.stderr.write("Sheet appears to be in the wrong format, nothing happened")
                return

            processed_portals = {v: k for k, v in dict(Resident.PORTALS).items()}
            for row in rosterreader:
                portal = row[i_portal]
                fname = row[i_fname]
                lname = row[i_lname]
                room = row[i_room]
                email = row[i_email]

                netid = email.split("@")[0]
                user = None
                try:
                    user = User.objects.get(username=netid)
                except ObjectDoesNotExist:
                    passwd = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                    user = User.objects.create_user(netid, email=email, password=passwd)
                    user.first_name = fname
                    user.last_name = lname
                    user.save()
                    self.stdout.write("Creating %s with password %s" % (netid, passwd))
                except MultipleObjectsReturned:
                    self.stderr.write("We found more than one user with that net id! Script crashes :(")
                    return

                self.stdout.write(room.split('-')[0])
                num = room.split('-')[0]
                subnum = room.split('-')[1]
                resident = Resident(user=user, portal=processed_portals[portal], room_number=num, room_subnumber=subnum)
                resident.save()
