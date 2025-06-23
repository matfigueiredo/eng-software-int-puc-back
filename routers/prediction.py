from flask import Blueprint, jsonify, make_response, request

from logger import log_error
from models.schemas import SimpleStudentData
from services.prediction_service import prediction_service
from utils.validation import (
    ValidationError,
    create_error_response,
    validate_dataclass_data,
)

prediction_bp = Blueprint('prediction', __name__, url_prefix='/api')

def add_cors_headers(response):
    """Add CORS headers to response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Accept'
    return response

@prediction_bp.route('/', methods=['GET'])
def root():
    """Root endpoint"""
    response = make_response(jsonify({
        "message": "Student Dropout Prediction API",
        "status": "running",
        "model_loaded": prediction_service.is_model_loaded(),
        "features": len(prediction_service.model_info.get('feature_names', [])) if prediction_service.model_info else 0,
        "version": "2.0.0"
    }))
    return add_cors_headers(response)

@prediction_bp.route('/model-info', methods=['GET'])
def get_model_info():
    """Get model information"""
    model_info = prediction_service.get_model_info()
    if model_info is None:
        response = make_response(jsonify({"error": "Model not loaded"}), 503)
    else:
        response = make_response(jsonify(model_info))
    return add_cors_headers(response)

@prediction_bp.route('/predict', methods=['POST', 'OPTIONS'])
def predict_student_status():
    """Predict student dropout status"""
    if request.method == 'OPTIONS':
        response = make_response()
        return add_cors_headers(response)
    
    if not prediction_service.is_model_loaded():
        response = make_response(jsonify({"error": "Model not loaded"}), 503)
        return add_cors_headers(response)
    
    try:
        data = request.get_json()
        if not data:
            response = make_response(jsonify({"error": "No JSON data provided"}), 400)
            return add_cors_headers(response)
        
        validated_data = validate_dataclass_data(SimpleStudentData, data)
        
        student_data = SimpleStudentData.from_dict(validated_data)
        
        result = prediction_service.predict(student_data)
        
        response = make_response(jsonify(result.to_dict()))
        return add_cors_headers(response)
        
    except ValidationError as e:
        log_error(f"Validation error: {e.message}")
        response = make_response(jsonify(create_error_response(e)), 400)
        return add_cors_headers(response)
    except Exception as e:
        log_error(f"Prediction error: {str(e)}")
        response = make_response(jsonify({"error": f"Prediction error: {str(e)}"}), 400)
        return add_cors_headers(response)

@prediction_bp.route('/predict-example', methods=['POST'])
def predict_example():
    """Endpoint with simplified example data for testing"""
    example_data = SimpleStudentData(
        age_at_enrollment=18,
        gender=0,  # Female
        marital_status=1,  # Single
        
        admission_grade=140.0,
        daytime_evening_attendance=1,  # Daytime
        
        scholarship_holder=1,  # Yes
        tuition_fees_up_to_date=1,  # Yes
        
        curricular_units_1st_sem_enrolled=8,
        curricular_units_1st_sem_approved=8,
        curricular_units_1st_sem_grade=14.0,
        
        curricular_units_2nd_sem_enrolled=8,
        curricular_units_2nd_sem_approved=8,
        curricular_units_2nd_sem_grade=14.5,
        
        unemployment_rate=10.8
    )
    
    try:
        result = prediction_service.predict(example_data)
        response = make_response(jsonify(result.to_dict()))
        return add_cors_headers(response)
    except Exception as e:
        log_error(f"Example prediction error: {str(e)}")
        response = make_response(jsonify({"error": f"Prediction error: {str(e)}"}), 400)
        return add_cors_headers(response)

@prediction_bp.route('/features', methods=['GET'])
def get_features():
    """Get list of features with descriptions"""
    if not prediction_service.is_model_loaded():
        response = make_response(jsonify({"error": "Model not loaded"}), 503)
        return add_cors_headers(response)
    
    try:
        features_info = prediction_service.get_features_info()
        if features_info is None:
            response = make_response(jsonify({"error": "Model not loaded"}), 503)
            return add_cors_headers(response)
        
        response = make_response(jsonify(features_info))
        return add_cors_headers(response)
    except Exception as e:
        log_error(f"Features error: {str(e)}")
        response = make_response(jsonify({"error": f"Error getting features: {str(e)}"}), 500)
        return add_cors_headers(response) 