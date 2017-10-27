from videos.models import *
noms = ["Raid", "TSGED", "La Courtine"]
images = ["raid.jpg", "tsged.png", "courtine.jpg"]
for i in range(len(noms)):
    for r in Tag.objects.get(titre=noms[i]).relation_tag_set.all():
      for p in r.video.relation_proj_set.all():
        proj = p.proj
        #proj.image = "/videos/affiches/" + images[i]
        #proj.save()
        print(proj.image)

kes = Category.objects.get(titre="Campagne Kès")
for p in Proj.objects.filter(category=kes):
  p.image = "/videos/affiches/kes.png"
  p.save()
