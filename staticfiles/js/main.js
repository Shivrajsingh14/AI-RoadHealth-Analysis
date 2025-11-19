// ROADHealth AI JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Form loading animations
    const forms = document.querySelectorAll('#loginForm, #signupForm');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const btn = this.querySelector('button[type="submit"]');
            const btnText = btn.querySelector('.btn-text');
            const btnSpinner = btn.querySelector('.btn-spinner');
            
            // Disable button and show spinner
            btn.disabled = true;
            btnText.classList.add('d-none');
            btnSpinner.classList.remove('d-none');
            
            // Add loading class to form
            this.classList.add('form-loading');
        });
    });
    
    // Enhanced file input handling
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                // Validate file type
                const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
                if (!validTypes.includes(file.type)) {
                    alert('Please select a valid image file (JPG, PNG, or WebP)');
                    this.value = '';
                    return;
                }
                
                // Validate file size (10MB max)
                if (file.size > 10 * 1024 * 1024) {
                    alert('File size must be less than 10MB');
                    this.value = '';
                    return;
                }
                
                // Preview image
                previewImage(file, this);
            }
        });
    });
    
    // Drag and drop functionality
    const uploadZones = document.querySelectorAll('.upload-zone');
    
    uploadZones.forEach(zone => {
        zone.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.classList.add('drag-hover');
        });
        
        zone.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.classList.remove('drag-hover');
        });
        
        zone.addEventListener('drop', function(e) {
            e.preventDefault();
            this.classList.remove('drag-hover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                const fileInput = this.querySelector('input[type="file"]');
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
        });
    });
    
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
});

// Image preview function
function previewImage(file, input) {
    const reader = new FileReader();
    reader.onload = function(e) {
        // Create or update preview
        let preview = document.querySelector('.image-preview');
        if (!preview) {
            preview = document.createElement('div');
            preview.className = 'image-preview mt-3 text-center';
            input.parentNode.appendChild(preview);
        }
        
        preview.innerHTML = `
            <img src="${e.target.result}" alt="Preview" class="img-fluid rounded shadow" style="max-height: 200px;">
            <p class="text-muted mt-2">${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)</p>
        `;
    };
    reader.readAsDataURL(file);
}

// Progress simulation for loading
function simulateProgress() {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        let width = 0;
        const interval = setInterval(() => {
            width += Math.random() * 10;
            if (width >= 100) {
                width = 100;
                clearInterval(interval);
            }
            progressBar.style.width = width + '%';
        }, 200);
    }
}

// Smooth animations for page transitions
function fadeInElements() {
    const elements = document.querySelectorAll('.fade-in-element');
    elements.forEach((element, index) => {
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, index * 100);
    });
}

// Initialize animations
window.addEventListener('load', function() {
    fadeInElements();
});