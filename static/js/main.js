// BookKeeper Enhanced JavaScript Functions

// Global variables
let searchTimeout;
const SEARCH_DELAY = 300; // milliseconds

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize all components
    initializeAnimations();
    initializeInteractiveElements();
    initializeSearch();
    initializeLazyLoading();
    initializeKeyboardShortcuts();
    initializeThemeToggle();
    initializeAutoSave();
    initializeParticles();
    initializeScrollEffects();
    
    console.log('🚀 BookKeeper Enhanced Edition initialized successfully');
}

// Initialize page animations
function initializeAnimations() {
    // Add stagger animation to book cards
    const bookCards = document.querySelectorAll('.book-card');
    bookCards.forEach((card, index) => {
        card.classList.add('stagger-animation');
        card.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add entrance animations to form elements
    const formGroups = document.querySelectorAll('.form-group, .mb-3');
    formGroups.forEach((group, index) => {
        group.classList.add('fade-in-up');
        group.style.animationDelay = `${index * 0.1}s`;
    });
    
    // Add card hover effects
    initializeCardAnimations();
}

// Initialize card animations
function initializeCardAnimations() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.classList.add('hover-lift');
        });
        
        card.addEventListener('mouseleave', function() {
            this.classList.remove('hover-lift');
        });
    });
}

// Initialize interactive elements
function initializeInteractiveElements() {
    // Add ripple effect to buttons
    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });
    
    // Add glow effect to interactive elements
    const interactiveElements = document.querySelectorAll('.interactive, .hover-glow');
    interactiveElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            this.style.boxShadow = '0 0 30px rgba(113, 201, 206, 0.6)';
        });
        
        element.addEventListener('mouseleave', function() {
            this.style.boxShadow = '';
        });
    });
}

// Create ripple effect
function createRipple(event) {
    const button = event.currentTarget;
    const ripple = document.createElement('span');
    const rect = button.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.position = 'absolute';
    ripple.style.borderRadius = '50%';
    ripple.style.transform = 'scale(0)';
    ripple.style.animation = 'ripple 0.6s linear';
    ripple.style.backgroundColor = 'rgba(255, 255, 255, 0.3)';
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    ripple.style.pointerEvents = 'none';
    
    button.style.position = 'relative';
    button.style.overflow = 'hidden';
    button.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Initialize particle system
function initializeParticles() {
    const particleContainer = document.body;
    const particleCount = 5;
    
    for (let i = 0; i < particleCount; i++) {
        createParticle(particleContainer);
    }
}

// Create floating particles
function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.left = Math.random() * 100 + '%';
    particle.style.top = Math.random() * 100 + '%';
    particle.style.animationDelay = Math.random() * 4 + 's';
    particle.style.animationDuration = (4 + Math.random() * 4) + 's';
    
    container.appendChild(particle);
    
    // Remove and recreate particle after animation
    setTimeout(() => {
        particle.remove();
        createParticle(container);
    }, 8000);
}

// Enhanced search functionality with animations
function initializeSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;
    
    // Add search icon animation
    const searchIcon = searchInput.parentNode.querySelector('i');
    if (searchIcon) {
        searchInput.addEventListener('focus', () => {
            searchIcon.classList.add('fa-spin');
        });
        
        searchInput.addEventListener('blur', () => {
            searchIcon.classList.remove('fa-spin');
        });
    }
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        const query = this.value.trim();
        
        // Visual feedback for search
        this.style.background = query ? 'rgba(113, 201, 206, 0.1)' : '';
        
        searchTimeout = setTimeout(() => {
            performSearch(query);
        }, SEARCH_DELAY);
    });
    
    // Add search suggestions with animation
    addSearchSuggestions(searchInput);
}

function performSearch(query) {
    const bookCards = document.querySelectorAll('.book-card');
    let visibleCount = 0;
    
    bookCards.forEach(card => {
        const title = card.dataset.title || '';
        const author = card.dataset.author || '';
        const genre = card.dataset.genre || '';
        
        const isMatch = title.includes(query.toLowerCase()) || 
                       author.includes(query.toLowerCase()) || 
                       genre.includes(query.toLowerCase());
        
        if (isMatch || query === '') {
            card.style.display = 'block';
            card.classList.add('fade-in');
            visibleCount++;
        } else {
            card.style.display = 'none';
            card.classList.remove('fade-in');
        }
    });
    
    // Update search results count
    updateSearchResultsCount(visibleCount, query);
}

