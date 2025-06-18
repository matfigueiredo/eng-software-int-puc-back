from typing import Any, Dict

from pydantic import BaseModel


class SimpleStudentData(BaseModel):
    # Personal Information (3 fields)
    age_at_enrollment: int
    gender: int  # 0=Female, 1=Male
    marital_status: int  # 1=Single, 2=Married, 3=Divorced, 4=Widowed
    
    # Academic Information (2 fields)
    admission_grade: float
    daytime_evening_attendance: int  # 0=Evening, 1=Daytime
    
    # Financial Status (2 fields)
    scholarship_holder: int  # 0=No, 1=Yes
    tuition_fees_up_to_date: int  # 0=No, 1=Yes
    
    # 1st Semester Performance (3 fields)
    curricular_units_1st_sem_enrolled: int
    curricular_units_1st_sem_approved: int
    curricular_units_1st_sem_grade: float
    
    # 2nd Semester Performance (3 fields)
    curricular_units_2nd_sem_enrolled: int
    curricular_units_2nd_sem_approved: int
    curricular_units_2nd_sem_grade: float
    
    # Economic Context (1 field)
    unemployment_rate: float

class PredictionResponse(BaseModel):
    prediction: str
    confidence: Dict[str, float]
    model_info: Dict[str, Any]

class ModelInfo(BaseModel):
    model_name: str
    model_score: float
    test_accuracy: float
    features_count: int
    classes: list
    is_simplified: bool
    feature_names: list

class FeatureInfo(BaseModel):
    name: str
    description: str

class FeaturesResponse(BaseModel):
    total_features: int
    features: list[FeatureInfo] 