# ActiScore - AI-Powered Emotion Analysis & Learning Platform

ActiScore is a comprehensive AI platform that combines multimodal emotion analysis (facial + speech) with intelligent learning tools. Built with Flask, it provides a modern web interface for emotion detection, document summarization, research recommendations, and more.

## 🚀 Features

### Core AI Features
- **Multimodal Emotion Analysis**: Analyze emotions from facial expressions and speech patterns
- **Legal Document Summarizer**: AI-powered legal document analysis and summarization
- **Research Paper Recommender**: Intelligent research paper discovery and recommendations
- **Video Summarizer**: Automatic transcription and summarization of educational videos
- **Startup Success Predictor**: ML-based prediction of startup success probability
- **Knowledge Graph Visualization**: Interactive visualization of research relationships
- **IntelliChat**: RAG-powered chatbot for intelligent assistance
- **AI Attendance Monitoring**: Camera-based attendance with emotion analytics

### Technical Features
- **Modern UI/UX**: Responsive design with 3D animations using Three.js
- **User Authentication**: Secure login system with role-based access (user/admin)
- **File Upload**: Support for videos, documents, and audio files
- **Real-time Processing**: Asynchronous task processing with progress tracking
- **Analytics Dashboard**: Comprehensive analytics and reporting
- **Admin Panel**: User management, content moderation, and system monitoring
- **Docker Support**: Containerized deployment with docker-compose

## 🛠️ Technology Stack

### Backend
- **Python 3.9+** with Flask framework
- **SQLAlchemy** for database ORM
- **Flask-Login** for authentication
- **Flask-Migrate** for database migrations
- **Celery** for background task processing
- **Redis** for task queue and caching

### Frontend
- **HTML5** with TailwindCSS for styling
- **JavaScript** with Three.js for 3D animations
- **Chart.js** for data visualization
- **Alpine.js** for interactive components

### Machine Learning
- **TensorFlow/Keras** for deep learning models
- **PyTorch** for additional ML capabilities
- **OpenCV** for computer vision tasks
- **MediaPipe** for face detection and analysis
- **Librosa** for audio processing
- **Transformers** (Hugging Face) for NLP tasks
- **FAISS** for vector similarity search

### Database
- **PostgreSQL** (primary) with SQLite fallback
- **Vector embeddings** support for semantic search

## 📦 Installation

### Prerequisites
- Python 3.9+
- Node.js (for frontend build tools)
- FFmpeg (for video processing)
- Redis (for task queue)
- PostgreSQL (optional, SQLite included)

### Local Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd actiscore
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   flask db upgrade
   python scripts/seed_db.py
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

### Docker Setup

1. **Using Docker Compose (Recommended)**
   ```bash
   docker-compose up --build
   ```

2. **Individual Docker containers**
   ```bash
   # Build and run the web application
   docker build -t actiscore .
   docker run -p 5000:5000 actiscore
   ```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key | `dev-secret-key` |
| `DATABASE_URL` | PostgreSQL connection string | `sqlite:///app.db` |
| `FLASK_CONFIG` | Flask configuration | `development` |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `ADMIN_EMAIL` | Admin user email | `admin@example.com` |
| `ADMIN_PASSWORD` | Admin user password | `admin123` |

### File Upload Settings

- **Maximum file size**: 16MB
- **Allowed video formats**: mp4, avi, mov, mkv, webm
- **Allowed audio formats**: wav, mp3, flac, aac, m4a
- **Allowed document formats**: pdf, txt, doc, docx

## 🎯 Usage

### Default Credentials
- **Admin**: `admin@example.com` / `admin123`
- **Demo User**: `john@example.com` / `password123`

### Key Features Usage

1. **Multimodal Emotion Analysis**
   - Upload a video file (MP4, AVI, MOV, etc.)
   - System processes facial expressions and speech
   - View timeline of detected emotions with confidence scores
   - Download results as CSV or JSON

2. **Legal Document Summarizer**
   - Upload PDF or text documents
   - Get AI-generated summaries
   - Ask questions about the document content
   - Export summaries in various formats

3. **Research Paper Recommender**
   - Enter research topics or keywords
   - Get semantically similar papers
   - View paper abstracts and citations
   - Save papers to your library

4. **Video Summarizer**
   - Upload educational videos
   - Automatic transcription using Whisper
   - AI-generated summaries of key points
   - Timeline visualization of topics

5. **Startup Success Predictor**
   - Input startup characteristics
   - Get success probability score
   - Receive risk assessment
   - Get personalized recommendations

## 🧪 Model Training

### Emotion Recognition Models

The platform uses pre-trained models for emotion recognition:

1. **FER Model**: Facial Emotion Recognition
   - Based on FER2013 dataset
   - 7 emotion categories: angry, disgust, fear, happy, sad, surprise, neutral
   - CNN architecture with transfer learning

