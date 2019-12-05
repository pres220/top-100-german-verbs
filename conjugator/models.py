from django.db import models

class Infinitive(models.Model):
    name = models.CharField(primary_key=True, max_length=30)
    frequency = models.PositiveSmallIntegerField(unique=True)

    def __str__(self):
        return self.name

class Verb(models.Model):
    infinitive = models.CharField(primary_key=True, max_length=30)
    translation = models.CharField(max_length=50)
    past_participle = models.CharField(max_length=30)

    # Present tense
    present_ich = models.CharField(max_length=30)
    present_du = models.CharField(max_length=30)
    present_er = models.CharField(max_length=30)
    present_wir = models.CharField(max_length=30)
    present_ihr = models.CharField(max_length=30)
    present_sie = models.CharField(max_length=30)

    # Present perfect tense
    perfect_ich = models.CharField(max_length=30)
    perfect_du = models.CharField(max_length=30)
    perfect_er = models.CharField(max_length=30)
    perfect_wir = models.CharField(max_length=30)
    perfect_ihr = models.CharField(max_length=30)
    perfect_sie = models.CharField(max_length=30)

    # Simple past tense
    past_ich = models.CharField(max_length=30)
    past_du = models.CharField(max_length=30)
    past_er = models.CharField(max_length=30)
    past_wir = models.CharField(max_length=30)
    past_ihr = models.CharField(max_length=30)
    past_sie = models.CharField(max_length=30)
