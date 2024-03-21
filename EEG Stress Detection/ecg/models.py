# ecg/models.py
from django.db import models

class ECGRecord(models.Model):
    tp9 = models.FloatField()
    tp10 = models.FloatField()
    af8 = models.FloatField()
    af7 = models.FloatField()
    right_aux = models.FloatField()
    output = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Record {self.id}'
