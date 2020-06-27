from django.db import models
from django.urls import reverse

# Create your models here.
class Activity(models.Model):
    profile_id = models.IntegerField()
    date = models.DateField()
    
    def get_absolute_url(self):
        return reverse("date_detail", kwargs={"slug": self.date})

    def __str__(self):
        return f"{self.date}"

    class Meta:
        ordering = ['date']