from django.db import models

from project_manager.users.models import User


class ContentModel(models.Model):
    """Abstract model for repeating fields: title, content"""

    title = models.CharField(max_length=150)
    content = models.TextField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title


class Workspace(ContentModel):
    owner = models.ForeignKey(
        User, related_name="own_workspaces", on_delete=models.CASCADE
    )
    avatar = models.ImageField(upload_to="workspaces/avatars", blank=True)


class UserWorkspace(models.Model):
    user = models.ForeignKey(
        User, related_name="workspaces", on_delete=models.CASCADE
    )
    workspace = models.ForeignKey(
        Workspace, related_name="users", on_delete=models.CASCADE
    )
    is_admin = models.BooleanField(default=False)


class List(ContentModel):
    workspace = models.ForeignKey(
        Workspace, related_name="lists", on_delete=models.CASCADE
    )
    avatar = models.ImageField(upload_to="lists/avatars", blank=True)
