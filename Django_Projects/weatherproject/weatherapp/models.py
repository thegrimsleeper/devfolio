from django.db import models

# Create your models here.
class City(models.Model):
    city_name = models.CharField(max_length=127)
    latitude = models.DecimalField(max_digits=6 , decimal_places=4, null=True, blank=True)
    longitude = models.DecimalField(max_digits=7, decimal_places=4,  null=True,  blank=True)

    def __str__(self):
        return self.city_name

    # Show the plural of city as cities instead of citys
    class Meta:
        verbose_name_plural = 'cities' 