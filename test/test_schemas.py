import pytest
from models.schemas import SimpleStudentData, PredictionResponse, ModelInfo, FeatureInfo, FeaturesResponse


class TestSimpleStudentData:
    
    @pytest.fixture
    def valid_data_dict(self):
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
    
    def test_from_dict(self, valid_data_dict):
        student = SimpleStudentData.from_dict(valid_data_dict)
        
        assert student.age_at_enrollment == 20
        assert student.gender == 1
        assert student.marital_status == 1
        assert student.admission_grade == 150.0
        assert student.unemployment_rate == 8.5
    
    def test_to_dict(self, valid_data_dict):
        student = SimpleStudentData.from_dict(valid_data_dict)
        result_dict = student.to_dict()
        
        assert result_dict == valid_data_dict
        assert isinstance(result_dict, dict)
    
    def test_dataclass_creation(self):
        student = SimpleStudentData(
            age_at_enrollment=25,
            gender=0,
            marital_status=2,
            admission_grade=180.0,
            daytime_evening_attendance=0,
            scholarship_holder=1,
            tuition_fees_up_to_date=1,
            curricular_units_1st_sem_enrolled=8,
            curricular_units_1st_sem_approved=7,
            curricular_units_1st_sem_grade=15.0,
            curricular_units_2nd_sem_enrolled=8,
            curricular_units_2nd_sem_approved=8,
            curricular_units_2nd_sem_grade=16.0,
            unemployment_rate=12.0
        )
        
        assert student.age_at_enrollment == 25
        assert student.gender == 0
        assert student.admission_grade == 180.0


class TestPredictionResponse:
    
    def test_creation_and_to_dict(self):
        response = PredictionResponse(
            prediction='Graduate',
            confidence={'Graduate': 0.7, 'Dropout': 0.3},
            model_info={'model_name': 'Test Model', 'version': '1.0'}
        )
        
        result_dict = response.to_dict()
        
        assert result_dict['prediction'] == 'Graduate'
        assert result_dict['confidence']['Graduate'] == 0.7
        assert result_dict['model_info']['model_name'] == 'Test Model'


class TestModelInfo:
    
    def test_creation_and_to_dict(self):
        model_info = ModelInfo(
            model_name='Random Forest',
            model_score=0.85,
            test_accuracy=0.82,
            features_count=14,
            classes=['Graduate', 'Dropout', 'Enrolled'],
            is_simplified=True,
            feature_names=['Age', 'Gender']
        )
        
        result_dict = model_info.to_dict()
        
        assert result_dict['model_name'] == 'Random Forest'
        assert result_dict['model_score'] == 0.85
        assert result_dict['test_accuracy'] == 0.82
        assert result_dict['features_count'] == 14
        assert result_dict['is_simplified'] is True
        assert len(result_dict['classes']) == 3
        assert len(result_dict['feature_names']) == 2


class TestFeatureInfo:
    
    def test_creation_and_to_dict(self):
        feature = FeatureInfo(
            name='Age at enrollment',
            description='Student age at enrollment'
        )
        
        result_dict = feature.to_dict()
        
        assert result_dict['name'] == 'Age at enrollment'
        assert result_dict['description'] == 'Student age at enrollment'


class TestFeaturesResponse:
    
    def test_creation_and_to_dict(self):
        features = [
            FeatureInfo('Age', 'Student age'),
            FeatureInfo('Gender', 'Student gender')
        ]
        
        response = FeaturesResponse(
            total_features=2,
            features=features
        )
        
        result_dict = response.to_dict()
        
        assert result_dict['total_features'] == 2
        assert len(result_dict['features']) == 2
        assert result_dict['features'][0]['name'] == 'Age'
        assert result_dict['features'][1]['name'] == 'Gender' 