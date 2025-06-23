import pytest
import json
from unittest.mock import Mock, patch
from flask import Flask

from routers.prediction import prediction_bp
from models.schemas import SimpleStudentData, PredictionResponse
from utils.validation import ValidationError


class TestPredictionRouter:
    
    @pytest.fixture
    def app(self):
        app = Flask(__name__)
        app.register_blueprint(prediction_bp)
        app.config['TESTING'] = True
        return app
    
    @pytest.fixture
    def client(self, app):
        return app.test_client()
    
    @pytest.fixture
    def mock_prediction_service(self):
        with patch('routers.prediction.prediction_service') as mock:
            yield mock
    
    @pytest.fixture
    def sample_request_data(self):
        return {
            'age_at_enrollment': 20,
            'gender': 1,
            'marital_status': 1,
            'admission_grade': 150.0,
            'daytime_evening_attendance': 1,
            'scholarship_holder': 0,
            'tuition_fees_up_to_date': 1,
            'curricular_units_1st_sem_enrolled': 6,
            'curricular_units_1st_sem_approved': 5,
            'curricular_units_1st_sem_grade': 12.5,
            'curricular_units_2nd_sem_enrolled': 6,
            'curricular_units_2nd_sem_approved': 6,
            'curricular_units_2nd_sem_grade': 13.0,
            'unemployment_rate': 8.5
        }
    
    @pytest.fixture
    def mock_prediction_response(self):
        return PredictionResponse(
            prediction='Graduate',
            confidence={'Graduate': 0.7, 'Dropout': 0.2, 'Enrolled': 0.1},
            model_info={'model_name': 'Test Model', 'features_used': 14, 'is_simplified': True}
        )

    def test_root_endpoint_model_loaded(self, client, mock_prediction_service):
        mock_prediction_service.is_model_loaded.return_value = True
        mock_prediction_service.model_info = {'feature_names': ['feature1', 'feature2']}
        
        response = client.get('/api/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'running'
        assert data['model_loaded'] is True
        assert data['features'] == 2
        assert 'Access-Control-Allow-Origin' in response.headers

    def test_root_endpoint_model_not_loaded(self, client, mock_prediction_service):
        mock_prediction_service.is_model_loaded.return_value = False
        mock_prediction_service.model_info = None
        
        response = client.get('/api/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['model_loaded'] is False
        assert data['features'] == 0

    def test_model_info_endpoint_success(self, client, mock_prediction_service):
        mock_info = {
            'model_name': 'Test Model',
            'model_score': 0.85,
            'features_count': 14
        }
        mock_prediction_service.get_model_info.return_value = mock_info
        
        response = client.get('/api/model-info')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['model_name'] == 'Test Model'
        assert data['model_score'] == 0.85

    def test_model_info_endpoint_not_loaded(self, client, mock_prediction_service):
        mock_prediction_service.get_model_info.return_value = None
        
        response = client.get('/api/model-info')
        
        assert response.status_code == 503
        data = json.loads(response.data)
        assert 'error' in data

    def test_predict_options_request(self, client):
        response = client.options('/api/predict')
        
        assert response.status_code == 200
        assert 'Access-Control-Allow-Origin' in response.headers
        assert 'Access-Control-Allow-Methods' in response.headers

    def test_predict_success(self, client, mock_prediction_service, sample_request_data, mock_prediction_response):
        mock_prediction_service.is_model_loaded.return_value = True
        mock_prediction_service.predict.return_value = mock_prediction_response
        
        with patch('routers.prediction.validate_dataclass_data') as mock_validate:
            mock_validate.return_value = sample_request_data
            
            response = client.post('/api/predict', 
                                 data=json.dumps(sample_request_data),
                                 content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['prediction'] == 'Graduate'
        assert 'confidence' in data

    def test_predict_model_not_loaded(self, client, mock_prediction_service, sample_request_data):
        mock_prediction_service.is_model_loaded.return_value = False
        
        response = client.post('/api/predict',
                             data=json.dumps(sample_request_data),
                             content_type='application/json')
        
        assert response.status_code == 503
        data = json.loads(response.data)
        assert 'error' in data

    def test_predict_no_json_data(self, client, mock_prediction_service):
        mock_prediction_service.is_model_loaded.return_value = True
        
        response = client.post('/api/predict')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'JSON' in data['error'] or 'application/json' in data['error']

    def test_predict_validation_error(self, client, mock_prediction_service, sample_request_data):
        mock_prediction_service.is_model_loaded.return_value = True
        
        with patch('routers.prediction.validate_dataclass_data') as mock_validate:
            mock_validate.side_effect = ValidationError("Invalid data", "age_at_enrollment")
            
            response = client.post('/api/predict',
                                 data=json.dumps(sample_request_data),
                                 content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    def test_predict_service_exception(self, client, mock_prediction_service, sample_request_data):
        mock_prediction_service.is_model_loaded.return_value = True
        mock_prediction_service.predict.side_effect = Exception("Prediction failed")
        
        with patch('routers.prediction.validate_dataclass_data') as mock_validate:
            mock_validate.return_value = sample_request_data
            
            response = client.post('/api/predict',
                                 data=json.dumps(sample_request_data),
                                 content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Prediction error' in data['error']

    def test_predict_example_success(self, client, mock_prediction_service, mock_prediction_response):
        mock_prediction_service.predict.return_value = mock_prediction_response
        
        response = client.post('/api/predict-example')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['prediction'] == 'Graduate'

    def test_predict_example_exception(self, client, mock_prediction_service):
        mock_prediction_service.predict.side_effect = Exception("Example prediction failed")
        
        response = client.post('/api/predict-example')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Prediction error' in data['error']

    def test_features_endpoint_success(self, client, mock_prediction_service):
        mock_prediction_service.is_model_loaded.return_value = True
        mock_features = {
            'total_features': 2,
            'features': [
                {'name': 'Age at enrollment', 'description': 'Student age'},
                {'name': 'Gender', 'description': 'Student gender'}
            ]
        }
        mock_prediction_service.get_features_info.return_value = mock_features
        
        response = client.get('/api/features')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['total_features'] == 2
        assert len(data['features']) == 2

    def test_features_endpoint_model_not_loaded(self, client, mock_prediction_service):
        mock_prediction_service.is_model_loaded.return_value = False
        
        response = client.get('/api/features')
        
        assert response.status_code == 503
        data = json.loads(response.data)
        assert 'error' in data

    def test_features_endpoint_service_returns_none(self, client, mock_prediction_service):
        mock_prediction_service.is_model_loaded.return_value = True
        mock_prediction_service.get_features_info.return_value = None
        
        response = client.get('/api/features')
        
        assert response.status_code == 503
        data = json.loads(response.data)
        assert 'error' in data

    def test_features_endpoint_exception(self, client, mock_prediction_service):
        mock_prediction_service.is_model_loaded.return_value = True
        mock_prediction_service.get_features_info.side_effect = Exception("Features error")
        
        response = client.get('/api/features')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'Error getting features' in data['error']

    def test_cors_headers_present(self, client, mock_prediction_service):
        mock_prediction_service.is_model_loaded.return_value = True
        
        response = client.get('/api/')
        
        assert response.headers['Access-Control-Allow-Origin'] == '*'
        assert 'GET, POST, OPTIONS' in response.headers['Access-Control-Allow-Methods']
        assert 'Content-Type' in response.headers['Access-Control-Allow-Headers'] 