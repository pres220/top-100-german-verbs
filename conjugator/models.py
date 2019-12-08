from django.db import models


class Verb(models.Model):
    infinitive = models.CharField(primary_key=True, max_length=30)
    frequency = models.PositiveSmallIntegerField(unique=True)
    translation = models.CharField(max_length=50, blank=True)
    present_participle = models.CharField(max_length=30, blank=True)
    past_participle = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.infinitive


class Mood(models.Model):
    mood = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return self.mood


class Tense(models.Model):
    tense = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return self.tense


class Conjugation(models.Model):
    infinitive = models.ForeignKey(Verb, on_delete=models.CASCADE)
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE)
    tense = models.ForeignKey(Tense, on_delete=models.CASCADE)
    ich = models.CharField(max_length=30, blank=True)
    du = models.CharField(max_length=30, blank=True)
    er = models.CharField(max_length=30, blank=True)
    wir = models.CharField(max_length=30, blank=True)
    ihr = models.CharField(max_length=30, blank=True)
    sie = models.CharField(max_length=30, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['infinitive', 'mood', 'tense'], name='unique_conjugation')
        ]

    def __str__(self):
        return f'{self.infinitive} {self.mood} {self.tense}'
