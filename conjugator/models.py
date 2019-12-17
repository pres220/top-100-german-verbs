from django.db import models


class Verb(models.Model):
    """Table representing the top 100 German verbs"""
    infinitive = models.CharField(primary_key=True, max_length=30)
    frequency = models.PositiveSmallIntegerField(unique=True)
    translation = models.CharField(max_length=50, blank=True)
    present_participle = models.CharField(max_length=30, blank=True)
    past_participle = models.CharField(max_length=30, blank=True)

    class Meta:
        ordering = ['frequency']

    def __str__(self):
        return self.infinitive


class Mood(models.Model):
    """Table representing grammatical mood"""
    name = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return self.name


class Tense(models.Model):
    """Table representing grammatical tense"""
    name = models.CharField(primary_key=True, max_length=30)

    def __str__(self):
        return self.name


class Conjugation(models.Model):
    """Table representing German verb conjugation patterns"""
    verb = models.ForeignKey(Verb, on_delete=models.CASCADE)
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
            models.UniqueConstraint(fields=['verb', 'mood', 'tense'], name='unique_conjugation')
        ]

    def __str__(self):
        return f'{self.verb} {self.mood} {self.tense}'
