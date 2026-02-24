# MindSpace - Emotional Wellness Platform

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**An AI-powered emotional wellness platform combining conversational therapy, emotion detection, and data-driven insights.**

[Features](#features) • [Demo](#demo) • [Installation](#installation) • [Usage](#usage) • [Team](#team)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Demo](#demo)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Team](#team)
- [Contributing](#contributing)
- [License](#license)

---

## 🌟 Overview

MindSpace is a comprehensive emotional wellness platform that provides:
- **24/7 AI Therapy Chat**: Empathetic conversations with an AI therapist
- **Emotion Detection**: Real-time emotion analysis using BERT
- **Visual Analytics**: Track emotional patterns over time
- **Private Journal**: Personal space for self-reflection

The platform addresses the growing need for accessible mental health support by leveraging cutting-edge AI technology to provide immediate, private, and cost-free emotional assistance.

---

## ✨ Features

### 🤖 AI Therapy Chatbot
- Powered by LangChain + Groq (LLaMA 3.3 70B)
- Context-aware, empathetic responses
- Conversation history maintained
- Emotion-informed dialogue

### 🎭 Emotion Detection
- BERT-based emotion classification
- Real-time analysis of user messages
- 87% accuracy on test dataset
- Three emotion categories: Positive, Negative, Neutral

### 📊 Interactive Dashboard
- Sentiment timeline visualization
- Adjustable time range (7-90 days)
- Statistics cards (avg sentiment, total messages, positive days)
- Hover tooltips with emotion breakdown
- Automatic demo data for new users

### 📔 Personal Journal
- Private journaling space
- Chronological entry display
- Date-stamped entries
- Separate from chat conversations

### 🎨 Professional UI
- Clean, modern design
- Consistent design system
- Responsive layouts
- Accessible and user-friendly

---

## 🎬 Demo

### Screenshots

**Home Page**
```
Professional landing page with feature overview and CTAs
```

**Chatbot Interface**
```
Real-time chat with emotion badges (Positive/Negative/Neutral)
```

**Emotion Dashboard**
```
Interactive timeline graph showing sentiment trends over time
```

**Journal**
```
Clean interface for writing and viewing past entries
```

---

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2
- **Database**: SQLite (dev), PostgreSQL (production recommended)
- **AI/ML**: 
  - Transformers (BERT emotion detection)
  - PyTorch (model inference)
  - LangChain (LLM orchestration)
  - Groq API (LLaMA 3.3 70B)

### Frontend
- **Core**: HTML5, CSS3, JavaScript (ES6+)
- **Visualization**: Chart.js
- **Design**: Custom CSS (no frameworks)

### Data
- **Dataset**: GoEmotions (58,000+ labeled comments)
- **Model**: Fine-tuned BERT (bert-base-uncased)

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/mindspace.git
cd mindspace/SIC
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Environment Configuration
Create a `.env` file in the `SIC` directory:
```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your Groq API key from: [https://console.groq.com/](https://console.groq.com/)

### Step 4: Database Setup
```bash
python manage.py migrate
```

### Step 5: Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server
```bash
python manage.py runserver
```

Visit: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 📖 Usage

### Quick Start

1. **Register Account**
   - Navigate to `/register/`
   - Create your account
   - Login with credentials

2. **Start Chatting**
   - Go to "Therapy Chat"
   - Type your message
   - See emotion detection in real-time
   - Get empathetic AI responses

3. **View Dashboard**
   - Navigate to "Emotion Dashboard"
   - See 23 days of demo data (Feb 1-23, 2026)
   - Adjust time range with slider
   - Hover over points for details

4. **Write Journal**
   - Go to "Personal Journal"
   - Write your thoughts
   - View past entries

### Example Interactions

**Positive Message:**
```
User: "I'm feeling great today! Everything is going well."
Emotion: Positive (85%)
Bot: "That's wonderful to hear! It sounds like you're in a really good place..."
```

**Negative Message:**
```
User: "I'm worried about my exam tomorrow."
Emotion: Negative (78%)
Bot: "I understand that exams can be stressful. It's natural to feel anxious..."
```

**Neutral Message:**
```
User: "Just a normal day, nothing special."
Emotion: Neutral (92%)
Bot: "Sometimes the ordinary days are just as important..."
```

---

## 📁 Project Structure

```
SIC/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
├── db.sqlite3               # SQLite database
│
├── SIC/                     # Main project directory
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
│
├── User/                    # Main application
│   ├── models.py            # Database models
│   ├── views.py             # View functions
│   ├── admin.py             # Admin configuration
│   ├── emotion_detector.py  # BERT emotion detection
│   ├── chatbot.py           # LangChain chatbot
│   │
│   ├── templates/           # HTML templates
│   │   ├── index.html       # Home page
│   │   ├── login.html       # Login page
│   │   ├── register.html    # Registration page
│   │   ├── landing.html     # User dashboard
│   │   ├── chatbot.html     # Chat interface
│   │   ├── dashboard.html   # Analytics dashboard
│   │   └── journal.html     # Journal interface
│   │
│   └── management/commands/ # Custom commands
│       └── populate_fake_data.py
│
├── model/                   # Emotion detection model
│   └── emotion_model_final/
│       ├── config.json
│       ├── model.safetensors
│       ├── tokenizer.json
│       └── tokenizer_config.json
│
└── docs/                    # Documentation
    ├── QUICK_START.md
    ├── CHANGES.md
    ├── UI_IMPROVEMENTS.md
    ├── FINAL_GUIDE.md
    └── PROJECT_REPORT.txt
```

---

## 🔌 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /register/
Content-Type: application/x-www-form-urlencoded

username=johndoe&email=john@example.com&password=securepass123
```

#### Login
```http
POST /login/
Content-Type: application/x-www-form-urlencoded

username=johndoe&password=securepass123
```

### Chatbot Endpoints

#### Send Message
```http
POST /api/send-message/
Content-Type: application/json
Authorization: Session

{
  "message": "I'm feeling happy today!"
}
```

**Response:**
```json
{
  "user_message": {
    "text": "I'm feeling happy today!",
    "emotion": "Positive",
    "confidence": 85.3,
    "timestamp": "2:30 PM"
  },
  "bot_message": {
    "text": "That's wonderful to hear! ...",
    "timestamp": "2:30 PM"
  }
}
```

### Dashboard Endpoints

#### Get Emotion Data
```http
GET /api/emotion-data/?days=30
Authorization: Session
```

**Response:**
```json
{
  "data": [
    {
      "date": "2026-02-01",
      "sentiment_score": 45.2,
      "positive": 65.5,
      "negative": 20.3,
      "neutral": 14.2,
      "message_count": 8
    },
    ...
  ]
}
```

### Journal Endpoints

#### Create Journal Entry
```http
POST /journal/
Content-Type: application/x-www-form-urlencoded
Authorization: Session

j=Today was a good day. I accomplished a lot.
```

---

## 👥 Team

### Development Team

| Name | Role | Responsibilities |
|------|------|-----------------|
| **Yash** | Data Scientist | Data cleaning, EDA, visualization |
| **Sarthak** | ML Engineer | Model training, optimization, deployment |
| **Liesha** | AI Engineer | LLM integration, prompt engineering |
| **Pakhi** | UI/UX Designer | Interface design, user experience |
| **Shreyansh** | Backend Developer | Django development, API design |

### Contact

For questions or support, please contact:
- Email: support@mindspace.app
- GitHub Issues: [Create an issue](https://github.com/yourusername/mindspace/issues)

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide for Python code
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed

---

## 📊 Model Performance

### Emotion Detection Model

- **Architecture**: BERT (bert-base-uncased)
- **Training Data**: GoEmotions (58,000+ samples)
- **Test Accuracy**: 87.3%
- **Macro F1-Score**: 0.78
- **Inference Time**: ~50ms per message (CPU)
- **Model Size**: 420MB

### Emotion Categories

| Category | Examples | Color |
|----------|----------|-------|
| Positive | Joy, excitement, gratitude | Green |
| Negative | Anger, sadness, fear | Red |
| Neutral | Calm, neutral, confusion | Gray |

---

## 🔒 Privacy & Security

- All conversations are private and encrypted
- No data sharing with third parties
- User data stored securely in database
- CSRF protection on all forms
- Password hashing with Django's built-in system
- Session-based authentication

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Google Research** for the GoEmotions dataset
- **Hugging Face** for Transformers library
- **Groq** for LLM API access
- **Django** community for excellent documentation
- **Chart.js** for visualization library

---

