from django.db import models

# Create your models here.
class Gadget(models.Model):
    name = models.CharField(max_length=64, unique=True)
    kind = models.TextField(blank=True)
    price = models.PositiveSmallIntegerField(null=True)

    def __str__(self):
        return f"Name<{self.name}>,Kind<{self.kind}>,Price<{self.price}>;"
