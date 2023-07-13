from django.db import models
from django.contrib.auth.models import User


class Items(models.Model):
    """
    This object represents a file or a folder in the database.
    """
    name = models.CharField(max_length=100)
    size = models.IntegerField(null=True, blank=True)  # in bytes
    is_file = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    real_path = models.CharField(max_length=1000, null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    shared_with = models.ManyToManyField(User, related_name='shared_with', blank=True)
    global_shared = models.BooleanField(default=False)

    def is_root(self):
        """
        It's a root folder if it has no parent.
        """
        return not self.parent

    def get_literal_size(self) -> str:
        """
        Returns the size of the file in a human-readable format.
        """
        if not self.is_file:
            return ""
        if self.size < 1000:
            return f"{self.size} B"
        elif self.size < 1000000:
            return f"{round(self.size / 1000, 2)} KB"
        elif self.size < 1000000000:
            return f"{round(self.size / 1000000, 2)} MB"
        else:
            return f"{round(self.size / 1000000000, 2)} GB"
