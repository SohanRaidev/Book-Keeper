import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from models import db, User, Book, Like, Comment
import uuid
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import base64
import io

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-this-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookkeeper.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY and GEMINI_API_KEY != 'your_gemini_api_key_here':
    genai.configure(api_key=GEMINI_API_KEY)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Custom template filter to convert newlines to HTML breaks
@app.template_filter('nl2br')
def nl2br_filter(text):
    """Convert newlines to HTML line breaks."""
    if text is None:
        return ''
    return text.replace('\n', '<br>')

# Make the filter available in templates
app.jinja_env.filters['nl2br'] = nl2br_filter
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Allowed file extensions for cover images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_image(image_path, max_size=(400, 600)):
    """Resize image while maintaining aspect ratio"""
    try:
        with Image.open(image_path) as img:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            img.save(image_path, optimize=True, quality=85)
    except Exception as e:
        print(f"Error resizing image: {e}")

def analyze_book_cover_with_gemini(image_path):
    """
    Analyze book cover using Gemini API to extract book information
    Returns dict with title, description, genre, etc.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'your_gemini_api_key_here':
        print("Gemini API key not configured properly")
        return None
    
    try:
        # Read and encode image
        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()
        
        # Configure Gemini 2.0 Flash model (latest and better free tier limits)
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Prepare the enhanced prompt
        prompt = """
        Analyze this book cover image and provide comprehensive book information in JSON format. Use your knowledge to provide accurate details about this book:
        
        {
            "title": "extracted book title from the cover",
            "author": "extracted author name from the cover", 
            "year": "publication year (search your knowledge base for this specific book)",
            "genre": "most appropriate genre from: Fiction, Non-Fiction, Mystery, Romance, Science Fiction, Fantasy, Biography, History, Self-Help, Business, Technology, Health, Travel, Art, Philosophy, Other",
            "rating": "average rating out of 5 stars (e.g., 4.2) based on popular review sites and your knowledge",
            "description": "a detailed 4-6 sentence description that includes: plot summary, main themes, writing style, and what makes this book notable or popular. Make it informative and engaging.",
            "tags": ["tag1", "tag2", "tag3", "tag4", "tag5"] // relevant tags like "romance", "sci-fi", "bestseller", "award-winning", etc.
        }
        
        Instructions:
        1. Extract title and author directly from the cover image
        2. Use your knowledge base to find the publication year, rating, and detailed information about this specific book
        3. Provide a rich, informative description that tells readers what the book is about and why they might want to read it
        4. Include relevant tags that help categorize and discover the book
        5. If you cannot identify the specific book, provide the best estimates based on the cover design and any visible text
        6. For rating, use your knowledge of popular ratings from Goodreads, Amazon, etc.
        """
        
        # Create image part
        image_part = {
            "mime_type": "image/jpeg",
            "data": image_data
        }
        
        # Generate response
        response = model.generate_content([prompt, image_part])
        
        # Parse JSON response
        import json
        response_text = response.text.strip()
        
        # Clean up response text (remove markdown formatting if present)
        if response_text.startswith('```json'):
            response_text = response_text[7:-3]
        elif response_text.startswith('```'):
            response_text = response_text[3:-3]
        
        book_info = json.loads(response_text)
        return book_info
        
    except Exception as e:
        print(f"Error analyzing book cover with Gemini: {e}")
        return None

@app.route('/')
def index():
    # Public catalog - show all books from all users
    search = request.args.get('search', '')
    genre_filter = request.args.get('genre', '')
    sort_by = request.args.get('sort', 'created_at')
    
    # Base query for all books (public)
    query = Book.query
    
    # Apply search filter
    if search:
        query = query.filter(
            (Book.title.contains(search)) |
            (Book.author.contains(search)) |
            (Book.description.contains(search))
        )
    
    # Apply genre filter
    if genre_filter:
        query = query.filter_by(genre=genre_filter)
    
    # Apply sorting
    if sort_by == 'title':
        query = query.order_by(Book.title)
    elif sort_by == 'author':
        query = query.order_by(Book.author)
    elif sort_by == 'likes':
        # Sort by most liked books
        query = query.outerjoin(Like).group_by(Book.id).order_by(db.func.count(Like.id).desc())
    elif sort_by == 'rating':
        query = query.order_by(Book.rating.desc())
    else:  # default to newest first
        query = query.order_by(Book.created_at.desc())
    
    books = query.all()
    
    # Get all unique genres for filter dropdown
    genres = db.session.query(Book.genre).distinct().all()
    genres = [genre[0] for genre in genres]
    
    return render_template('index.html', books=books, genres=genres, 
                         current_search=search, current_genre=genre_filter, current_sort=sort_by)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required!', 'danger')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long!', 'danger')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully!', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # My Library - show only current user's books
    search = request.args.get('search', '')
    genre_filter = request.args.get('genre', '')
    sort_by = request.args.get('sort', 'created_at')
    
    # Base query for current user's books only
    query = Book.query.filter_by(user_id=current_user.id)
    
    # Apply search filter
    if search:
        query = query.filter(
            (Book.title.contains(search)) |
            (Book.author.contains(search)) |
            (Book.description.contains(search))
        )
    
    # Apply genre filter
    if genre_filter:
        query = query.filter_by(genre=genre_filter)
    
    # Apply sorting
    if sort_by == 'title':
        query = query.order_by(Book.title)
    elif sort_by == 'author':
        query = query.order_by(Book.author)
    elif sort_by == 'rating':
        query = query.order_by(Book.rating.desc())
    else:  # default to newest first
        query = query.order_by(Book.created_at.desc())
    
    books = query.all()
    
    # Get all unique genres for filter dropdown (from user's books only)
    genres = db.session.query(Book.genre).filter_by(user_id=current_user.id).distinct().all()
    genres = [genre[0] for genre in genres]
    
    return render_template('dashboard.html', books=books, genres=genres, 
                         current_search=search, current_genre=genre_filter, current_sort=sort_by)

@app.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        description = request.form['description']
        year = request.form['year']
        rating = request.form['rating']
        
        # Validation
        if not title or not author or not genre:
            flash('Title, Author, and Genre are required!', 'danger')
            return render_template('add_book.html')
        
        # Handle file upload
        cover_image = 'default_book.png'
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename and allowed_file(file.filename):
                # Generate unique filename
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                try:
                    file.save(file_path)
                    resize_image(file_path)  # Resize the uploaded image
                    cover_image = filename
                except Exception as e:
                    flash('Error uploading image. Using default cover.', 'warning')
        
        # Create new book
        book = Book(
            title=title,
            author=author,
            genre=genre,
            description=description,
            year=year,
            rating=float(rating) if rating else None,
            cover_image=cover_image,
            user_id=current_user.id
        )
        
        try:
            db.session.add(book)
            db.session.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding book. Please try again.', 'danger')
    
    return render_template('add_book.html')

@app.route('/api/analyze_cover', methods=['POST'])
@login_required
def analyze_cover():
    """API endpoint to analyze book cover using Gemini AI"""
    print(f"analyze_cover endpoint called by user: {current_user.username}")  # Debug print
    
    if 'cover_image' not in request.files:
        print("No cover_image in request files")  # Debug print
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['cover_image']
    print(f"File received: {file.filename}, content type: {file.content_type}")  # Debug print
    
    if not file or not file.filename or not allowed_file(file.filename):
        print("Invalid file or filename")  # Debug print
        return jsonify({'error': 'Invalid image file'}), 400
    
    try:
        # Save temporary file
        temp_filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], temp_filename)
        print(f"Saving temp file to: {temp_path}")  # Debug print
        file.save(temp_path)
        
        # Verify file was saved
        if not os.path.exists(temp_path):
            print("Temp file was not saved properly")  # Debug print
            return jsonify({'error': 'Failed to save uploaded file'}), 500
        
        print(f"Temp file size: {os.path.getsize(temp_path)} bytes")  # Debug print
        
        # Analyze with Gemini
        print("Calling analyze_book_cover_with_gemini...")  # Debug print
        book_info = analyze_book_cover_with_gemini(temp_path)
        
        # Clean up temporary file
        try:
            os.remove(temp_path)
        except:
            pass
        
        if book_info:
            return jsonify({
                'success': True,
                'data': book_info
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Could not analyze the image. AI service may be unavailable or the image may not be clear enough.'
            })
    
    except Exception as e:
        print(f"Error in analyze_cover: {e}")  # Debug print
        
        # Check if it's a quota error
        error_message = str(e)
        if "429" in error_message or "quota" in error_message.lower():
            return jsonify({
                'success': False,
                'error': 'AI analysis temporarily unavailable due to usage limits. Please try again in a few minutes or use manual entry.'
            }), 429
        else:
            return jsonify({
                'success': False,
                'error': f'Error analyzing image: {str(e)}'
            }), 500

@app.route('/api/test_ai')
@login_required
def test_ai():
    """Simple endpoint to test if AI is configured"""
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'your_gemini_api_key_here':
        return jsonify({
            'status': 'error',
            'message': 'Gemini API key not configured'
        })
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        return jsonify({
            'status': 'success',
            'message': 'AI is properly configured and ready to use!'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'AI configuration error: {str(e)}'
        })

@app.route('/book/<int:book_id>')
def view_book(book_id):
    # Public view - anyone can view book details
    book = Book.query.get_or_404(book_id)
    
    # Get comments for this book
    comments = Comment.query.filter_by(book_id=book_id).order_by(Comment.created_at.desc()).all()
    
    # Check if current user can edit/delete (only book owner)
    can_edit = current_user.is_authenticated and current_user.id == book.user_id
    
    return render_template('view_book.html', book=book, comments=comments, can_edit=can_edit)

@app.route('/edit_book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        book.title = request.form['title']
        book.author = request.form['author']
        book.genre = request.form['genre']
        book.description = request.form['description']
        book.year = request.form['year']
        book.rating = float(request.form['rating']) if request.form['rating'] else None
        
        # Handle new cover image upload
        if 'cover_image' in request.files:
            file = request.files['cover_image']
            if file and file.filename and allowed_file(file.filename):
                # Delete old image if it's not the default
                if book.cover_image != 'default_book.png':
                    old_file_path = os.path.join(app.config['UPLOAD_FOLDER'], book.cover_image)
                    if os.path.exists(old_file_path):
                        os.remove(old_file_path)
                
                # Save new image
                filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                try:
                    file.save(file_path)
                    resize_image(file_path)
                    book.cover_image = filename
                except Exception as e:
                    flash('Error uploading new image. Keeping current cover.', 'warning')
        
        try:
            db.session.commit()
            flash('Book updated successfully!', 'success')
            return redirect(url_for('view_book', book_id=book.id))
        except Exception as e:
            db.session.rollback()
            flash('Error updating book. Please try again.', 'danger')
    
    return render_template('edit_book.html', book=book)

@app.route('/delete_book/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id, user_id=current_user.id).first_or_404()
    
    # Delete cover image if it's not the default
    if book.cover_image != 'default_book.png':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], book.cover_image)
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error deleting file: {e}")
    
    try:
        db.session.delete(book)
        db.session.commit()
        flash('Book deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting book. Please try again.', 'danger')
    
    return redirect(url_for('dashboard'))

@app.route('/profile')
@login_required
def profile():
    total_books = Book.query.filter_by(user_id=current_user.id).count()
    favorite_genre = db.session.query(Book.genre).filter_by(user_id=current_user.id).group_by(Book.genre).order_by(db.func.count(Book.genre).desc()).first()
    favorite_genre = favorite_genre[0] if favorite_genre else "None"
    
    recent_books = Book.query.filter_by(user_id=current_user.id).order_by(Book.created_at.desc()).limit(5).all()
    
    return render_template('profile.html', total_books=total_books, 
                         favorite_genre=favorite_genre, recent_books=recent_books)

# API endpoints for AJAX requests
@app.route('/api/books')
@login_required
def api_books():
    books = Book.query.filter_by(user_id=current_user.id).all()
    return jsonify([{
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'genre': book.genre,
        'rating': book.rating
    } for book in books])

# Like/Unlike functionality
@app.route('/api/like/<int:book_id>', methods=['POST'])
@login_required
def toggle_like(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Check if user already liked this book
    existing_like = Like.query.filter_by(user_id=current_user.id, book_id=book_id).first()
    
    if existing_like:
        # Unlike the book
        db.session.delete(existing_like)
        liked = False
    else:
        # Like the book
        new_like = Like(user_id=current_user.id, book_id=book_id)
        db.session.add(new_like)
        liked = True
    
    try:
        db.session.commit()
        likes_count = book.get_likes_count()
        return jsonify({
            'success': True,
            'liked': liked,
            'likes_count': likes_count
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Add comment
@app.route('/api/comment/<int:book_id>', methods=['POST'])
@login_required
def add_comment(book_id):
    book = Book.query.get_or_404(book_id)
    
    # Handle both JSON and form data
    if request.is_json:
        content = request.get_json().get('content', '').strip()
    else:
        content = request.form.get('content', '').strip()
    
    if not content:
        return jsonify({'success': False, 'error': 'Comment cannot be empty'}), 400
    
    if len(content) > 500:
        return jsonify({'success': False, 'error': 'Comment too long (max 500 characters)'}), 400
    
    comment = Comment(
        content=content,
        user_id=current_user.id,
        book_id=book_id
    )
    
    try:
        db.session.add(comment)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'comment': {
                'id': comment.id,
                'content': comment.content,
                'username': current_user.username,
                'created_at': comment.created_at.strftime('%B %d, %Y at %I:%M %p')
            }
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# Delete comment (only comment owner can delete)
@app.route('/api/comment/<int:comment_id>', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    if comment.user_id != current_user.id:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 403
    
    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create uploads directory if it doesn't exist
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Create default book cover if it doesn't exist
        default_cover_path = os.path.join(app.config['UPLOAD_FOLDER'], 'default_book.png')
        if not os.path.exists(default_cover_path):
            # Create a simple default cover image
            try:
                from PIL import Image, ImageDraw, ImageFont
                img = Image.new('RGB', (300, 400), color='#f8f9fa')
                draw = ImageDraw.Draw(img)
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 24)
                except:
                    font = ImageFont.load_default()
                draw.text((150, 200), "No Cover", fill='#6c757d', anchor='mm', font=font)
                img.save(default_cover_path)
            except ImportError:
                # If PIL is not available, just create an empty file
                with open(default_cover_path, 'w') as f:
                    f.write('')
    
    app.run(debug=True)
