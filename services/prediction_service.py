import os
from typing import Any, Dict, Optional

import joblib
import pandas as pd

from config import settings
from logger import log_error, log_info, log_warning
from models.schemas import PredictionResponse, SimpleStudentData


class PredictionService:
    def __init__(self):
        self.model = None
        self.model_info = None
    
    def load_model(self):
        """Load the model and model info from disk"""
        try:
            if os.path.exists(settings.MODEL_PATH) and os.path.exists(settings.MODEL_INFO_PATH):
                self.model = joblib.load(settings.MODEL_PATH)
                self.model_info = joblib.load(settings.MODEL_INFO_PATH)
                log_info(f"✅ Simplified model loaded: {self.model_info['model_name']}")
                log_info(f"📊 Features: {len(self.model_info['feature_names'])}")
                log_info(f"🎯 Classes: {self.model_info['classes']}")
            else:
                log_warning("❌ Model files not found. Please run generate_simple_model.py first.")
                return False
        except Exception as e:
            log_error(f"💥 Error loading model: {e}")
            return False
        return True
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None and self.model_info is not None
    
    def get_model_info(self) -> Optional[Dict[str, Any]]:
        """Get model information"""
        if not self.is_model_loaded():
            return None
        
        return {
            "model_name": self.model_info.get("model_name"),
            "model_score": self.model_info.get("model_score"),
            "test_accuracy": self.model_info.get("test_accuracy"),
            "features_count": len(self.model_info.get("feature_names", [])),
            "classes": self.model_info.get("classes", []),
            "is_simplified": self.model_info.get("is_simplified", True),
            "feature_names": self.model_info.get("feature_names", [])
        }
    
    def predict(self, student_data: SimpleStudentData) -> PredictionResponse:
        """Make prediction for student data"""
        if not self.is_model_loaded():
            raise Exception("Model not loaded")
        
        # Convert pydantic model to dict with correct column names
        data_dict = {
            'Age at enrollment': student_data.age_at_enrollment,
            'Gender': student_data.gender,
            'Marital status': student_data.marital_status,
            'Admission grade': student_data.admission_grade,
            'Daytime/evening attendance': student_data.daytime_evening_attendance,
            'Scholarship holder': student_data.scholarship_holder,
            'Tuition fees up to date': student_data.tuition_fees_up_to_date,
            'Curricular units 1st sem (enrolled)': student_data.curricular_units_1st_sem_enrolled,
            'Curricular units 1st sem (approved)': student_data.curricular_units_1st_sem_approved,
            'Curricular units 1st sem (grade)': student_data.curricular_units_1st_sem_grade,
            'Curricular units 2nd sem (enrolled)': student_data.curricular_units_2nd_sem_enrolled,
            'Curricular units 2nd sem (approved)': student_data.curricular_units_2nd_sem_approved,
            'Curricular units 2nd sem (grade)': student_data.curricular_units_2nd_sem_grade,
            'Unemployment rate': student_data.unemployment_rate
        }
        
        # Create DataFrame with single row
        df = pd.DataFrame([data_dict])
        
        # Ensure columns are in the same order as training
        feature_names = self.model_info['feature_names']
        df = df[feature_names]
        
        # Make prediction
        prediction = self.model.predict(df)[0]
        
        # Get prediction probabilities
        confidence = {}
        if hasattr(self.model, 'predict_proba'):
            try:
                probabilities = self.model.predict_proba(df)[0]
                classes = self.model.classes_
                confidence = {str(cls): float(prob) for cls, prob in zip(classes, probabilities)}
            except Exception as e:
                log_error(f"💥 Error getting probabilities: {e}")
                confidence = {"prediction_only": 1.0}
        else:
            confidence = {"prediction_only": 1.0}
        
        return PredictionResponse(
            prediction=str(prediction),
            confidence=confidence,
            model_info={
                "model_name": self.model_info.get("model_name", "Unknown"),
                "features_used": len(feature_names),
                "is_simplified": True
            }
        )
    
    def get_features_info(self) -> Dict[str, Any]:
        """Get features information with descriptions"""
        if not self.is_model_loaded():
            return None
        
        feature_descriptions = {
            'Age at enrollment': 'Idade do estudante na matrícula (16-80 anos)',
            'Gender': 'Gênero (0=Feminino, 1=Masculino)',
            'Marital status': 'Estado civil (1=Solteiro, 2=Casado, 3=Divorciado, 4=Viúvo)',
            'Admission grade': 'Nota de admissão (0-200)',
            'Daytime/evening attendance': 'Período (0=Noturno, 1=Diurno)',
            'Scholarship holder': 'Bolseiro (0=Não, 1=Sim)',
            'Tuition fees up to date': 'Propinas em dia (0=Não, 1=Sim)',
            'Curricular units 1st sem (enrolled)': 'Unidades curriculares matriculadas no 1º semestre',
            'Curricular units 1st sem (approved)': 'Unidades curriculares aprovadas no 1º semestre',
            'Curricular units 1st sem (grade)': 'Nota média do 1º semestre (0-20)',
            'Curricular units 2nd sem (enrolled)': 'Unidades curriculares matriculadas no 2º semestre',
            'Curricular units 2nd sem (approved)': 'Unidades curriculares aprovadas no 2º semestre',
            'Curricular units 2nd sem (grade)': 'Nota média do 2º semestre (0-20)',
            'Unemployment rate': 'Taxa de desemprego (%)'
        }
        
        features = []
        for feature_name in self.model_info['feature_names']:
            features.append({
                'name': feature_name,
                'description': feature_descriptions.get(feature_name, 'Descrição não disponível')
            })
        
        return {
            'total_features': len(features),
            'features': features
        }

# Global instance
prediction_service = PredictionService() 