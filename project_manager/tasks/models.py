from django.db import models

from project_manager.users.models import User
from project_manager.workspaces.models import ContentModel


class Status(models.Model):
    """Status model"""

    name = models.CharField(max_length=50)


class Task(ContentModel):
    """Task model"""

    task_list = models.ForeignKey(
        "workspaces.TaskList", related_name="tasks", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.PROTECT)


class StatusChanges(models.Model):
    """Model for tracking status changes"""

    task = models.ForeignKey(
        Task, related_name="status_changes", on_delete=models.CASCADE
    )
    from_status = models.ForeignKey(
        Status, related_name="status_changes_from", on_delete=models.CASCADE
    )
    to_status = models.ForeignKey(
        Status, related_name="status_changes_to", on_delete=models.CASCADE
    )


class TaskImage(models.Model):
    """Task images model"""

    task = models.ForeignKey(
        Task, related_name="images", on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to="tasks/images")


class Attachment(models.Model):
    """Task file attachments model"""

    task = models.ForeignKey(
        Task, related_name="attachments", on_delete=models.CASCADE
    )
    attachment = models.FileField(upload_to="tasks/attachments")


class Tag(models.Model):
    """Tag model"""

    name = models.CharField(max_length=20)


class TaskTag(models.Model):
    """Many-to-many relationship between Task and Tag models"""

    task = models.ForeignKey(
        Task, related_name="tags", on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        Tag, related_name="users", on_delete=models.CASCADE
    )


class Comment(models.Model):
    """Comment model"""

    task = models.ForeignKey(
        Task, related_name="comments", on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User, related_name="comments", on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class UserTask(models.Model):
    """Many-to-many relationship between User and Task models"""

    user = models.ForeignKey(
        User, related_name="tasks", on_delete=models.CASCADE
    )
    task = models.ForeignKey(
        Task, related_name="users", on_delete=models.CASCADE
    )
