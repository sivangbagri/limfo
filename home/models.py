from django.db import models


# Create your models here.

class Feedback(models.Model):
    name = models.CharField(max_length=20, default='')
    email = models.CharField(max_length=20, default='')

    text = models.TextField(default='')

    def __str__(self):
        return 'Feedback from ' + str(self.name)
