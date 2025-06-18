import pytest
from pydantic import ValidationError

from models.schemas import FeatureInfo, ModelInfo, PredictionResponse, SimpleStudentData


class TestSimpleStudentData:
    """Test SimpleStudentData schema validation"""
    
    def test_valid_student_data(self):
        """Test creating valid student data"""
        data = SimpleStudentData(
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
        
        assert data.age_at_enrollment == 20
        assert data.gender == 1
        assert data.admission_grade == 150.0
        assert data.unemployment_rate == 9.5
    
    def test_missing_required_field(self):
        """Test validation error for missing required field"""
        with pytest.raises(ValidationError) as exc_info:
            SimpleStudentData(
                age_at_enrollment=20,
                gender=1,
                # Missing marital_status
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
        
        assert "marital_status" in str(exc_info.value)
    
    def test_wrong_type_field(self):
        """Test validation error for wrong type"""
        with pytest.raises(ValidationError) as exc_info:
            SimpleStudentData(
                age_at_enrollment="invalid",  # Should be int
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
        
        assert "age_at_enrollment" in str(exc_info.value)

class TestPredictionResponse:
    """Test PredictionResponse schema"""
    
    def test_valid_prediction_response(self):
        """Test creating valid prediction response"""
        response = PredictionResponse(
            prediction="Graduate",
            confidence={"Dropout": 0.2, "Graduate": 0.7, "Enrolled": 0.1},
            model_info={"model_name": "Test Model", "features_used": 14}
        )
        
        assert response.prediction == "Graduate"
        assert response.confidence["Graduate"] == 0.7
        assert response.model_info["model_name"] == "Test Model"

class TestModelInfo:
    """Test ModelInfo schema"""
    
    def test_valid_model_info(self):
        """Test creating valid model info"""
        info = ModelInfo(
            model_name="Random Forest",
            model_score=0.85,
            test_accuracy=0.82,
            features_count=14,
            classes=["Dropout", "Graduate", "Enrolled"],
            is_simplified=True,
            feature_names=["age", "gender"]
        )
        
        assert info.model_name == "Random Forest"
        assert info.model_score == 0.85
        assert len(info.classes) == 3
        assert info.is_simplified is True

class TestFeatureInfo:
    """Test FeatureInfo schema"""
    
    def test_valid_feature_info(self):
        """Test creating valid feature info"""
        feature = FeatureInfo(
            name="Age at enrollment",
            description="Idade do estudante na matrícula"
        )
        
        assert feature.name == "Age at enrollment"
        assert feature.description == "Idade do estudante na matrícula" 