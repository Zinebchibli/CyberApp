// Main JavaScript for SecureBank Application

document.addEventListener('DOMContentLoaded', function() {
    // Add fade-in animation to flash messages
    const flashMessages = document.querySelectorAll('[role="alert"]');
    flashMessages.forEach(msg => {
        msg.classList.add('alert-animation');
        
        // Auto-dismiss flash messages after 5 seconds
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s';
            
            // Remove from DOM after fade out
            setTimeout(() => {
                msg.remove();
            }, 500);
        }, 5000);
    });

    // Handle form submissions for logging
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            // Log form submission (this is just for demo purposes)
            console.log('Form submitted:', form.action);
        });
    });
    
    // Format currency values on input (for transfer form)
    const amountInput = document.getElementById('amount');
    if (amountInput) {
        amountInput.addEventListener('blur', function() {
            if (this.value) {
                // Format to 2 decimal places
                this.value = parseFloat(this.value).toFixed(2);
            }
        });
    }
    
    // IBAN validator (very simple version for demo)
    const ibanInput = document.getElementById('receiver_account');
    if (ibanInput) {
        ibanInput.addEventListener('blur', function() {
            const iban = this.value.trim().replace(/\s/g, '');
            
            // Very basic validation - just checking length and format for demo
            if (iban && (iban.length < 15 || !/^[A-Z]{2}/.test(iban))) {
                this.classList.add('border-red-500');
                
                // Show warning
                let warning = document.getElementById('iban-warning');
                if (!warning) {
                    warning = document.createElement('p');
                    warning.id = 'iban-warning';
                    warning.className = 'mt-1 text-xs text-red-600';
                    warning.textContent = 'Format IBAN incorrect. Exemple: FR7630001007941234567890185';
                    this.parentNode.appendChild(warning);
                }
            } else {
                this.classList.remove('border-red-500');
                const warning = document.getElementById('iban-warning');
                if (warning) {
                    warning.remove();
                }
            }
        });
    }
});
