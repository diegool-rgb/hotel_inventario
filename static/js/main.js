// JavaScript para mejorar la funcionalidad del Sistema de Inventario Hotelero

document.addEventListener('DOMContentLoaded', function() {
    
    // Mostrar loading en formularios
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('btn-loading');
                submitBtn.disabled = true;
                
                // Crear overlay de loading
                const loadingOverlay = document.createElement('div');
                loadingOverlay.className = 'loading-overlay';
                loadingOverlay.innerHTML = '<div class="loading-spinner"></div>';
                document.body.appendChild(loadingOverlay);
                
                // Remover loading si hay error (después de 10 segundos)
                setTimeout(() => {
                    submitBtn.classList.remove('btn-loading');
                    submitBtn.disabled = false;
                    if (document.body.contains(loadingOverlay)) {
                        document.body.removeChild(loadingOverlay);
                    }
                }, 10000);
            }
        });
    });
    
    // Animaciones para elementos que entran en pantalla
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate__animated');
            }
        });
    }, observerOptions);
    
    // Observar elementos con clase fade-in-up
    document.querySelectorAll('.fade-in-up').forEach(el => {
        observer.observe(el);
    });
    
    // Mejorar tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Auto-hide alerts después de 5 segundos
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease-out';
            alert.style.opacity = '0';
            setTimeout(() => {
                if (alert.parentNode) {
                    alert.parentNode.removeChild(alert);
                }
            }, 500);
        }, 5000);
    });
    
    // Validación en tiempo real para formularios
    const formControls = document.querySelectorAll('.form-control, .form-select');
    formControls.forEach(control => {
        control.addEventListener('blur', function() {
            validateField(this);
        });
        
        control.addEventListener('input', function() {
            if (this.classList.contains('is-invalid')) {
                validateField(this);
            }
        });
    });
    
    function validateField(field) {
        const formGroup = field.closest('.form-group, .mb-3');
        
        // Limpiar estados anteriores
        field.classList.remove('is-valid', 'is-invalid');
        if (formGroup) {
            formGroup.classList.remove('has-success', 'has-error');
        }
        
        // Validar campo requerido
        if (field.hasAttribute('required') && !field.value.trim()) {
            field.classList.add('is-invalid');
            if (formGroup) {
                formGroup.classList.add('has-error');
            }
            return false;
        }
        
        // Validar email
        if (field.type === 'email' && field.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(field.value)) {
                field.classList.add('is-invalid');
                if (formGroup) {
                    formGroup.classList.add('has-error');
                }
                return false;
            }
        }
        
        // Validar números
        if (field.type === 'number' && field.value) {
            const num = parseFloat(field.value);
            const min = parseFloat(field.min);
            const max = parseFloat(field.max);
            
            if (isNaN(num) || (min !== null && num < min) || (max !== null && num > max)) {
                field.classList.add('is-invalid');
                if (formGroup) {
                    formGroup.classList.add('has-error');
                }
                return false;
            }
        }
        
        // Campo válido
        if (field.value.trim()) {
            field.classList.add('is-valid');
            if (formGroup) {
                formGroup.classList.add('has-success');
            }
        }
        
        return true;
    }
    
    // Mejorar dropdowns
    const dropdownButtons = document.querySelectorAll('[data-bs-toggle="dropdown"]');
    dropdownButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Agregar efectos de animación
            const dropdown = this.nextElementSibling;
            if (dropdown && dropdown.classList.contains('dropdown-menu')) {
                dropdown.style.transform = 'translateY(-10px)';
                dropdown.style.opacity = '0';
                
                setTimeout(() => {
                    dropdown.style.transition = 'all 0.3s ease';
                    dropdown.style.transform = 'translateY(0)';
                    dropdown.style.opacity = '1';
                }, 10);
            }
        });
    });
    
    // Confirmación para acciones destructivas
    const deleteButtons = document.querySelectorAll('.btn-danger, [data-action="delete"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!this.dataset.confirmed) {
                e.preventDefault();
                
                const confirmText = this.dataset.confirmText || '¿Estás seguro de que quieres realizar esta acción?';
                
                if (confirm(confirmText)) {
                    this.dataset.confirmed = 'true';
                    this.click();
                }
            }
        });
    });
    
    // Mejorar tablas responsivas
    const tables = document.querySelectorAll('.table');
    tables.forEach(table => {
        if (!table.closest('.table-responsive')) {
            const wrapper = document.createElement('div');
            wrapper.className = 'table-responsive';
            table.parentNode.insertBefore(wrapper, table);
            wrapper.appendChild(table);
        }
    });
    
    // Auto-save para formularios largos (opcional)
    const autoSaveForms = document.querySelectorAll('[data-auto-save]');
    autoSaveForms.forEach(form => {
        const formId = form.id || 'form_' + Date.now();
        
        // Cargar datos guardados
        const savedData = localStorage.getItem('autosave_' + formId);
        if (savedData) {
            try {
                const data = JSON.parse(savedData);
                Object.keys(data).forEach(key => {
                    const field = form.querySelector(`[name="${key}"]`);
                    if (field && field.type !== 'file') {
                        field.value = data[key];
                    }
                });
            } catch (e) {
                console.warn('Error loading auto-saved data:', e);
            }
        }
        
        // Guardar cambios
        const saveData = () => {
            const formData = new FormData(form);
            const data = {};
            for (let [key, value] of formData.entries()) {
                if (form.querySelector(`[name="${key}"]`).type !== 'file') {
                    data[key] = value;
                }
            }
            localStorage.setItem('autosave_' + formId, JSON.stringify(data));
        };
        
        // Guardar cada 30 segundos
        setInterval(saveData, 30000);
        
        // Limpiar datos guardados al enviar
        form.addEventListener('submit', () => {
            localStorage.removeItem('autosave_' + formId);
        });
    });
    
    console.log('Sistema de Inventario Hotelero - JS cargado correctamente');
});

// Función utilitaria para mostrar notificaciones
function showNotification(message, type = 'info', duration = 5000) {
    const notification = document.createElement('div');
    notification.className = `toast toast-${type}`;
    notification.innerHTML = `
        <div class="toast-body">
            ${message}
        </div>
    `;
    
    // Agregar al container de toasts
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed top-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    toastContainer.appendChild(notification);
    
    // Mostrar toast
    const toast = new bootstrap.Toast(notification, { delay: duration });
    toast.show();
    
    // Remover del DOM después de ocultarse
    notification.addEventListener('hidden.bs.toast', () => {
        notification.remove();
    });
}

// Función para formatear números como moneda chilena
function formatCurrency(amount) {
    return new Intl.NumberFormat('es-CL', {
        style: 'currency',
        currency: 'CLP'
    }).format(amount);
}

// Función para formatear fechas
function formatDate(date, options = {}) {
    const defaultOptions = {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    };
    
    return new Intl.DateTimeFormat('es-CL', { ...defaultOptions, ...options }).format(new Date(date));
}