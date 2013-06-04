from django.db import models

class Epub(models.Model):
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=4000)
    author = models.CharField(max_length=30)

    def __unicode__(self):
        return self.title
