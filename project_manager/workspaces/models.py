from django.db import models

from project_manager.users.models import User


class ContentModel(models.Model):
    """Abstract model for repeating fields: name, description"""

    name = models.CharField(max_length=150)
    description = models.TextField()

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name


class Workspace(ContentModel):
    owner = models.ForeignKey(
        User, related_name="own_workspaces", on_delete=models.CASCADE
    )
    avatar = models.ImageField(upload_to="workspaces/avatars", blank=True)
    users = models.ManyToManyField(
        User, related_name="users", through="UserWorkspace"
    )


class UserWorkspace(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)


class TaskList(ContentModel):
    workspace = models.ForeignKey(
        Workspace, related_name="task_lists", on_delete=models.CASCADE
    )
