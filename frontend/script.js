// Configuration
const API_BASE_URL = 'http://localhost:5000/api';

// State management
let currentStep = 1;
const totalSteps = 5;

// DOM elements - will be initialized after DOM loads
let form, resultsDiv, prevBtn, nextBtn, submitBtn, fillExampleBtn, progressFill, currentStepSpan;

function initializeElements() {
    form = document.getElementById('predictionForm');
    resultsDiv = document.getElementById('results');
    prevBtn = document.getElementById('prevBtn');
    nextBtn = document.getElementById('nextBtn');
    submitBtn = document.getElementById('submitBtn');
    fillExampleBtn = document.getElementById('fillExampleBtn');
    progressFill = document.getElementById('progressFill');
    currentStepSpan = document.getElementById('currentStep');
    
    console.log('Elements initialized:', {
        form: !!form,
        resultsDiv: !!resultsDiv,
        prevBtn: !!prevBtn,
        nextBtn: !!nextBtn,
        submitBtn: !!submitBtn,
        fillExampleBtn: !!fillExampleBtn,
        progressFill: !!progressFill,
        currentStepSpan: !!currentStepSpan
    });
}

// Initialize the form
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing...');
    
    // Wait a bit for all elements to be ready
    setTimeout(() => {
        initializeElements(); // Initialize DOM elements first
        initializeForm();
        updateStepDisplay(); // Make sure first step is properly displayed
        updateProgress();
        testApiConnection();
        
        // Show welcome message
        setTimeout(() => {
            showNotification('Bem-vindo! Use o botão "Exemplo" para testar', 'info');
        }, 1000);
    }, 100);
});

// Initialize form and event listeners
function initializeForm() {
    console.log('Initializing form...');
    
    // Check if elements exist
    if (!prevBtn || !nextBtn || !submitBtn || !fillExampleBtn) {
        console.error('Navigation buttons not found!');
        return;
    }
    
    // Navigation buttons
    prevBtn.addEventListener('click', previousStep);
    nextBtn.addEventListener('click', nextStep);
    submitBtn.addEventListener('click', handleSubmit);
    fillExampleBtn.addEventListener('click', fillExampleData);
    
    // Form validation on input change
    const inputs = form.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.addEventListener('change', () => {
            // Clear error styling when user starts typing
            if (input.value && input.value.trim() !== '') {
                input.style.borderColor = '';
            }
        });
        input.addEventListener('input', () => {
            // Clear error styling when user starts typing
            if (input.value && input.value.trim() !== '') {
                input.style.borderColor = '';
            }
        });
    });
    
    console.log('Form initialized successfully');
}

// Navigation functions
function nextStep() {
    console.log('Next step clicked, current step:', currentStep);
    
    if (validateCurrentStep()) {
        if (currentStep < totalSteps) {
            currentStep++;
            console.log('Moving to step:', currentStep);
            updateStepDisplay();
            updateProgress();
        } else {
            console.log('Already at last step');
        }
    } else {
        console.log('Validation failed, staying at step:', currentStep);
    }
}

function previousStep() {
    console.log('Previous step clicked, current step:', currentStep);
    
    if (currentStep > 1) {
        currentStep--;
        console.log('Moving to step:', currentStep);
        updateStepDisplay();
        updateProgress();
    } else {
        console.log('Already at first step');
    }
}

// Update step display
function updateStepDisplay() {
    console.log('Updating step display to step:', currentStep);
    
    // Hide all step contents
    const stepContents = document.querySelectorAll('.step-content');
    stepContents.forEach(content => {
        content.classList.remove('active');
    });
    
    // Show current step content
    const currentContent = document.querySelector(`.step-content[data-step="${currentStep}"]`);
    if (currentContent) {
        currentContent.classList.add('active');
        console.log('Activated step content:', currentStep);
    } else {
        console.error('Could not find step content for step:', currentStep);
    }
    
    // Update stepper
    const steps = document.querySelectorAll('.stepper .step');
    steps.forEach((step, index) => {
        const stepNumber = index + 1;
        step.classList.remove('active', 'completed');
        
        if (stepNumber < currentStep) {
            step.classList.add('completed');
        } else if (stepNumber === currentStep) {
            step.classList.add('active');
        }
    });
    
    // Update navigation buttons
    if (prevBtn) prevBtn.classList.toggle('hidden', currentStep === 1);
    if (nextBtn) nextBtn.classList.toggle('hidden', currentStep === totalSteps);
    if (submitBtn) submitBtn.classList.toggle('hidden', currentStep !== totalSteps);
    
    // Hide results when navigating
    if (resultsDiv) resultsDiv.classList.add('hidden');
}

