from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from .models import Task, Client as ProjectClient


class TaskModelTests(TestCase):
    def setUp(self):
        self.client_obj = ProjectClient.objects.create(name="ACME", email="acme@example.com")

    def test_completed_timestamp_set_when_done(self):
        task = Task.objects.create(title="T1", client=self.client_obj, status=Task.Status.DONE)
        self.assertIsNotNone(task.completed_at)
        self.assertLessEqual(task.completed_at, timezone.now())

    def test_completed_timestamp_cleared_when_not_done(self):
        task = Task.objects.create(title="T2", client=self.client_obj, status=Task.Status.DONE)
        task.status = Task.Status.REVIEW
        task.save()
        self.assertIsNone(task.completed_at)


class UpdateTaskStatusTests(TestCase):
    def setUp(self):
        self.client_obj = ProjectClient.objects.create(name="ACME", email="acme@example.com")
        self.task = Task.objects.create(title="T1", client=self.client_obj, status=Task.Status.BRIEF_READY)
        self.client = Client()

    def test_move_task_to_new_status(self):
        response = self.client.post(
            reverse("update_task_status"),
            {"task_updates": f"{{\"{self.task.id}\": \"{Task.Status.REVIEW}\"}}"},
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.REVIEW)

    def test_move_task_to_inbox_is_ignored(self):
        response = self.client.post(
            reverse("update_task_status"),
            {"task_updates": f"{{\"{self.task.id}\": \"{Task.Status.INBOX}\"}}"},
        )
        self.assertEqual(response.status_code, 200)
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.status, Task.Status.INBOX)
