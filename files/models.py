from django.db import models
from django.contrib.auth.models import User


class Items(models.Model):
    """
    This object represents a file or a folder in the database.
    """
    name = models.CharField(max_length=100)
    is_file = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shared_with = models.ManyToManyField(User, related_name='shared_with', blank=True)
    global_shared = models.BooleanField(default=False)

    def is_root(self):
        """
        It's a root folder if it has no parent.
        """
        return not self.parent
