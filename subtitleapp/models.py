from django.db import models


class Subtitle(models.Model):
    name = models.CharField(max_length=250)
    output_text = models.TextField()

    def __str__(self):
        return self.name