function addSearchSuggestions(input) {
    // Create datalist for search suggestions
    const datalist = document.createElement('datalist');
    datalist.id = 'search-suggestions';
    input.setAttribute('list', 'search-suggestions');
    input.parentNode.appendChild(datalist);
    
    // Populate suggestions from existing books
    const bookCards = document.querySelectorAll('.book-card');
    const suggestions = new Set();
    
    bookCards.forEach(card => {
        const title = card.dataset.title;
        const author = card.dataset.author;
        if (title) suggestions.add(title);
        if (author) suggestions.add(author);
    });
    
    suggestions.forEach(suggestion => {
        const option = document.createElement('option');
        option.value = suggestion;
        datalist.appendChild(option);
    });
}

function updateSearchResultsCount(count, query) {
    let resultElement = document.getElementById('search-results-count');
    
    if (!resultElement) {
        resultElement = document.createElement('div');
        resultElement.id = 'search-results-count';
        resultElement.className = 'small text-muted mt-2';
        
        const searchContainer = document.querySelector('input[name="search"]').closest('.card-body');
        if (searchContainer) {
            searchContainer.appendChild(resultElement);
        }
    }
    
    if (query) {
        resultElement.textContent = `${count} book${count !== 1 ? 's' : ''} found for "${query}"`;
        resultElement.style.display = 'block';
    } else {
        resultElement.style.display = 'none';
    }
}

// Lazy loading for images
function initializeLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// Keyboard shortcuts
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Only trigger shortcuts when not in input fields
        if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
        
        if (e.ctrlKey || e.metaKey) {
            switch(e.key) {
                case 'k': // Ctrl+K: Focus search
                    e.preventDefault();
                    focusSearch();
                    break;
                case 'n': // Ctrl+N: Add new book
                    e.preventDefault();
                    window.location.href = '/add_book';
                    break;
                case 'd': // Ctrl+D: Go to dashboard
                    e.preventDefault();
                    window.location.href = '/dashboard';
                    break;
            }
        }
        
        // Escape key: Clear search or close modals
        if (e.key === 'Escape') {
            clearSearch();
            closeModals();
        }
    });
}

function focusSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        searchInput.focus();
        searchInput.select();
    }
}

function clearSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput && searchInput.value) {
        searchInput.value = '';
        performSearch('');
    }
}

function closeModals() {
    const modals = document.querySelectorAll('.modal.show');
    modals.forEach(modal => {
        const bsModal = bootstrap.Modal.getInstance(modal);
        if (bsModal) bsModal.hide();
    });
}

// Theme toggle functionality
function initializeThemeToggle() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;
    
    const currentTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', currentTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Update icon
        const icon = themeToggle.querySelector('i');
        if (newTheme === 'dark') {
            icon.className = 'fas fa-sun';
        } else {
            icon.className = 'fas fa-moon';
        }
        
        showToast(`Switched to ${newTheme} theme`, 'info');
    });
}

// Auto-save functionality for forms
function initializeAutoSave() {
    const forms = document.querySelectorAll('form[data-autosave]');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('input, textarea, select');
        
        inputs.forEach(input => {
            input.addEventListener('input', debounce(() => {
                autoSaveForm(form);
            }, 1000));
        });
    });
}

function autoSaveForm(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);
    
    const formId = form.id || 'default';
    localStorage.setItem(`autosave_${formId}`, JSON.stringify(data));
    
    showToast('Draft saved', 'info', 2000);
}

function restoreAutoSavedForm(formId) {
    const savedData = localStorage.getItem(`autosave_${formId}`);
    if (!savedData) return;
    
    const data = JSON.parse(savedData);
    const form = document.getElementById(formId);
    if (!form) return;
    
    Object.keys(data).forEach(key => {
        const input = form.querySelector(`[name="${key}"]`);
        if (input) {
            input.value = data[key];
        }
    });
    
    showToast('Draft restored', 'success', 3000);
}

