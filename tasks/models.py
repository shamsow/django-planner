from django.db import models
from django.urls import reverse
from dashboard.models import Activity
# Create your models here.

class Task(models.Model):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    PRIORITY_CHOICES = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High")
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    time = models.TimeField()
    date = models.DateField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=LOW)
    profile_id = models.IntegerField()
    completed = models.BooleanField(default=False)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse("task_detail", kwargs={"id": self.id})

    def __str__(self):
        return f"{self.title}"
    

    class Meta:
        ordering = ['date', 'time', '-priority']