from django.test import TestCase
from catalog.models import Concert
from songs.models import Song
from photos.models import Photo
from datetime import date
from unittest.mock import patch
import os
from catalog.views import fetch_api
class PageSmokeTests(TestCase):
    def test_home_and_admin(self):
        self.assertEqual(self.client.get('/').status_code,200)
        self.assertEqual(self.client.get('/admin/login/').status_code,200)
    def test_song_list_and_modal(self):
        Song.objects.create(title='Midnight Sky',artist='Northbound',lyrics='Hello')
        r=self.client.get('/songs/')
        self.assertContains(r,'Midnight Sky')
        self.assertContains(r,'showModal()')
    def test_photo_and_concerts(self):
        Photo.objects.create(title='Test Concert',image_url='https://example.org/photo.jpg')
        Concert.objects.create(venue='Astana',location='Kazakhstan',date=date(2026,12,5))
        self.assertContains(self.client.get('/photos/'),'Test Concert')
        self.assertContains(self.client.get('/concerts/'),'Astana')

    @patch.dict(os.environ, {'SONGS_API_URL':'https://songs.example.test'})
    @patch('catalog.views.fetch_api')
    def test_song_page_uses_service_data(self, fetch):
        fetch.return_value={'songs':[{'id':7,'title':'Service Track','artist':'Northbound','lyrics':'Live words'}]}
        self.assertContains(self.client.get('/songs/'),'Service Track')
        fetch.assert_called_once_with('https://songs.example.test','/song')

    @patch.dict(os.environ, {'PICTURES_API_URL':'https://pictures.example.test'})
    @patch('catalog.views.fetch_api')
    def test_photo_page_uses_service_data(self, fetch):
        fetch.return_value=[{'event_city':'Astana','event_date':'2026-10-31','pic_url':'/static/images/concert.jpg'}]
        self.assertContains(self.client.get('/photos/'),'Astana')
        fetch.assert_called_once_with('https://pictures.example.test','/picture')

    @patch('catalog.views.urlopen',side_effect=OSError('unavailable'))
    def test_unavailable_service_returns_fallback_signal(self, _):
        self.assertIsNone(fetch_api('https://unavailable.example.test','/song'))
