# 📚 BookKeeper - Social Book Catalog

A modern web application built with Flask that allows users to create, share, and discover books in a social community environment. Users can maintain their personal library while browsing and interacting with books shared by the entire community.

## ✨ Features

### 🔐 User Authentication
- Secure user registration and login system
- Password hashing with Werkzeug's PBKDF2
- Session management with Flask-Login
- User profile management

### 📖 Book Management
- Add books with detailed information (title, author, genre, year, ISBN, description)
- Upload custom book cover images with automatic resizing
- Default book cover generation for books without images
- Edit and delete your own books
- Star rating system (1-5 stars)

### 🌐 Social Features
- **Public Book Catalog**: Browse all books shared by community members
- **Like System**: Like/unlike books with real-time updates
- **Comment System**: Add, view, and delete comments on books
- **User Attribution**: See who shared each book
- **My Library**: Personal collection view for your own books

### 🔍 Advanced Search & Filtering
- Search books by title, author, or description
- Filter by genre
- Sort by newest, most liked, title, author, or rating
- Real-time filtering and search

### 📱 Responsive Design
- Modern Bootstrap 5 interface
- Mobile-friendly responsive design
- Smooth animations and transitions
- Font Awesome icons
- Dark/light theme support

### 🎨 User Experience
- Intuitive navigation with clear separation between public catalog and personal library
- Interactive book cards with hover effects
- Real-time like and comment updates
- Guest browsing (view-only for non-authenticated users)
- Keyboard shortcuts for power users

## 🛠️ Technology Stack

- **Backend**: Flask 3.0.0, Python 3.13+
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Flask-Login with secure password hashing
- **Frontend**: Bootstrap 5, Font Awesome, Vanilla JavaScript
- **Image Processing**: Pillow (PIL) for cover image handling
- **File Upload**: Secure file handling with validation

## 📋 Prerequisites

- Python 3.13 or higher
- pip (Python package installer)

## 🚀 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/BookKeeper.git
   cd BookKeeper
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv bookkeeper_env
   
   # On macOS/Linux:
   source bookkeeper_env/bin/activate
   
   # On Windows:
   bookkeeper_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the database**
   ```bash
   python -c "from app import app, db; 
   with app.app_context(): 
       db.create_all()
       print('Database initialized successfully!')"
   ```

5. **Create uploads directory**
   ```bash
   mkdir -p static/uploads
   ```

6. **Run the application**
   ```bash
   python app.py
   ```

7. **Access the application**
   Open your browser and navigate to `http://127.0.0.1:5000`

## 📁 Project Structure

```
BookKeeper/
├── app.py                 # Main Flask application
├── models.py             # Database models (User, Book, Like, Comment)
├── requirements.txt      # Python dependencies
├── bookkeeper.db        # SQLite database (auto-generated)
├── static/
│   ├── css/
│   │   └── style.css    # Custom styles
│   ├── js/
│   │   └── main.js      # Custom JavaScript
│   └── uploads/         # Book cover images
│       └── default_book.png
└── templates/           # HTML templates
    ├── base.html        # Base template
    ├── index.html       # Public book catalog
    ├── dashboard.html   # Personal library
    ├── login.html       # Login page
    ├── register.html    # Registration page
    ├── profile.html     # User profile
    ├── add_book.html    # Add/edit book form
    └── view_book.html   # Book details with comments
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```bash
SECRET_KEY=your-super-secret-key-here
DATABASE_URL=sqlite:///bookkeeper.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216  # 16MB
```

### Security Notes
- Change the `SECRET_KEY` in production
- Use a more robust database (PostgreSQL) for production
- Implement HTTPS in production
- Add rate limiting for API endpoints
- Validate and sanitize all user inputs

## 📊 Database Schema

### User Model
- id, username, email, password_hash
- One-to-many relationship with books
- Many-to-many relationships with likes and comments

### Book Model
- id, title, author, genre, year, isbn, description, rating
- cover_image, user_id, created_at, updated_at
- Relationships with likes and comments

### Like Model
- id, user_id, book_id, created_at
- Unique constraint on user_id + book_id

### Comment Model
- id, content, user_id, book_id, created_at
- Cascade delete when user or book is deleted

## 🎯 Usage

### For Regular Users
1. **Register/Login**: Create an account to start using social features
2. **Browse Books**: Explore the public catalog on the homepage
3. **Add Books**: Share your favorite books with the community
4. **Interact**: Like and comment on books you enjoy
5. **Manage Library**: View and organize your personal collection

### For Guests
- Browse the public book catalog
- View book details and existing comments
- Access registration to join the community

## 🚧 Future Enhancements

- [ ] Book recommendations based on user preferences
- [ ] User following system
- [ ] Book reading status (want to read, currently reading, read)
- [ ] Book import from external APIs (Google Books, Goodreads)
- [ ] Advanced search with filters (publication date, page count)
- [ ] Book collections/shelves
- [ ] Export personal library
- [ ] Email notifications for new comments/likes
- [ ] Admin panel for content moderation
- [ ] Mobile app (React Native/Flutter)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask team for the excellent web framework
- Bootstrap team for the responsive CSS framework
- Font Awesome for the beautiful icons
- SQLAlchemy team for the powerful ORM
- Pillow team for image processing capabilities

## 📧 Contact

Your Name - your.email@example.com

Project Link: [https://github.com/yourusername/BookKeeper](https://github.com/yourusername/BookKeeper)

---

**Built with ❤️ and ☕ by [Your Name]**
- **Session Management**: Stay logged in with "Remember Me" functionality
- **User Profiles**: View your reading statistics and account information

### 📖 Book Management (CRUD)
- **Add Books**: Upload cover images, add detailed information including:
  - Title, Author, Genre, Description
  - Publication Year, ISBN, Personal Rating
  - Custom genres support
- **View Books**: Beautiful card-based layout with cover images
- **Edit Books**: Update any book information including cover images
- **Delete Books**: Remove books from your collection

### 🔍 Advanced Search & Filtering
- **Real-time Search**: Search by title, author, or description
- **Genre Filtering**: Filter books by genre
- **Sorting Options**: Sort by newest, title, author, or rating
- **Search Suggestions**: Auto-complete based on your library

### 📊 Dashboard & Analytics
- **Personal Dashboard**: Overview of your entire collection
- **Reading Statistics**: Track your favorite genres and reading habits
- **Recent Books**: Quick access to recently added books
- **Export Functionality**: Export your library as JSON or CSV

### 🎨 Modern UI/UX
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- **Bootstrap 5**: Modern, clean interface with smooth animations
- **Dark Mode Ready**: Prepared for future dark theme implementation
- **Accessibility**: Built with accessibility best practices

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
```bash
git clone <repository-url>
cd BookKeeper
```

2. **Create a virtual environment (recommended)**
```bash
python -m venv bookkeeper_env
source bookkeeper_env/bin/activate  # On Windows: bookkeeper_env\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Open your browser**
Navigate to `http://localhost:5000`

