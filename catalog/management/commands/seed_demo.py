from datetime import date
from django.core.management.base import BaseCommand
from songs.models import Song
from photos.models import Photo
from catalog.models import Concert
class Command(BaseCommand):
    help='Create sample concerts and album content in local database'
    def handle(self,*args,**kwargs):
        for title,artist,lyrics in [
          ('Midnight Sky','Northbound','Under a midnight sky, the road goes on.'),
          ('City Lights','Northbound','Every window tells a story.'),
          ('After the Rain','Northbound','The sun returns to quiet streets.')]:
            Song.objects.get_or_create(title=title,defaults={'artist':artist,'lyrics':lyrics})
        Photo.objects.update_or_create(title='Live performance',defaults={'image_url':'/static/images/concert.jpg'})
        Concert.objects.get_or_create(venue='Astana Music Hall',date=date(2026,12,5),defaults={'location':'Astana, Kazakhstan'})
        Concert.objects.get_or_create(venue='Almaty Live Stage',date=date(2026,12,12),defaults={'location':'Almaty, Kazakhstan'})
        self.stdout.write(self.style.SUCCESS('Sample songs, photos and concerts are ready.'))
