# data_import/models.py

from django.db import models

class DHSI2(models.Model):
    date_importation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"DHSI2 - {self.date_importation}"

    class Meta:
        db_table = 'DHSI2'
        managed = False