// Update progress bar
function updateProgress() {
    const progress = (currentStep / totalSteps) * 100;
    if (progressFill) {
        progressFill.style.width = `${progress}%`;
    }
    if (currentStepSpan) {
        currentStepSpan.textContent = currentStep;
    }
    console.log('Progress updated:', progress + '%', 'Step:', currentStep);
}

// Validate current step
function validateCurrentStep() {
    const currentContent = document.querySelector(`.step-content[data-step="${currentStep}"]`);
    if (!currentContent) {
        console.error('Could not find current step content for validation:', currentStep);
        return false;
    }
    
    const inputs = currentContent.querySelectorAll('input[required], select[required]');
    let isValid = true;
    let emptyFields = [];
    
    inputs.forEach(input => {
        if (!input.value || input.value.trim() === '') {
            isValid = false;
            input.style.borderColor = 'hsl(var(--destructive))';
            emptyFields.push(input.previousElementSibling?.textContent || input.name);
        } else {
            input.style.borderColor = '';
        }
    });
    
    if (!isValid) {
        console.log('Validation failed for fields:', emptyFields);
        showNotification('Por favor, preencha todos os campos obrigatórios', 'error');
    }
    
    return isValid;
}

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();
    
    if (!validateAllSteps()) {
        showNotification('Por favor, verifique todos os campos', 'error');
        return;
    }
    
    setLoading(true);
    
    try {
        const formData = collectFormData();
        const response = await fetch(`${API_BASE_URL}/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        displayPrediction(data);
        
    } catch (error) {
        console.error('Prediction error:', error);
        displayError('Erro ao fazer predição. Verifique se a API está funcionando.');
    } finally {
        setLoading(false);
    }
}

// Validate all steps
function validateAllSteps() {
    const allInputs = form.querySelectorAll('input[required], select[required]');
    let isValid = true;
    
    allInputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
        }
    });
    
    return isValid;
}

// Collect form data
function collectFormData() {
    const formData = new FormData(form);
    const data = {};
    
    for (let [key, value] of formData.entries()) {
        // Convert numeric values
        if (value && !isNaN(value)) {
            data[key] = parseFloat(value);
        } else {
            data[key] = value;
        }
    }
    
    return data;
}

// Display prediction results
function displayPrediction(data) {
    console.log('Received prediction data:', data);
    
    // Handle both string and number predictions
    const predictionLabels = {
        // Number format
        0: { text: 'O aluno abandona o curso', class: 'dropout', emoji: '⚠️' },
        1: { text: 'O aluno continua matriculado no curso', class: 'enrolled', emoji: '📚' },
        2: { text: 'O aluno se gradua no curso', class: 'graduate', emoji: '🎓' },
        // String format
        'Dropout': { text: 'O aluno abandona o curso', class: 'dropout', emoji: '⚠️' },
        'Enrolled': { text: 'O aluno continua matriculado no curso', class: 'enrolled', emoji: '📚' },
        'Graduate': { text: 'O aluno se gradua no curso', class: 'graduate', emoji: '🎓' }
    };
    
    const prediction = predictionLabels[data.prediction];
    const predictionText = prediction ? prediction.text : 'Desconhecido';
    const predictionClass = prediction ? prediction.class : 'unknown';
    const predictionEmoji = prediction ? prediction.emoji : '❓';
    
    const confidenceData = data.confidence || {};
    
    // Convert confidence percentages (they come as decimals)
    const dropoutPercent = ((confidenceData.Dropout || confidenceData.dropout || 0) * 100).toFixed(1);
    const enrolledPercent = ((confidenceData.Enrolled || confidenceData.enrolled || 0) * 100).toFixed(1);
    const graduatePercent = ((confidenceData.Graduate || confidenceData.graduate || 0) * 100).toFixed(1);
    
    // Get model info
    const modelInfo = data.model_info || {};
    const modelName = modelInfo.model_name || 'SVM';
    
    const resultHTML = `    
        <div class="prediction-result">
            <div class="prediction-badge prediction-${predictionClass}">
                ${predictionEmoji} ${predictionText}
            </div>
            <p>Modelo escolhido: <strong>${modelName}</strong></p>

            <br>

            <p>Veja as probabilidades de cada resultado:</p>
            
            <div class="confidence-grid">
                <div class="confidence-item">
                    <div class="confidence-label">⚠️ Abandono</div>
                    <div class="confidence-value">${dropoutPercent}%</div>
                </div>
                <div class="confidence-item">
                    <div class="confidence-label">📚 Matriculado</div>
                    <div class="confidence-value">${enrolledPercent}%</div>
                </div>
                <div class="confidence-item">
                    <div class="confidence-label">🎓 Graduado</div>
                    <div class="confidence-value">${graduatePercent}%</div>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('prediction-content').innerHTML = resultHTML;
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
    
    // Show success notification
    showNotification(`Predição: ${predictionText}`, 'success');
}

// Display error message
function displayError(message) {
    const errorHTML = `
        <div class="error-message">
            <strong>Erro:</strong> ${message}
        </div>
    `;
    
    document.getElementById('prediction-content').innerHTML = errorHTML;
    resultsDiv.classList.remove('hidden');
    resultsDiv.scrollIntoView({ behavior: 'smooth' });
    
    showNotification(`Erro: ${message}`, 'error');
}

// Set loading state
function setLoading(isLoading) {
    const btnText = submitBtn.querySelector('.btn-text');
    const btnLoader = submitBtn.querySelector('.btn-loader');
    
    if (isLoading) {
        btnText.classList.add('hidden');
        btnLoader.classList.add('visible');
        submitBtn.disabled = true;
        form.classList.add('loading');
    } else {
        btnText.classList.remove('hidden');
        btnLoader.classList.remove('visible');
        submitBtn.disabled = false;
        form.classList.remove('loading');
    }
}

// Fill example data
function fillExampleData() {
    const exampleData = {
        age_at_enrollment: 18,
        gender: '0',
        marital_status: '1',
        admission_grade: 142.5,
        daytime_evening_attendance: '1',
        scholarship_holder: '0',
        tuition_fees_up_to_date: '1',
        curricular_units_1st_sem_enrolled: 6,
        curricular_units_1st_sem_approved: 6,
        curricular_units_1st_sem_grade: 13.4,
        curricular_units_2nd_sem_enrolled: 6,
        curricular_units_2nd_sem_approved: 6,
        curricular_units_2nd_sem_grade: 13.4,
        unemployment_rate: 10.8
    };
    
    // Fill form fields
    Object.entries(exampleData).forEach(([key, value]) => {
        const field = document.getElementById(key);
        if (field) {
            field.value = value;
        }
    });
    
    // Show success message
    showNotification('Dados de exemplo preenchidos!', 'success');
    
    // Go to first step to review data
    currentStep = 1;
    updateStepDisplay();
    updateProgress();
}

// Test API connection
async function testApiConnection() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (response.ok) {
            const data = await response.json();
        }
    } catch (error) {
        showNotification('API não disponível. Verifique se o servidor está rodando', 'error');
    }
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style notification
    Object.assign(notification.style, {
        transform: 'translateX(100%)',
        transition: 'transform 0.3s ease'
    });
    
    // Add to page
    document.body.appendChild(notification);
    
    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remove after delay
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 3000);
} 