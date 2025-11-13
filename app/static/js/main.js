// Main JavaScript for ActiScore

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeNavigation();
    initializeFileUploads();
    initializeProgressBars();
    initializeTooltips();
    initializeModals();
});

// Navigation functionality
function initializeNavigation() {
    // Mobile menu toggle
    const mobileMenuButton = document.querySelector('[data-mobile-menu-toggle]');
    const mobileMenu = document.querySelector('[data-mobile-menu]');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// File upload functionality
function initializeFileUploads() {
    const fileUploadAreas = document.querySelectorAll('[data-file-upload]');
    
    fileUploadAreas.forEach(area => {
        const fileInput = area.querySelector('input[type="file"]');
        const fileInfo = area.querySelector('[data-file-info]');
        const filePreview = area.querySelector('[data-file-preview]');
        
        if (fileInput) {
            // Drag and drop functionality
            area.addEventListener('dragover', function(e) {
                e.preventDefault();
                area.classList.add('dragover');
            });
            
            area.addEventListener('dragleave', function(e) {
                e.preventDefault();
                area.classList.remove('dragover');
            });
            
            area.addEventListener('drop', function(e) {
                e.preventDefault();
                area.classList.remove('dragover');
                
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    handleFileSelect(files[0], fileInfo, filePreview);
                }
            });
            
            // File input change
            fileInput.addEventListener('change', function(e) {
                if (e.target.files.length > 0) {
                    handleFileSelect(e.target.files[0], fileInfo, filePreview);
                }
            });
            
            // Click to upload
            area.addEventListener('click', function() {
                fileInput.click();
            });
        }
    });
}

function handleFileSelect(file, fileInfo, filePreview) {
    // Validate file
    if (!validateFile(file)) {
        showNotification('Invalid file type or size', 'error');
        return;
    }
    
    // Update file info
    if (fileInfo) {
        fileInfo.innerHTML = `
            <div class="text-sm text-gray-600">
                <strong>${file.name}</strong>
                <br>
                Size: ${formatFileSize(file.size)}
                <br>
                Type: ${file.type}
            </div>
        `;
        fileInfo.classList.remove('hidden');
    }
    
    // Show preview for images and videos
    if (filePreview && (file.type.startsWith('image/') || file.type.startsWith('video/'))) {
        const reader = new FileReader();
        reader.onload = function(e) {
            if (file.type.startsWith('image/')) {
                filePreview.innerHTML = `<img src="${e.target.result}" class="max-w-full h-auto rounded-lg">`;
            } else if (file.type.startsWith('video/')) {
                filePreview.innerHTML = `<video src="${e.target.result}" controls class="max-w-full h-auto rounded-lg"></video>`;
            }
            filePreview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
    
    // Trigger custom event
    document.dispatchEvent(new CustomEvent('fileSelected', { detail: { file: file } }));
}

function validateFile(file) {
    const maxSize = 16 * 1024 * 1024; // 16MB
    const allowedTypes = [
        // Video types
        'video/mp4', 'video/avi', 'video/mov', 'video/mkv', 'video/webm',
        // Audio types
        'audio/wav', 'audio/mp3', 'audio/flac', 'audio/aac', 'audio/m4a',
        // Document types
        'application/pdf', 'text/plain', 'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    ];
    
    if (file.size > maxSize) {
        return false;
    }
    
    if (!allowedTypes.includes(file.type)) {
        return false;
    }
    
    return true;
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Progress bar functionality
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('[data-progress-bar]');
    
    progressBars.forEach(bar => {
        const progress = parseInt(bar.dataset.progress) || 0;
        const progressFill = bar.querySelector('[data-progress-fill]');
        
        if (progressFill) {
            setTimeout(() => {
                progressFill.style.width = progress + '%';
            }, 100);
        }
    });
}

// Tooltip functionality
function initializeTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    
    tooltipTriggers.forEach(trigger => {
        const tooltipText = trigger.dataset.tooltip;
        
        trigger.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'absolute z-50 px-2 py-1 text-sm text-white bg-gray-900 rounded shadow-lg';
            tooltip.textContent = tooltipText;
            tooltip.style.bottom = '100%';
            tooltip.style.left = '50%';
            tooltip.style.transform = 'translateX(-50%)';
            tooltip.style.marginBottom = '5px';
            
            trigger.style.position = 'relative';
            trigger.appendChild(tooltip);
        });
        
        trigger.addEventListener('mouseleave', function() {
            const tooltip = trigger.querySelector('div');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// Modal functionality
function initializeModals() {
    const modalTriggers = document.querySelectorAll('[data-modal-trigger]');
    const modalCloses = document.querySelectorAll('[data-modal-close]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.dataset.modalTrigger;
            const modal = document.getElementById(modalId);
            if (modal) {
                modal.classList.remove('hidden');
                document.body.style.overflow = 'hidden';
            }
        });
    });
    
    modalCloses.forEach(close => {
        close.addEventListener('click', function() {
            const modal = this.closest('[data-modal]');
            if (modal) {
                modal.classList.add('hidden');
                document.body.style.overflow = 'auto';
            }
        });
    });
    
    // Close modal on outside click
    document.addEventListener('click', function(e) {
        if (e.target.hasAttribute('data-modal')) {
            e.target.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    });
}

// Notification system
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transition-all duration-300 transform translate-x-full`;
    
    const colors = {
        success: 'bg-green-500 text-white',
        error: 'bg-red-500 text-white',
        info: 'bg-blue-500 text-white',
        warning: 'bg-yellow-500 text-white'
    };
    
    notification.className += ` ${colors[type] || colors.info}`;
    notification.innerHTML = `
        <div class="flex items-center">
            <span class="mr-2">${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-auto text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.classList.remove('translate-x-full');
    }, 100);
    
    // Auto remove
    setTimeout(() => {
        notification.classList.add('translate-x-full');
        setTimeout(() => {
            if (notification.parentElement) {
                notification.parentElement.removeChild(notification);
            }
        }, 300);
    }, duration);
}

// API helper functions
async function apiRequest(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        credentials: 'same-origin'
    };
    
    const response = await fetch(url, { ...defaultOptions, ...options });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for use in other scripts
window.ActiScore = {
    showNotification,
    apiRequest,
    debounce,
    throttle,
    formatFileSize
};