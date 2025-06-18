from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class SimpleStudentData:
    """Student data for prediction"""
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
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SimpleStudentData':
        """Create instance from dictionary"""
        return cls(
            age_at_enrollment=data['age_at_enrollment'],
            gender=data['gender'],
            marital_status=data['marital_status'],
            admission_grade=data['admission_grade'],
            daytime_evening_attendance=data['daytime_evening_attendance'],
            scholarship_holder=data['scholarship_holder'],
            tuition_fees_up_to_date=data['tuition_fees_up_to_date'],
            curricular_units_1st_sem_enrolled=data['curricular_units_1st_sem_enrolled'],
            curricular_units_1st_sem_approved=data['curricular_units_1st_sem_approved'],
            curricular_units_1st_sem_grade=data['curricular_units_1st_sem_grade'],
            curricular_units_2nd_sem_enrolled=data['curricular_units_2nd_sem_enrolled'],
            curricular_units_2nd_sem_approved=data['curricular_units_2nd_sem_approved'],
            curricular_units_2nd_sem_grade=data['curricular_units_2nd_sem_grade'],
            unemployment_rate=data['unemployment_rate']
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'age_at_enrollment': self.age_at_enrollment,
            'gender': self.gender,
            'marital_status': self.marital_status,
            'admission_grade': self.admission_grade,
            'daytime_evening_attendance': self.daytime_evening_attendance,
            'scholarship_holder': self.scholarship_holder,
            'tuition_fees_up_to_date': self.tuition_fees_up_to_date,
            'curricular_units_1st_sem_enrolled': self.curricular_units_1st_sem_enrolled,
            'curricular_units_1st_sem_approved': self.curricular_units_1st_sem_approved,
            'curricular_units_1st_sem_grade': self.curricular_units_1st_sem_grade,
            'curricular_units_2nd_sem_enrolled': self.curricular_units_2nd_sem_enrolled,
            'curricular_units_2nd_sem_approved': self.curricular_units_2nd_sem_approved,
            'curricular_units_2nd_sem_grade': self.curricular_units_2nd_sem_grade,
            'unemployment_rate': self.unemployment_rate
        }

@dataclass
class PredictionResponse:
    """Response for prediction endpoint"""
    prediction: str
    confidence: Dict[str, float]
    model_info: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response"""
        return {
            'prediction': self.prediction,
            'confidence': self.confidence,
            'model_info': self.model_info
        }

@dataclass
class ModelInfo:
    """Model information response"""
    model_name: str
    model_score: float
    test_accuracy: float
    features_count: int
    classes: List[str]
    is_simplified: bool
    feature_names: List[str]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response"""
        return {
            'model_name': self.model_name,
            'model_score': self.model_score,
            'test_accuracy': self.test_accuracy,
            'features_count': self.features_count,
            'classes': self.classes,
            'is_simplified': self.is_simplified,
            'feature_names': self.feature_names
        }

@dataclass
class FeatureInfo:
    """Feature information"""
    name: str
    description: str
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response"""
        return {
            'name': self.name,
            'description': self.description
        }

@dataclass
class FeaturesResponse:
    """Features list response"""
    total_features: int
    features: List[FeatureInfo]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON response"""
        return {
            'total_features': self.total_features,
            'features': [feature.to_dict() for feature in self.features]
        } 