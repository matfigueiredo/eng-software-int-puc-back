// API Configuration
const API_BASE_URL = 'http://localhost:8000';  // Different port for simplified API

// DOM Elements
const form = document.getElementById('predictionForm');
const submitBtn = document.getElementById('submitBtn');
const fillExampleBtn = document.getElementById('fillExampleBtn');
const resultsDiv = document.getElementById('results');
const btnText = document.querySelector('.btn-text');
const btnLoader = document.querySelector('.btn-loader');

// Simplified example data
const exampleData = {
    age_at_enrollment: 18,
    gender: 0,  // Female
    marital_status: 1,  // Single
    admission_grade: 140.0,
    daytime_evening_attendance: 1,  // Daytime
    scholarship_holder: 1,  // Yes
    tuition_fees_up_to_date: 1,  // Yes
    curricular_units_1st_sem_enrolled: 8,
    curricular_units_1st_sem_approved: 8,
    curricular_units_1st_sem_grade: 14.0,
    curricular_units_2nd_sem_enrolled: 8,
    curricular_units_2nd_sem_approved: 8,
    curricular_units_2nd_sem_grade: 14.5,
    unemployment_rate: 10.8
};

// Fill example data
function fillExampleData() {
    Object.keys(exampleData).forEach(key => {
        const input = document.getElementById(key);
        if (input) {
            input.value = exampleData[key];
            // Trigger input event for validation
            input.dispatchEvent(new Event('input'));
        }
    });
    
    // Show success message
    showNotification('✅ Dados de exemplo preenchidos!', 'success');
}

// Collect form data
function getFormData() {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        // Convert numeric fields
        if (key.includes('grade') || key.includes('rate') || key === 'admission_grade') {
            data[key] = parseFloat(value);
        } else {
            data[key] = parseInt(value);
        }
    }
    
    return data;
}

// Show loading state
function showLoading() {
    submitBtn.disabled = true;
    btnText.classList.add('hidden');
    btnLoader.classList.remove('hidden');
    btnLoader.classList.add('visible');
    form.classList.add('loading');
}

// Hide loading state
function hideLoading() {
    submitBtn.disabled = false;
    btnText.classList.remove('hidden');
    btnLoader.classList.add('hidden');
    btnLoader.classList.remove('visible');
    form.classList.remove('loading');
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style notification
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '1rem 1.5rem',
        borderRadius: '8px',
        color: 'white',
        fontWeight: '500',
        zIndex: '1000',
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    // Set background color based on type
    const colors = {
        success: '#48bb78',
        error: '#f56565',
        info: '#4299e1'
    };
    notification.style.background = colors[type] || colors.info;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
}

// Display prediction results
function displayResults(data) {
    const prediction = data.prediction;
    const confidence = data.confidence;
    
    // Determine prediction class for styling
    let predictionClass = '';
    let predictionText = '';
    let predictionEmoji = '';
    
    switch(prediction.toLowerCase()) {
        case 'dropout':
            predictionClass = 'prediction-dropout';
            predictionText = 'Risco de Abandono';
            predictionEmoji = '⚠️';
            break;
        case 'enrolled':
            predictionClass = 'prediction-enrolled';
            predictionText = 'Continua Matriculado';
            predictionEmoji = '📚';
            break;
        case 'graduate':
            predictionClass = 'prediction-graduate';
            predictionText = 'Irá se Formar';
            predictionEmoji = '🎓';
            break;
        default:
            predictionClass = 'prediction-enrolled';
            predictionText = prediction;
            predictionEmoji = '📊';
    }
    
    // Build confidence grid
    let confidenceHTML = '';
    if (confidence && Object.keys(confidence).length > 1) {
        confidenceHTML = `
            <h4 style="margin: 1rem 0 0.5rem 0; color: #4a5568;">Confiança do Modelo:</h4>
            <div class="confidence-grid">
                ${Object.entries(confidence).map(([key, value]) => {
                    const percentage = (value * 100).toFixed(1);
                    let label = key;
                    let emoji = '';
                    
                    // Translate labels
                    switch(key.toLowerCase()) {
                        case 'dropout':
                            label = 'Dropout';
                            emoji = '⚠️';
                            break;
                        case 'enrolled':
                            label = 'Enrolled';
                            emoji = '📚';
                            break;
                        case 'graduate':
                            label = 'Graduate';
                            emoji = '🎓';
                            break;
                    }
                    
                    return `
                        <div class="confidence-item">
                            <div class="confidence-label">${emoji} ${label}</div>
                            <div class="confidence-value">${percentage}%</div>
                        </div>
                    `;
                }).join('')}
            </div>
        `;
    }
    
    const resultHTML = `
        <div class="prediction-result">
            <div class="prediction-badge ${predictionClass}">
                ${predictionEmoji} ${predictionText}
            </div>
            <p style="color: #718096; margin-bottom: 0.5rem;">
                Modelo: <strong>${data.model_info.model_name}</strong> 
                (${data.model_info.features_used} campos)
            </p>
            ${confidenceHTML}
        </div>
    `;
    
    document.getElementById('prediction-content').innerHTML = resultHTML;
    resultsDiv.classList.remove('hidden');
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
    
    // Show success notification
    showNotification(`✅ Predição: ${predictionText}`, 'success');
}

