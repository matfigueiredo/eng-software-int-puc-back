from unittest.mock import patch


class TestAPI:
    """Test API endpoints"""
    
    def test_root_endpoint_no_model(self, client):
        """Test root endpoint when no model is loaded"""
        with patch('services.prediction_service.prediction_service.is_model_loaded', return_value=False):
            with patch('services.prediction_service.prediction_service.model_info', None):
                response = client.get("/api/")
                
                assert response.status_code == 200
                data = response.json()
                assert data["message"] == "Student Dropout Prediction API"
                assert data["status"] == "running"
                assert data["model_loaded"] is False
                assert data["features"] == 0
                assert data["version"] == "1.0.0"
    
    def test_root_endpoint_with_model(self, client, mock_model_info):
        """Test root endpoint when model is loaded"""
        with patch('services.prediction_service.prediction_service.is_model_loaded', return_value=True):
            with patch('services.prediction_service.prediction_service.model_info', mock_model_info):
                response = client.get("/api/")
                
                assert response.status_code == 200
                data = response.json()
                assert data["model_loaded"] is True
    
    def test_model_info_no_model(self, client):
        """Test model-info endpoint when no model loaded"""
        with patch('services.prediction_service.prediction_service.get_model_info', return_value=None):
            response = client.get("/api/model-info")
            
            assert response.status_code == 503
            assert "Model not loaded" in response.json()["detail"]
    
    def test_model_info_success(self, client, mock_model_info):
        """Test successful model-info endpoint"""
        expected_info = {
            "model_name": "Test Random Forest",
            "model_score": 0.85,
            "test_accuracy": 0.82,
            "features_count": 14,
            "classes": ["Dropout", "Graduate", "Enrolled"],
            "is_simplified": True,
            "feature_names": mock_model_info["feature_names"]
        }
        
        with patch('services.prediction_service.prediction_service.get_model_info', return_value=expected_info):
            response = client.get("/api/model-info")
            
            assert response.status_code == 200
            data = response.json()
            assert data["model_name"] == "Test Random Forest"
            assert data["model_score"] == 0.85
            assert data["features_count"] == 14
    
    def test_predict_no_model(self, client, sample_student_data):
        """Test predict endpoint when no model loaded"""
        with patch('services.prediction_service.prediction_service.is_model_loaded', return_value=False):
            response = client.post("/api/predict", json=sample_student_data.dict())
            
            assert response.status_code == 503
            assert "Model not loaded" in response.json()["detail"]
    
    def test_predict_success(self, client, sample_student_data):
        """Test successful prediction"""
        mock_response = {
            "prediction": "Graduate",
            "confidence": {"Dropout": 0.2, "Graduate": 0.7, "Enrolled": 0.1},
            "model_info": {"model_name": "Test Model", "features_used": 14, "is_simplified": True}
        }
        
        with patch('services.prediction_service.prediction_service.is_model_loaded', return_value=True):
            with patch('services.prediction_service.prediction_service.predict', return_value=type('obj', (object,), mock_response)()):
                response = client.post("/api/predict", json=sample_student_data.dict())
                
                assert response.status_code == 200
                data = response.json()
                assert data["prediction"] == "Graduate"
                assert "confidence" in data
                assert "model_info" in data
    
    def test_predict_invalid_data(self, client):
        """Test predict with invalid data"""
        invalid_data = {
            "age_at_enrollment": "invalid",  # Should be int
            "gender": 1
            # Missing required fields
        }
        
        response = client.post("/api/predict", json=invalid_data)
        assert response.status_code == 422  # Validation error
    
    def test_predict_exception(self, client, sample_student_data):
        """Test predict when service raises exception"""
        with patch('services.prediction_service.prediction_service.is_model_loaded', return_value=True):
            with patch('services.prediction_service.prediction_service.predict', side_effect=Exception("Prediction failed")):
                response = client.post("/api/predict", json=sample_student_data.dict())
                
                assert response.status_code == 400
                assert "Prediction error" in response.json()["detail"]
    
    def test_predict_example_success(self, client):
        """Test predict-example endpoint"""
        mock_response = {
            "prediction": "Graduate",
            "confidence": {"Dropout": 0.2, "Graduate": 0.7, "Enrolled": 0.1},
            "model_info": {"model_name": "Test Model", "features_used": 14, "is_simplified": True}
        }
        
        with patch('services.prediction_service.prediction_service.is_model_loaded', return_value=True):
            with patch('services.prediction_service.prediction_service.predict', return_value=type('obj', (object,), mock_response)()):
                response = client.post("/api/predict-example")
                
                assert response.status_code == 200
                data = response.json()
                assert "prediction" in data
                assert "confidence" in data
    
    def test_features_no_model(self, client):
        """Test features endpoint when no model loaded"""
        with patch('services.prediction_service.prediction_service.is_model_loaded', return_value=False):
            response = client.get("/api/features")
            
            assert response.status_code == 503
            assert "Model not loaded" in response.json()["detail"]
    
    def test_features_success(self, client):
        """Test successful features endpoint"""
        mock_features = {
            "total_features": 2,
            "features": [
                {"name": "Age at enrollment", "description": "Idade do estudante na matrícula"},
                {"name": "Gender", "description": "Gênero do estudante"}
            ]
        }
        
        with patch('services.prediction_service.prediction_service.is_model_loaded', return_value=True):
            with patch('services.prediction_service.prediction_service.get_features_info', return_value=mock_features):
                response = client.get("/api/features")
                
                assert response.status_code == 200
                data = response.json()
                assert data["total_features"] == 2
                assert len(data["features"]) == 2
                assert data["features"][0]["name"] == "Age at enrollment"
    
    def test_features_service_returns_none(self, client):
        """Test features endpoint when service returns None"""
        with patch('services.prediction_service.prediction_service.is_model_loaded', return_value=True):
            with patch('services.prediction_service.prediction_service.get_features_info', return_value=None):
                response = client.get("/api/features")
                
                assert response.status_code == 503
                assert "Model not loaded" in response.json()["detail"] 