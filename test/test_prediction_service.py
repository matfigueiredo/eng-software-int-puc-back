import pytest
from unittest.mock import Mock, patch, mock_open
import pandas as pd
import joblib

from services.prediction_service import PredictionService
from models.schemas import SimpleStudentData, PredictionResponse


class TestPredictionService:
    
    @pytest.fixture
    def service(self):
        return PredictionService()
    
    @pytest.fixture
    def mock_model_info(self):
        return {
            'model_name': 'Test Model',
            'model_score': 0.85,
            'test_accuracy': 0.82,
            'classes': ['Graduate', 'Dropout', 'Enrolled'],
            'is_simplified': True,
            'feature_names': [
                'Age at enrollment',
                'Gender',
                'Admission grade'
            ]
        }
    
    @pytest.fixture
    def mock_model(self):
        model = Mock()
        model.predict.return_value = ['Graduate']
        model.predict_proba.return_value = [[0.7, 0.2, 0.1]]
        model.classes_ = ['Graduate', 'Dropout', 'Enrolled']
        return model
    
    @pytest.fixture
    def sample_student_data(self):
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
            curricular_units_1st_sem_grade=12.5,
            curricular_units_2nd_sem_enrolled=6,
            curricular_units_2nd_sem_approved=6,
            curricular_units_2nd_sem_grade=13.0,
            unemployment_rate=8.5
        )

    def test_init(self, service):
        assert service.model is None
        assert service.model_info is None

    @patch('os.path.exists')
    @patch('joblib.load')
    def test_load_model_success(self, mock_joblib_load, mock_exists, service, mock_model, mock_model_info):
        mock_exists.return_value = True
        mock_joblib_load.side_effect = [mock_model, mock_model_info]
        
        result = service.load_model()
        
        assert result is True
        assert service.model == mock_model
        assert service.model_info == mock_model_info
        assert mock_joblib_load.call_count == 2

    @patch('os.path.exists')
    def test_load_model_files_not_found(self, mock_exists, service):
        mock_exists.return_value = False
        
        result = service.load_model()
        
        assert result is False
        assert service.model is None
        assert service.model_info is None

    @patch('os.path.exists')
    @patch('joblib.load')
    def test_load_model_exception(self, mock_joblib_load, mock_exists, service):
        mock_exists.return_value = True
        mock_joblib_load.side_effect = Exception("Load error")
        
        result = service.load_model()
        
        assert result is False

    def test_is_model_loaded_false(self, service):
        assert service.is_model_loaded() is False

    def test_is_model_loaded_true(self, service, mock_model, mock_model_info):
        service.model = mock_model
        service.model_info = mock_model_info
        
        assert service.is_model_loaded() is True

    def test_get_model_info_not_loaded(self, service):
        result = service.get_model_info()
        
        assert result is None

    def test_get_model_info_loaded(self, service, mock_model, mock_model_info):
        service.model = mock_model
        service.model_info = mock_model_info
        
        result = service.get_model_info()
        
        assert result['model_name'] == 'Test Model'
        assert result['model_score'] == 0.85
        assert result['test_accuracy'] == 0.82
        assert result['features_count'] == 3
        assert result['classes'] == ['Graduate', 'Dropout', 'Enrolled']
        assert result['is_simplified'] is True

    def test_predict_model_not_loaded(self, service, sample_student_data):
        with pytest.raises(Exception, match="Model not loaded"):
            service.predict(sample_student_data)

    def test_predict_success(self, service, mock_model, mock_model_info, sample_student_data):
        service.model = mock_model
        service.model_info = mock_model_info
        
        result = service.predict(sample_student_data)
        
        assert isinstance(result, PredictionResponse)
        assert result.prediction == 'Graduate'
        assert 'Graduate' in result.confidence
        assert 'Dropout' in result.confidence
        assert 'Enrolled' in result.confidence
        assert result.model_info['model_name'] == 'Test Model'
        assert result.model_info['is_simplified'] is True

    def test_predict_without_probabilities(self, service, mock_model_info, sample_student_data):
        mock_model = Mock()
        mock_model.predict.return_value = ['Graduate']
        # Remove predict_proba method
        delattr(mock_model, 'predict_proba') if hasattr(mock_model, 'predict_proba') else None
        
        service.model = mock_model
        service.model_info = mock_model_info
        
        result = service.predict(sample_student_data)
        
        assert result.prediction == 'Graduate'
        assert result.confidence == {"prediction_only": 1.0}

    def test_get_features_info_not_loaded(self, service):
        result = service.get_features_info()
        
        assert result is None

    def test_get_features_info_loaded(self, service, mock_model, mock_model_info):
        service.model = mock_model
        service.model_info = mock_model_info
        
        result = service.get_features_info()
        
        assert result['total_features'] == 3
        assert len(result['features']) == 3
        assert result['features'][0]['name'] == 'Age at enrollment'
        assert 'Idade do estudante' in result['features'][0]['description'] 