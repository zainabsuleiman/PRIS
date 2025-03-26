from django.db import models

# Create your models here.
class Rdb(models.Model):
    company_name = models.CharField(max_length=200)
    tin_number = models.CharField(max_length=20)
    def __str__(self):
        return self.company_name
    class Meta:
        db_table ='Rdb'