from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum
from datetime import datetime, timedelta
from .models import *
from .emotion_detector import get_emotion_detector
from .chatbot import get_chatbot
import json

# Create your views here.
def home(request):

    return render(request , 'index.html')

def login_view(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request , password = password , username = username)

        if user:
            login(request , user)
            return redirect('landing')
        else:
            messages.error(request , "Invalid Credentials")
            return redirect('login')

    
    return render(request , 'login.html')

def register(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username = username).exists():
            messages.error(request , "Username Taken")
            return redirect('register')
        
        
        elif User.objects.filter(email = email).exists():
            messages.error(request , "Email Taken")
            return redirect('register')

        user = User.objects.create(
            username = username, 
            email = email
        )

        user.set_password(password)
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')


    return render(request , 'register.html')


def landing(request):
    return render(request , 'landing.html')



@login_required
def journal(request):
    if request.method == "POST":
        text = request.POST.get('j')

        Journal.objects.create(
            user=request.user,
            text=text
        )

        messages.success(request, 'Journal Submitted')
        return redirect('journal')

    journals = Journal.objects.filter(user=request.user).order_by('-date')
    return render(request, 'journal.html', {'journals': journals})


@login_required
def chatbot_view(request):
    """Main chatbot interface"""
    messages_list = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    return render(request, 'chatbot.html', {'messages': messages_list})


@login_required
def send_message(request):
    """Handle chatbot message sending via AJAX"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_text = data.get('message', '').strip()
            
            if not user_text:
                return JsonResponse({'error': 'Empty message'}, status=400)
            
            # Detect emotion
            detector = get_emotion_detector()
            emotion, confidence, sentiment = detector.predict(user_text)
            
            # Save user message
            user_msg = ChatMessage.objects.create(
                user=request.user,
                text=user_text,
                sender='USER',
                emotion=emotion,
                emotion_score=confidence
            )
            
            # Get conversation history
            history = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')[:20]
            conversation_history = [(msg.sender, msg.text) for msg in reversed(history)]
            
            # Get bot response
            chatbot = get_chatbot()
            bot_response = chatbot.get_response(user_text, emotion, conversation_history)
            
            # Save bot message
            bot_msg = ChatMessage.objects.create(
                user=request.user,
                text=bot_response,
                sender='BOT'
            )
            
            # Update emotion timeline
            update_emotion_timeline(request.user, sentiment, confidence)
            
            return JsonResponse({
                'user_message': {
                    'text': user_text,
                    'emotion': emotion,
                    'confidence': round(confidence * 100, 1),
                    'timestamp': user_msg.timestamp.strftime('%I:%M %p')
                },
                'bot_message': {
                    'text': bot_response,
                    'timestamp': bot_msg.timestamp.strftime('%I:%M %p')
                }
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)


def update_emotion_timeline(user, sentiment, confidence):
    """Update daily emotion timeline"""
    today = datetime.now().date()
    timeline, created = EmotionTimeline.objects.get_or_create(
        user=user,
        date=today,
        defaults={
            'positive_score': 0.0,
            'negative_score': 0.0,
            'neutral_score': 0.0,
            'message_count': 0
        }
    )
    
    # Update scores
    if sentiment == 'positive':
        timeline.positive_score += confidence
    elif sentiment == 'negative':
        timeline.negative_score += confidence
    else:
        timeline.neutral_score += confidence
    
    timeline.message_count += 1
    timeline.save()


@login_required
def dashboard(request):
    """Emotion dashboard with timeline graph"""
    return render(request, 'dashboard.html')


@login_required
def get_emotion_data(request):
    """API endpoint for emotion timeline data with hardcoded fake data for Feb 1-23, 2026"""
    import random
    
    days = int(request.GET.get('days', 7))
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days-1)
    
    # Get real data from database
    timeline_data = EmotionTimeline.objects.filter(
        user=request.user,
        date__gte=start_date,
        date__lte=end_date
    ).order_by('date')
    
    # Convert to dict for easier manipulation
    existing_data = {entry.date: entry for entry in timeline_data}
    
    # Add hardcoded fake data for Feb 1-23, 2026 if no real data exists
    fake_data_start = datetime(2026, 2, 1).date()
    fake_data_end = datetime(2026, 2, 23).date()
    
    # Generate fake data for dates that don't have real data
    current_fake_date = fake_data_start
    while current_fake_date <= fake_data_end:
        # Only add if date is in requested range and doesn't have real data
        if current_fake_date >= start_date and current_fake_date <= end_date:
            if current_fake_date not in existing_data:
                # Generate realistic fake data
                day_of_week = current_fake_date.weekday()
                
                # Skip some days randomly (15% chance to skip)
                if random.random() > 0.15:
                    # Weekends tend to be more positive
                    if day_of_week >= 5:
                        positive_base = random.uniform(0.6, 0.9)
                        negative_base = random.uniform(0.1, 0.3)
                    else:
                        positive_base = random.uniform(0.4, 0.7)
                        negative_base = random.uniform(0.2, 0.5)
                    
                    neutral_base = random.uniform(0.2, 0.4)
                    message_count = random.randint(3, 15)
                    
                    positive_score = positive_base * message_count * random.uniform(0.8, 1.2)
                    negative_score = negative_base * message_count * random.uniform(0.8, 1.2)
                    neutral_score = neutral_base * message_count * random.uniform(0.8, 1.2)
                    
                    # Create fake entry object (not saved to DB)
                    class FakeEntry:
                        def __init__(self, date, pos, neg, neu, count):
                            self.date = date
                            self.positive_score = pos
                            self.negative_score = neg
                            self.neutral_score = neu
                            self.message_count = count
                    
                    existing_data[current_fake_date] = FakeEntry(
                        current_fake_date,
                        round(positive_score, 2),
                        round(negative_score, 2),
                        round(neutral_score, 2),
                        message_count
                    )
        
        current_fake_date += timedelta(days=1)
    
    # Sort by date and build response
    sorted_dates = sorted(existing_data.keys())
    data = []
    
    for date in sorted_dates:
        entry = existing_data[date]
        if entry.message_count > 0:
            # Calculate average percentages
            total = entry.positive_score + entry.negative_score + entry.neutral_score
            if total > 0:
                pos_pct = (entry.positive_score / total) * 100
                neg_pct = (entry.negative_score / total) * 100
                neu_pct = (entry.neutral_score / total) * 100
                
                # Overall sentiment score (-100 to +100)
                sentiment_score = pos_pct - neg_pct
                
                data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'sentiment_score': round(sentiment_score, 2),
                    'positive': round(pos_pct, 1),
                    'negative': round(neg_pct, 1),
                    'neutral': round(neu_pct, 1),
                    'message_count': entry.message_count
                })
    
    return JsonResponse({'data': data})