// Enhanced image upload with preview and validation
function initializeImageUpload() {
    const uploadAreas = document.querySelectorAll('.upload-area');
    
    uploadAreas.forEach(area => {
        const input = area.querySelector('input[type="file"]');
        if (!input) return;
        
        // Click to upload
        area.addEventListener('click', () => input.click());
        
        // Drag and drop
        area.addEventListener('dragover', handleDragOver);
        area.addEventListener('dragleave', handleDragLeave);
        area.addEventListener('drop', (e) => handleDrop(e, input));
        
        // File input change
        input.addEventListener('change', (e) => handleFileSelect(e.target));
    });
}

function handleDragOver(e) {
    e.preventDefault();
    e.currentTarget.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
}

function handleDrop(e, input) {
    e.preventDefault();
    e.currentTarget.classList.remove('dragover');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        input.files = files;
        handleFileSelect(input);
    }
}

function handleFileSelect(input) {
    if (!input.files || input.files.length === 0) return;
    
    const file = input.files[0];
    
    // Validate file
    if (!validateImageFile(file)) return;
    
    // Show preview
    previewImage(file, input);
}

function validateImageFile(file) {
    const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
    const maxSize = 16 * 1024 * 1024; // 16MB
    
    if (!allowedTypes.includes(file.type)) {
        showToast('Please select a valid image file (JPEG, PNG, GIF)', 'error');
        return false;
    }
    
    if (file.size > maxSize) {
        showToast('File size must be less than 16MB', 'error');
        return false;
    }
    
    return true;
}

function previewImage(file, input) {
    const reader = new FileReader();
    
    reader.onload = function(e) {
        const uploadArea = input.closest('.upload-area');
        const placeholder = uploadArea.querySelector('#upload-placeholder');
        const preview = uploadArea.querySelector('#image-preview');
        const previewImg = uploadArea.querySelector('#preview-img');
        
        if (previewImg) {
            previewImg.src = e.target.result;
            placeholder.classList.add('d-none');
            preview.classList.remove('d-none');
        }
    };
    
    reader.readAsDataURL(file);
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showToast(message, type = 'info', duration = 5000) {
    // Create toast container if it doesn't exist
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast element
    const toastId = 'toast-' + Date.now();
    const toastHTML = `
        <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="toast-header">
                <i class="fas fa-${getToastIcon(type)} text-${type} me-2"></i>
                <strong class="me-auto">BookKeeper</strong>
                <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
            </div>
            <div class="toast-body">
                ${message}
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement, { delay: duration });
    toast.show();
    
    // Remove toast element after it's hidden
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

function getToastIcon(type) {
    const icons = {
        'success': 'check-circle',
        'error': 'exclamation-triangle',
        'warning': 'exclamation-triangle',
        'info': 'info-circle'
    };
    return icons[type] || 'info-circle';
}

function showLoadingSpinner(show = true) {
    let spinner = document.getElementById('loading-spinner');
    
    if (show && !spinner) {
        spinner = document.createElement('div');
        spinner.id = 'loading-spinner';
        spinner.className = 'position-fixed top-0 start-0 w-100 h-100 d-flex align-items-center justify-content-center';
        spinner.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
        spinner.style.zIndex = '9999';
        spinner.innerHTML = `
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        `;
        document.body.appendChild(spinner);
    } else if (!show && spinner) {
        spinner.remove();
    }
}

// Form validation enhancements
function enhanceFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
            
            form.classList.add('was-validated');
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                if (this.checkValidity()) {
                    this.classList.remove('is-invalid');
                    this.classList.add('is-valid');
                } else {
                    this.classList.remove('is-valid');
                    this.classList.add('is-invalid');
                }
            });
        });
    });
}

// Book card interactions
function initializeBookCards() {
    const bookCards = document.querySelectorAll('.book-item');
    
    bookCards.forEach(card => {
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
        
        // Add click to view functionality
        card.addEventListener('click', function(e) {
            // Don't trigger if clicking on buttons
            if (e.target.closest('.btn') || e.target.closest('button')) return;
            
            const viewLink = this.querySelector('a[href*="view_book"]');
            if (viewLink) {
                window.location.href = viewLink.href;
            }
        });
    });
}

// Initialize all components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    enhanceFormValidation();
    initializeImageUpload();
    initializeBookCards();
});

// Export functions for global use
window.BookKeeper = {
    showToast,
    showLoadingSpinner,
    debounce,
    validateImageFile,
    previewImage,
    focusSearch,
    clearSearch
};
