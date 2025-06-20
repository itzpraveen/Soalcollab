from django.core.management.base import BaseCommand
from tracker.models import Client, Task

class Command(BaseCommand):
    help = 'Seeds the database with initial data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        
        # Create clients
        client1 = Client.objects.create(name='Client 1', email='client1@example.com')
        client2 = Client.objects.create(name='Client 2', email='client2@example.com')

        # Create tasks
        Task.objects.create(title='Task 1', client=client1, status='inbox')
        Task.objects.create(title='Task 2', client=client1, status='brief_ready')
        Task.objects.create(title='Task 3', client=client2, status='in_design')
        Task.objects.create(title='Task 4', client=client2, status='review')
        Task.objects.create(title='Task 5', client=client1, status='sent')
        Task.objects.create(title='Task 6', client=client2, status='done')

        self.stdout.write(self.style.SUCCESS('Data seeded successfully.'))
