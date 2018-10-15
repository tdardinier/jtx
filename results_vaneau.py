import sys
reload(sys)
sys.setdefaultencoding('utf8')

import django
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "jtx.settings")
django.setup()

from vote.models import *

for c in VoteCategory.objects.all():
    print("\nCategorie : " +  c.name.encode('utf-8'))
    for v in c.videos.all():
        i = 0
        for vote in v.votes.all():
            i += 1
        print("Video : " + v.name.encode('utf-8') + " => " + v.description.encode('utf-8') + " : " + str(i))
