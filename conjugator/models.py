from django.db import models

class Verb(models.Model):
    infinitive = models.CharField(primary_key=True, max_length=30)
    frequency = models.PositiveSmallIntegerField(unique=True)
    translation = models.CharField(max_length=50, blank=True)
    past_participle = models.CharField(max_length=30, blank=True)

    # Present tense
    present_ich = models.CharField(max_length=30, blank=True)
    present_du = models.CharField(max_length=30, blank=True)
    present_er = models.CharField(max_length=30, blank=True)
    present_wir = models.CharField(max_length=30, blank=True)
    present_ihr = models.CharField(max_length=30, blank=True)
    present_sie = models.CharField(max_length=30, blank=True)

    # Present perfect tense
    perfect_ich = models.CharField(max_length=30, blank=True)
    perfect_du = models.CharField(max_length=30, blank=True)
    perfect_er = models.CharField(max_length=30, blank=True)
    perfect_wir = models.CharField(max_length=30, blank=True)
    perfect_ihr = models.CharField(max_length=30, blank=True)
    perfect_sie = models.CharField(max_length=30, blank=True)

    # Simple past tense
    past_ich = models.CharField(max_length=30, blank=True)
    past_du = models.CharField(max_length=30, blank=True)
    past_er = models.CharField(max_length=30, blank=True)
    past_wir = models.CharField(max_length=30, blank=True)
    past_ihr = models.CharField(max_length=30, blank=True)
    past_sie = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.infinitive