// Display error message
function displayError(message) {
    const errorHTML = `
        <div class="error-message">
            <strong>❌ Erro:</strong> ${message}
        </div>
    `;
    
    document.getElementById('prediction-content').innerHTML = errorHTML;
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
    
    showNotification(`❌ Erro: ${message}`, 'error');
}

// Make prediction
async function makePrediction(data) {
    try {
        const response = await fetch(`${API_BASE_URL}/api/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        displayResults(result);
        
    } catch (error) {
        console.error('Prediction error:', error);
        
        if (error.name === 'TypeError' && error.message.includes('fetch')) {
            displayError('Não foi possível conectar com a API. Verifique se o servidor está rodando em ' + API_BASE_URL);
        } else {
            displayError(error.message);
        }
    }
}

// Validate form
function validateForm() {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    let firstInvalidField = null;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.style.borderColor = '#f56565';
            isValid = false;
            if (!firstInvalidField) {
                firstInvalidField = field;
            }
        } else {
            field.style.borderColor = '#e2e8f0';
        }
    });
    
    // Focus on first invalid field
    if (firstInvalidField) {
        firstInvalidField.focus();
        firstInvalidField.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
    
    return isValid;
}

// Validate numeric ranges
function validateRanges() {
    const validations = [
        { id: 'age_at_enrollment', min: 16, max: 80, name: 'Idade' },
        { id: 'admission_grade', min: 0, max: 200, name: 'Nota de Admissão' },
        { id: 'curricular_units_1st_sem_grade', min: 0, max: 20, name: 'Nota 1º Semestre' },
        { id: 'curricular_units_2nd_sem_grade', min: 0, max: 20, name: 'Nota 2º Semestre' },
        { id: 'unemployment_rate', min: 0, max: 30, name: 'Taxa de Desemprego' }
    ];
    
    let isValid = true;
    
    validations.forEach(({ id, min, max, name }) => {
        const field = document.getElementById(id);
        if (field && field.value) {
            const value = parseFloat(field.value);
            if (value < min || value > max) {
                field.style.borderColor = '#f56565';
                showNotification(`${name} deve estar entre ${min} e ${max}`, 'error');
                isValid = false;
            }
        }
    });
    
    return isValid;
}

// Event Listeners
fillExampleBtn.addEventListener('click', fillExampleData);

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
        displayError('Por favor, preencha todos os campos obrigatórios.');
        return;
    }
    
    if (!validateRanges()) {
        displayError('Por favor, verifique os valores inseridos.');
        return;
    }
    
    showLoading();
    
    try {
        const formData = getFormData();
        await makePrediction(formData);
    } catch (error) {
        displayError('Erro ao processar os dados do formulário.');
    } finally {
        hideLoading();
    }
});

// Test API connection on page load
async function testAPIConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/api`);
        if (response.ok) {
            const data = await response.json();
            console.log('✅ API connection successful');
            console.log('📊 Model features:', data.features);
            showNotification('🟢 Conectado à API simplificada', 'success');
        }
    } catch (error) {
        console.warn('⚠️ API connection failed:', error.message);
        console.warn('Make sure the simplified API server is running on', API_BASE_URL);
        showNotification('🔴 API não disponível. Execute: python main_simple.py', 'error');
    }
}

// Add input event listeners for real-time validation
function setupRealTimeValidation() {
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            if (input.value.trim()) {
                input.style.borderColor = '#e2e8f0';
            }
        });
        
        // Add focus effects
        input.addEventListener('focus', () => {
            input.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', () => {
            input.parentElement.style.transform = 'scale(1)';
        });
    });
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    testAPIConnection();
    setupRealTimeValidation();
    
    // Show welcome message
    setTimeout(() => {
        showNotification('👋 Bem-vindo! Use o botão "Preencher Exemplo" para testar', 'info');
    }, 1000);
}); 