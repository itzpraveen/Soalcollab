from django.db import models
from django.utils import timezone

class Client(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    class Status(models.TextChoices):
        INBOX = 'inbox', 'Inbox'
        BRIEF_READY = 'brief_ready', 'Brief Ready'
        IN_DESIGN = 'in_design', 'In Design'
        REVIEW = 'review', 'Review'
        SENT = 'sent', 'Sent'
        DONE = 'done', 'Done'

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INBOX)
    internal_due = models.DateField(null=True, blank=True)
    client_due = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        return self.client_due and self.client_due < timezone.now().date() and not self.completed_at

    @property
    def is_due_today(self):
        return self.client_due and self.client_due == timezone.now().date() and not self.completed_at

    @property
    def card_color(self):
        today = timezone.now().date()
        if self.status == self.Status.DONE:
            return 'green'
        if self.client_due and self.client_due < today:
            return 'red'
        if self.client_due and self.client_due == today:
            return 'red'
        if self.internal_due and self.internal_due <= today:
            return 'yellow'
        return 'green'

class Attachment(models.Model):
    file = models.FileField(upload_to='attachments/')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')

    def __str__(self):
        return self.file.name