### First Time Setup
1. Register a new account or use demo credentials:
   - Username: `demo`
   - Password: `demo123`
2. Start adding books to your collection!

## 📁 Project Structure

```
BookKeeper/
├── app.py                 # Main Flask application
├── models.py              # Database models (User, Book)
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Landing page
│   ├── register.html     # User registration
│   ├── login.html        # User login
│   ├── dashboard.html    # Main dashboard
│   ├── add_book.html     # Add new book
│   ├── view_book.html    # View book details
│   ├── edit_book.html    # Edit book
│   └── profile.html      # User profile
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Custom CSS
│   ├── js/
│   │   └── main.js       # Custom JavaScript
│   └── uploads/          # Book cover images
└── bookkeeper.db         # SQLite database (created automatically)
```

## 🎯 Key Features Explained

### Book Management
- **Cover Images**: Upload and automatically resize book covers
- **Rich Metadata**: Store comprehensive book information
- **Personal Ratings**: Rate books from 1-5 stars
- **Custom Genres**: Add your own genres beyond the predefined list

### Search & Discovery
- **Instant Search**: Real-time filtering as you type
- **Multiple Filters**: Combine search with genre and sorting
- **Smart Suggestions**: Search autocomplete based on your books

### User Experience
- **Responsive Design**: Optimized for all device sizes
- **Fast Loading**: Efficient image loading and caching
- **Keyboard Shortcuts**: 
  - `Ctrl+K`: Focus search
  - `Ctrl+N`: Add new book
  - `Ctrl+D`: Go to dashboard
  - `Escape`: Clear search/close modals

## 🛠️ Technical Details

### Backend
- **Flask**: Lightweight Python web framework
- **SQLAlchemy**: Database ORM for easy data management
- **Flask-Login**: User session management
- **SQLite**: File-based database (easy to deploy)
- **Pillow**: Image processing for cover photos

### Frontend
- **Bootstrap 5**: Modern CSS framework
- **Font Awesome**: Beautiful icons
- **Vanilla JavaScript**: No heavy frameworks, fast loading
- **Progressive Enhancement**: Works without JavaScript

### Security
- **Password Hashing**: Secure password storage with Werkzeug
- **CSRF Protection**: Built-in form security
- **Session Management**: Secure user sessions
- **File Upload Validation**: Safe image upload handling

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production:
```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DATABASE_URL=sqlite:///bookkeeper.db
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### Database
The app uses SQLite by default, which creates a file-based database. For production, you can easily switch to PostgreSQL or MySQL by changing the `SQLALCHEMY_DATABASE_URI`.

## 📱 Mobile Support

BookKeeper is fully responsive and works great on:
- 📱 Mobile phones (iOS/Android)
- 📱 Tablets (iPad/Android tablets)
- 💻 Desktop computers
- 💻 Laptops

## 🎨 Customization

### Themes
The application is built with CSS custom properties, making it easy to customize:
- Colors: Modify the `:root` variables in `static/css/style.css`
- Layout: Adjust Bootstrap classes in templates
- Fonts: Change font families in CSS

### Adding Features
The modular structure makes it easy to add new features:
- Add new routes in `app.py`
- Create new templates in `templates/`
- Extend models in `models.py`

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production (Basic)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Production (with environment)
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set up a reverse proxy (Nginx)
4. Use a production database (PostgreSQL)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [Flask](https://flask.palletsprojects.com/)
- UI powered by [Bootstrap](https://getbootstrap.com/)
- Icons from [Font Awesome](https://fontawesome.com/)
- Image processing by [Pillow](https://pillow.readthedocs.io/)

## 📞 Support

If you encounter any issues or have questions:
1. Check the existing issues
2. Create a new issue with detailed information
3. Include steps to reproduce any bugs

---

**Happy Reading! 📚**

Start organizing your personal library today with BookKeeper!
