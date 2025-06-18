from unittest.mock import MagicMock, Mock, patch

import pytest

from models.schemas import PredictionResponse
from services.prediction_service import PredictionService


class TestPredictionService:
    """Test PredictionService class"""
    
    def test_init(self):
        """Test service initialization"""
        service = PredictionService()
        assert service.model is None
        assert service.model_info is None
    
    def test_is_model_loaded_false(self):
        """Test is_model_loaded returns False when no model"""
        service = PredictionService()
        assert service.is_model_loaded() is False
    
    def test_is_model_loaded_true(self, prediction_service_with_model):
        """Test is_model_loaded returns True when model loaded"""
        assert prediction_service_with_model.is_model_loaded() is True
    
    @patch('os.path.exists')
    @patch('joblib.load')
    def test_load_model_success(self, mock_joblib_load, mock_exists, mock_model, mock_model_info):
        """Test successful model loading"""
        mock_exists.return_value = True
        mock_joblib_load.side_effect = [mock_model, mock_model_info]
        
        service = PredictionService()
        result = service.load_model()
        
        assert result is True
        assert service.model == mock_model
        assert service.model_info == mock_model_info
        assert mock_joblib_load.call_count == 2
    
    @patch('os.path.exists')
    def test_load_model_files_not_found(self, mock_exists):
        """Test model loading when files don't exist"""
        mock_exists.return_value = False
        
        service = PredictionService()
        result = service.load_model()
        
        assert result is False
        assert service.model is None
        assert service.model_info is None
    
    @patch('os.path.exists')
    @patch('joblib.load')
    def test_load_model_exception(self, mock_joblib_load, mock_exists):
        """Test model loading with exception"""
        mock_exists.return_value = True
        mock_joblib_load.side_effect = Exception("Loading error")
        
        service = PredictionService()
        result = service.load_model()
        
        assert result is False
    
    def test_get_model_info_no_model(self):
        """Test get_model_info when no model loaded"""
        service = PredictionService()
        result = service.get_model_info()
        assert result is None
    
    def test_get_model_info_success(self, prediction_service_with_model):
        """Test successful get_model_info"""
        result = prediction_service_with_model.get_model_info()
        
        assert result is not None
        assert result["model_name"] == "Test Random Forest"
        assert result["model_score"] == 0.85
        assert result["test_accuracy"] == 0.82
        assert result["features_count"] == 14
        assert result["is_simplified"] is True
    
    def test_predict_no_model(self, sample_student_data):
        """Test predict when no model loaded"""
        service = PredictionService()
        
        with pytest.raises(Exception, match="Model not loaded"):
            service.predict(sample_student_data)
    
    def test_predict_success(self, prediction_service_with_model, sample_student_data):
        """Test successful prediction"""
        result = prediction_service_with_model.predict(sample_student_data)
        
        assert isinstance(result, PredictionResponse)
        assert result.prediction == "Graduate"
        assert "Dropout" in result.confidence
        assert "Graduate" in result.confidence
        assert "Enrolled" in result.confidence
        assert result.model_info["model_name"] == "Unknown"
        assert result.model_info["features_used"] == 14
        assert result.model_info["is_simplified"] is True
    
    def test_predict_data_transformation(self, prediction_service_with_model, sample_student_data):
        """Test that student data is correctly transformed for prediction"""
        with patch('pandas.DataFrame') as mock_df:
            mock_df_instance = MagicMock()
            mock_df.return_value = mock_df_instance
            
            prediction_service_with_model.predict(sample_student_data)
            
            # Check DataFrame was created with correct data
            call_args = mock_df.call_args[0][0][0]  # First call, first arg, first row
            assert call_args['Age at enrollment'] == 20
            assert call_args['Gender'] == 1
            assert call_args['Admission grade'] == 150.0
            assert call_args['Unemployment rate'] == 9.5
    
    def test_predict_without_probabilities(self, mock_model_info, sample_student_data):
        """Test prediction when model doesn't have predict_proba"""
        service = PredictionService()
        mock_model = Mock()
        mock_model.predict.return_value = ["Graduate"]
        # Don't set predict_proba attribute
        delattr(mock_model, 'predict_proba') if hasattr(mock_model, 'predict_proba') else None
        
        service.model = mock_model
        service.model_info = mock_model_info
        
        result = service.predict(sample_student_data)
        
        assert result.confidence == {"prediction_only": 1.0}
    
    def test_get_features_info_no_model(self):
        """Test get_features_info when no model loaded"""
        service = PredictionService()
        result = service.get_features_info()
        assert result is None
    
    def test_get_features_info_success(self, prediction_service_with_model):
        """Test successful get_features_info"""
        result = prediction_service_with_model.get_features_info()
        
        assert result is not None
        assert result["total_features"] == 14
        assert len(result["features"]) == 14
        
        # Check first feature
        first_feature = result["features"][0]
        assert first_feature["name"] == "Age at enrollment"
        assert "Idade do estudante" in first_feature["description"]
    
    def test_predict_probabilities_exception(self, mock_model_info, sample_student_data):
        """Test prediction when predict_proba raises exception"""
        service = PredictionService()
        mock_model = Mock()
        mock_model.predict.return_value = ["Graduate"]
        mock_model.predict_proba.side_effect = Exception("Probability error")
        
        service.model = mock_model
        service.model_info = mock_model_info
        
        result = service.predict(sample_student_data)
        
        assert result.confidence == {"prediction_only": 1.0} 