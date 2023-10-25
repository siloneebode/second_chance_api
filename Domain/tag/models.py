from django.db import models


class Tag(models.Model):
    name = models.CharField(null=False, max_length=60)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