2. **SER Model**: Speech Emotion Recognition
   - Trained on RAVDESS and CREMA-D datasets
   - Extracts MFCC, pitch, and prosodic features
   - SVM and neural network classifiers

3. **Fusion Model**: Combines FER and SER results
   - Late fusion approach
   - Weighted ensemble method
   - Confidence-based decision making

### Training Your Own Models

1. **Prepare datasets** in the `Dataset/` folder
2. **Run training scripts** (to be implemented)
3. **Update model paths** in configuration
4. **Test model performance**

## 📊 API Documentation

### Authentication
All API endpoints require authentication via Flask-Login session.

### Key Endpoints

#### Video Processing
- `POST /api/upload/video` - Upload video file
- `GET /api/processing/status/<task_id>` - Check processing status
- `GET /actiscore/results/<video_id>` - Get emotion analysis results

#### Document Processing
- `POST /api/upload/document` - Upload document
- `POST /ai/summarize-legal-document` - Summarize legal document
- `POST /ai/recommend-papers` - Get paper recommendations

#### User Management
- `GET /api/user/stats` - Get user statistics
- `GET /admin/users` - List users (admin only)
- `POST /admin/users/<id>/toggle-status` - Toggle user status

## 🚀 Deployment

### Production Deployment

1. **Set production environment variables**
   ```bash
   export FLASK_CONFIG=production
   export SECRET_KEY=your-secret-key-here
   export DATABASE_URL=postgresql://user:pass@host/db
   ```

2. **Use production WSGI server**
   ```bash
   gunicorn --bind 0.0.0.0:5000 --workers 4 run:app
   ```

3. **Set up reverse proxy** (Nginx/Apache)
4. **Configure SSL/TLS certificates**
5. **Set up monitoring and logging**

### Cloud Deployment

#### Heroku
```bash
# Create Heroku app
heroku create actiscore-app

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_CONFIG=production

# Deploy
git push heroku main
```

#### AWS/GCP/Azure
- Use containerized deployment with Docker
- Set up managed databases (RDS, Cloud SQL, etc.)
- Configure load balancers and auto-scaling
- Set up monitoring with CloudWatch/Stackdriver

## 🔒 Security

### Security Features
- **Password hashing** with Werkzeug/bcrypt
- **CSRF protection** on all forms
- **Input validation** and sanitization
- **File upload security** with type validation
- **Rate limiting** on API endpoints
- **Secure headers** with Flask-Talisman

### Best Practices
- Keep dependencies updated
- Use environment variables for secrets
- Implement proper logging and monitoring
- Regular security audits
- Use HTTPS in production
- Implement proper backup strategies

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

### Test Structure
```
tests/
├── test_auth.py          # Authentication tests
├── test_api.py           # API endpoint tests
├── test_models.py        # Database model tests
├── test_integration.py   # Integration tests
└── fixtures/            # Test data fixtures
```

## 📈 Monitoring & Logging

### Logging Configuration
- Application logs: `logs/app.log`
- Error logs: `logs/error.log`
- Access logs: `logs/access.log`
- ML processing logs: `logs/ml.log`

### Health Checks
- Application health: `/api/health`
- Database connectivity check
- Model loading status
- External service availability

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and add tests
4. Run tests: `pytest`
5. Commit changes: `git commit -am 'Add feature'`
6. Push to branch: `git push origin feature-name`
7. Create Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use Black for code formatting
- Add docstrings to functions
- Write comprehensive tests
- Update documentation

## 📚 Documentation

### Additional Documentation
- [API Reference](docs/api.md)
- [Model Training Guide](docs/training.md)
- [Deployment Guide](docs/deployment.md)
- [Contributing Guidelines](docs/contributing.md)

## 🐛 Troubleshooting

### Common Issues

1. **Model Loading Errors**
   - Ensure model files are in the correct directory
   - Check model compatibility with TensorFlow/PyTorch versions
   - Verify model file permissions

2. **Database Connection Issues**
   - Check PostgreSQL service status
   - Verify database credentials
   - Ensure proper network connectivity

3. **File Upload Failures**
   - Check file size limits
   - Verify file type restrictions
   - Ensure sufficient disk space

4. **Memory Issues**
   - Reduce batch sizes for large files
   - Implement file streaming for large uploads
   - Monitor memory usage during processing

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FER2013 Dataset**: For facial emotion recognition training
- **RAVDESS Dataset**: For speech emotion recognition
- **Hugging Face**: For transformer models and NLP tools
- **OpenCV**: For computer vision capabilities
- **MediaPipe**: For face detection and analysis
- **TailwindCSS**: For modern UI components
- **Three.js**: For 3D animations

## 📞 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Review the troubleshooting guide
- Contact: support@actiscore.com

---

**ActiScore** - Empowering AI-driven emotion analysis and intelligent learning experiences.