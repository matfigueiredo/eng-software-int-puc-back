from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from main import app
from models.schemas import SimpleStudentData
from services.prediction_service import PredictionService


@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def sample_student_data():
    """Sample student data for testing"""
    return SimpleStudentData(
        age_at_enrollment=20,
        gender=1,
        marital_status=1,
        admission_grade=150.0,
        daytime_evening_attendance=1,
        scholarship_holder=0,
        tuition_fees_up_to_date=1,
        curricular_units_1st_sem_enrolled=6,
        curricular_units_1st_sem_approved=5,
        curricular_units_1st_sem_grade=13.5,
        curricular_units_2nd_sem_enrolled=6,
        curricular_units_2nd_sem_approved=6,
        curricular_units_2nd_sem_grade=14.2,
        unemployment_rate=9.5
    )

@pytest.fixture
def mock_model():
    """Mock ML model for testing"""
    mock = Mock()
    mock.predict.return_value = ["Graduate"]
    mock.predict_proba.return_value = [[0.2, 0.7, 0.1]]
    mock.classes_ = ["Dropout", "Graduate", "Enrolled"]
    return mock

@pytest.fixture
def mock_model_info():
    """Mock model info for testing"""
    return {
        "model_name": "Test Random Forest",
        "model_score": 0.85,
        "test_accuracy": 0.82,
        "classes": ["Dropout", "Graduate", "Enrolled"],
        "is_simplified": True,
        "feature_names": [
            'Age at enrollment',
            'Gender',
            'Marital status',
            'Admission grade',
            'Daytime/evening attendance',
            'Scholarship holder',
            'Tuition fees up to date',
            'Curricular units 1st sem (enrolled)',
            'Curricular units 1st sem (approved)',
            'Curricular units 1st sem (grade)',
            'Curricular units 2nd sem (enrolled)',
            'Curricular units 2nd sem (approved)',
            'Curricular units 2nd sem (grade)',
            'Unemployment rate'
        ]
    }

@pytest.fixture
def prediction_service_with_model(mock_model, mock_model_info):
    """PredictionService with loaded mock model"""
    service = PredictionService()
    service.model = mock_model
    service.model_info = mock_model_info
    return service 