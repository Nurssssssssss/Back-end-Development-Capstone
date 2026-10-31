from django.db import models
class Concert(models.Model):
    venue=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    date=models.DateField()
    def __str__(self):return f'{self.venue} ({self.date})'
