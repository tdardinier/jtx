f = open("membres.txt").readlines()
from videos.views import *

promo = int(f[0])

for line in f[1:]:
    l = line.split(" ")
    a = Auteur(firstname=l[0], lastname=" ".join(l[1:]).rstrip(), promo=promo)
    a.save()
