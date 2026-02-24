from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from User.models import EmotionTimeline
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate fake emotion data before Feb 24, 2026'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username to add data for')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User "{username}" does not exist'))
            return

        # Generate data from Jan 1, 2026 to Feb 23, 2026
        end_date = datetime(2026, 2, 23).date()
        start_date = datetime(2026, 1, 1).date()
        
        current_date = start_date
        created_count = 0
        
        while current_date <= end_date:
            # Skip some days randomly to make it realistic
            if random.random() > 0.15:  # 85% chance of having data
                # Generate realistic emotion scores
                # Simulate different patterns
                day_of_week = current_date.weekday()
                
                # Weekends tend to be more positive
                if day_of_week >= 5:
                    positive_base = random.uniform(0.6, 0.9)
                    negative_base = random.uniform(0.1, 0.3)
                else:
                    positive_base = random.uniform(0.4, 0.7)
                    negative_base = random.uniform(0.2, 0.5)
                
                neutral_base = random.uniform(0.2, 0.4)
                
                # Random number of messages per day (3-15)
                message_count = random.randint(3, 15)
                
                # Calculate scores (sum of confidences)
                positive_score = positive_base * message_count * random.uniform(0.8, 1.2)
                negative_score = negative_base * message_count * random.uniform(0.8, 1.2)
                neutral_score = neutral_base * message_count * random.uniform(0.8, 1.2)
                
                # Create or update timeline entry
                EmotionTimeline.objects.update_or_create(
                    user=user,
                    date=current_date,
                    defaults={
                        'positive_score': round(positive_score, 2),
                        'negative_score': round(negative_score, 2),
                        'neutral_score': round(neutral_score, 2),
                        'message_count': message_count
                    }
                )
                created_count += 1
            
            current_date += timedelta(days=1)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {created_count} emotion timeline entries for user "{username}"'
            )
        )
