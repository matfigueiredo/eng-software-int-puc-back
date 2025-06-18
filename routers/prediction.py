from fastapi import APIRouter, HTTPException

from models.schemas import PredictionResponse, SimpleStudentData
from services.prediction_service import prediction_service

router = APIRouter(prefix="/api", tags=["prediction"])

@router.get("/")
async def root():
    return {
        "message": "Student Dropout Prediction API",
        "status": "running",
        "model_loaded": prediction_service.is_model_loaded(),
        "features": prediction_service.model_info['feature_count'] if prediction_service.model_info else 0,
        "version": "1.0.0"
    }

@router.get("/model-info")
async def get_model_info():
    model_info = prediction_service.get_model_info()
    if model_info is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return model_info

@router.post("/predict", response_model=PredictionResponse)
async def predict_student_status(student_data: SimpleStudentData):
    if not prediction_service.is_model_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        return prediction_service.predict(student_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@router.post("/predict-example")
async def predict_example():
    """Endpoint with simplified example data for testing"""
    example_data = SimpleStudentData(
        # Personal Information
        age_at_enrollment=18,
        gender=0,  # Female
        marital_status=1,  # Single
        
        # Academic Information
        admission_grade=140.0,
        daytime_evening_attendance=1,  # Daytime
        
        # Financial Status
        scholarship_holder=1,  # Yes
        tuition_fees_up_to_date=1,  # Yes
        
        # 1st Semester Performance
        curricular_units_1st_sem_enrolled=8,
        curricular_units_1st_sem_approved=8,
        curricular_units_1st_sem_grade=14.0,
        
        # 2nd Semester Performance
        curricular_units_2nd_sem_enrolled=8,
        curricular_units_2nd_sem_approved=8,
        curricular_units_2nd_sem_grade=14.5,
        
        # Economic Context
        unemployment_rate=10.8
    )
    
    return await predict_student_status(example_data)

@router.get("/features")
async def get_features():
    """Get list of features with descriptions"""
    if not prediction_service.is_model_loaded():
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    features_info = prediction_service.get_features_info()
    if features_info is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    return features_info 