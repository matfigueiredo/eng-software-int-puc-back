from config import Settings, settings


class TestSettings:
    """Test configuration settings"""
    
    def test_settings_attributes(self):
        """Test that settings has all required attributes"""
        test_settings = Settings()
        
        assert hasattr(test_settings, 'MODEL_PATH')
        assert hasattr(test_settings, 'MODEL_INFO_PATH')
        assert hasattr(test_settings, 'API_TITLE')
        assert hasattr(test_settings, 'API_DESCRIPTION')
        assert hasattr(test_settings, 'API_VERSION')
        assert hasattr(test_settings, 'HOST')
        assert hasattr(test_settings, 'PORT')
    
    def test_settings_values(self):
        """Test settings values"""
        test_settings = Settings()
        
        assert test_settings.MODEL_PATH == "student_dropout_simple_model.pkl"
        assert test_settings.MODEL_INFO_PATH == "student_dropout_simple_model_info.pkl"
        assert test_settings.API_TITLE == "Student Dropout Prediction API - Simplified"
        assert "API simplificada" in test_settings.API_DESCRIPTION
        assert test_settings.API_VERSION == "2.0.0"
        assert test_settings.HOST == "0.0.0.0"
        assert test_settings.PORT == 8000
    
    def test_global_settings_instance(self):
        """Test that global settings instance exists"""
        assert settings is not None
        assert isinstance(settings, Settings)
        assert settings.MODEL_PATH == "student_dropout_simple_model.pkl" 