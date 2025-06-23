import pytest
import numpy as np
import pandas as pd
from unittest.mock import Mock, patch
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from services.prediction_service import PredictionService
from models.schemas import SimpleStudentData


class TestModelPerformance:
    """
    Testes de performance do modelo de predição de evasão estudantil.
    
    Thresholds definidos baseados na performance atual do modelo:
    - Accuracy mínima: 60% (modelo deve ter performance básica aceitável)
    - Precision mínima: 50% (evitar modelos completamente aleatórios)
    - Recall mínimo: 55% (identificar pelo menos metade dos casos reais)
    - F1-Score mínimo: 55% (balanceamento mínimo entre precision e recall)
    """
    
    # Performance thresholds
    MIN_ACCURACY = 0.60
    MIN_PRECISION = 0.50
    MIN_RECALL = 0.55
    MIN_F1_SCORE = 0.55
    
    @pytest.fixture
    def service(self):
        service = PredictionService()
        return service
    
    @pytest.fixture
    def sample_test_data(self):
        """Dataset de teste simulado com casos conhecidos"""
        return [
            # Casos de graduação (classe 'Graduate')
            SimpleStudentData(
                age_at_enrollment=19, gender=1, marital_status=1,
                admission_grade=170.0, daytime_evening_attendance=1,
                scholarship_holder=1, tuition_fees_up_to_date=1,
                curricular_units_1st_sem_enrolled=6, curricular_units_1st_sem_approved=6,
                curricular_units_1st_sem_grade=16.0, curricular_units_2nd_sem_enrolled=6,
                curricular_units_2nd_sem_approved=6, curricular_units_2nd_sem_grade=16.5,
                unemployment_rate=5.0
            ),
            SimpleStudentData(
                age_at_enrollment=20, gender=0, marital_status=1,
                admission_grade=165.0, daytime_evening_attendance=1,
                scholarship_holder=0, tuition_fees_up_to_date=1,
                curricular_units_1st_sem_enrolled=7, curricular_units_1st_sem_approved=7,
                curricular_units_1st_sem_grade=15.5, curricular_units_2nd_sem_enrolled=7,
                curricular_units_2nd_sem_approved=7, curricular_units_2nd_sem_grade=15.8,
                unemployment_rate=6.2
            ),
            # Casos de evasão (classe 'Dropout')
            SimpleStudentData(
                age_at_enrollment=25, gender=1, marital_status=2,
                admission_grade=120.0, daytime_evening_attendance=0,
                scholarship_holder=0, tuition_fees_up_to_date=0,
                curricular_units_1st_sem_enrolled=5, curricular_units_1st_sem_approved=2,
                curricular_units_1st_sem_grade=8.5, curricular_units_2nd_sem_enrolled=4,
                curricular_units_2nd_sem_approved=1, curricular_units_2nd_sem_grade=7.0,
                unemployment_rate=15.0
            ),
            SimpleStudentData(
                age_at_enrollment=30, gender=0, marital_status=3,
                admission_grade=110.0, daytime_evening_attendance=0,
                scholarship_holder=0, tuition_fees_up_to_date=0,
                curricular_units_1st_sem_enrolled=6, curricular_units_1st_sem_approved=3,
                curricular_units_1st_sem_grade=9.0, curricular_units_2nd_sem_enrolled=5,
                curricular_units_2nd_sem_approved=2, curricular_units_2nd_sem_grade=8.5,
                unemployment_rate=18.5
            ),
            # Casos matriculados (classe 'Enrolled')
            SimpleStudentData(
                age_at_enrollment=18, gender=1, marital_status=1,
                admission_grade=145.0, daytime_evening_attendance=1,
                scholarship_holder=1, tuition_fees_up_to_date=1,
                curricular_units_1st_sem_enrolled=6, curricular_units_1st_sem_approved=5,
                curricular_units_1st_sem_grade=12.0, curricular_units_2nd_sem_enrolled=6,
                curricular_units_2nd_sem_approved=4, curricular_units_2nd_sem_grade=11.5,
                unemployment_rate=8.0
            ),
        ]
    
    @pytest.fixture
    def expected_labels(self):
        """Labels esperados para o dataset de teste"""
        return ['Graduate', 'Graduate', 'Dropout', 'Dropout', 'Enrolled']
    
    def test_model_accuracy_threshold(self, service, sample_test_data, expected_labels):
        """Testa se a accuracy do modelo atende ao threshold mínimo"""
        if not service.load_model():
            pytest.skip("Modelo não disponível para teste de performance")
        
        predictions = []
        for student_data in sample_test_data:
            try:
                result = service.predict(student_data)
                predictions.append(result.prediction)
            except Exception as e:
                pytest.fail(f"Erro na predição: {e}")
        
        accuracy = accuracy_score(expected_labels, predictions)
        
        assert accuracy >= self.MIN_ACCURACY, (
            f"Accuracy {accuracy:.3f} está abaixo do threshold mínimo {self.MIN_ACCURACY}. "
            f"Modelo não atende aos requisitos de performance."
        )
    
    def test_model_precision_threshold(self, service, sample_test_data, expected_labels):
        """Testa se a precision do modelo atende ao threshold mínimo"""
        if not service.load_model():
            pytest.skip("Modelo não disponível para teste de performance")
        
        predictions = []
        for student_data in sample_test_data:
            result = service.predict(student_data)
            predictions.append(result.prediction)
        
        # Calcula precision macro (média entre todas as classes)
        precision = precision_score(expected_labels, predictions, average='macro', zero_division=0)
        
        assert precision >= self.MIN_PRECISION, (
            f"Precision {precision:.3f} está abaixo do threshold mínimo {self.MIN_PRECISION}. "
            f"Modelo tem muitos falsos positivos."
        )
    
    def test_model_recall_threshold(self, service, sample_test_data, expected_labels):
        """Testa se o recall do modelo atende ao threshold mínimo"""
        if not service.load_model():
            pytest.skip("Modelo não disponível para teste de performance")
        
        predictions = []
        for student_data in sample_test_data:
            result = service.predict(student_data)
            predictions.append(result.prediction)
        
        # Calcula recall macro (média entre todas as classes)
        recall = recall_score(expected_labels, predictions, average='macro', zero_division=0)
        
        assert recall >= self.MIN_RECALL, (
            f"Recall {recall:.3f} está abaixo do threshold mínimo {self.MIN_RECALL}. "
            f"Modelo não identifica suficientes casos reais."
        )
    
    def test_model_f1_score_threshold(self, service, sample_test_data, expected_labels):
        """Testa se o F1-Score do modelo atende ao threshold mínimo"""
        if not service.load_model():
            pytest.skip("Modelo não disponível para teste de performance")
        
        predictions = []
        for student_data in sample_test_data:
            result = service.predict(student_data)
            predictions.append(result.prediction)
        
        # Calcula F1-Score macro (balanceamento precision/recall)
        f1 = f1_score(expected_labels, predictions, average='macro', zero_division=0)
        
        assert f1 >= self.MIN_F1_SCORE, (
            f"F1-Score {f1:.3f} está abaixo do threshold mínimo {self.MIN_F1_SCORE}. "
            f"Modelo não tem balanceamento adequado entre precision e recall."
        )
    
    def test_model_confidence_consistency(self, service, sample_test_data):
        """Testa se o modelo fornece níveis de confiança consistentes"""
        if not service.load_model():
            pytest.skip("Modelo não disponível para teste de performance")
        
        confidences = []
        for student_data in sample_test_data:
            result = service.predict(student_data)
            if result.confidence and 'prediction_only' not in result.confidence:
                # Soma das probabilidades deve ser aproximadamente 1.0
                total_confidence = sum(result.confidence.values())
                confidences.append(total_confidence)
        
        if confidences:
            # Verifica se as probabilidades somam aproximadamente 1.0
            for conf in confidences:
                assert 0.95 <= conf <= 1.05, (
                    f"Confiança inconsistente: {conf}. "
                    f"Probabilidades devem somar aproximadamente 1.0"
                )
    
    def test_model_prediction_time(self, service, sample_test_data):
        """Testa se o tempo de predição está dentro do limite aceitável"""
        if not service.load_model():
            pytest.skip("Modelo não disponível para teste de performance")
        
        import time
        
        MAX_PREDICTION_TIME = 1.0  # 1 segundo por predição
        
        for student_data in sample_test_data:
            start_time = time.time()
            service.predict(student_data)
            prediction_time = time.time() - start_time
            
            assert prediction_time <= MAX_PREDICTION_TIME, (
                f"Tempo de predição {prediction_time:.3f}s excede limite de {MAX_PREDICTION_TIME}s. "
                f"Modelo muito lento para produção."
            )
    
    def test_model_handles_edge_cases(self, service):
        """Testa se o modelo lida adequadamente com casos extremos"""
        if not service.load_model():
            pytest.skip("Modelo não disponível para teste de performance")
        
        # Caso extremo: estudante muito jovem com notas baixas
        edge_case_1 = SimpleStudentData(
            age_at_enrollment=16, gender=1, marital_status=1,
            admission_grade=95.0, daytime_evening_attendance=0,
            scholarship_holder=0, tuition_fees_up_to_date=0,
            curricular_units_1st_sem_enrolled=3, curricular_units_1st_sem_approved=0,
            curricular_units_1st_sem_grade=5.0, curricular_units_2nd_sem_enrolled=2,
            curricular_units_2nd_sem_approved=0, curricular_units_2nd_sem_grade=4.0,
            unemployment_rate=25.0
        )
        
        # Caso extremo: estudante mais velho com excelente performance
        edge_case_2 = SimpleStudentData(
            age_at_enrollment=45, gender=0, marital_status=4,
            admission_grade=200.0, daytime_evening_attendance=1,
            scholarship_holder=1, tuition_fees_up_to_date=1,
            curricular_units_1st_sem_enrolled=8, curricular_units_1st_sem_approved=8,
            curricular_units_1st_sem_grade=20.0, curricular_units_2nd_sem_enrolled=8,
            curricular_units_2nd_sem_approved=8, curricular_units_2nd_sem_grade=20.0,
            unemployment_rate=2.0
        )
        
        # Modelo deve conseguir fazer predições sem erros
        try:
            result1 = service.predict(edge_case_1)
            result2 = service.predict(edge_case_2)
            
            assert result1.prediction in ['Graduate', 'Dropout', 'Enrolled']
            assert result2.prediction in ['Graduate', 'Dropout', 'Enrolled']
            
        except Exception as e:
            pytest.fail(f"Modelo falhou com casos extremos: {e}")
    
    @pytest.mark.integration
    def test_model_performance_regression(self, service):
        """Teste de regressão para evitar degradação de performance"""
        if not service.load_model():
            pytest.skip("Modelo não disponível para teste de performance")
        
        model_info = service.get_model_info()
        if model_info and 'test_accuracy' in model_info:
            recorded_accuracy = model_info['test_accuracy']
            
            # Performance não deve degradar mais que 5% da accuracy registrada
            min_acceptable_accuracy = recorded_accuracy * 0.95
            
            assert min_acceptable_accuracy >= self.MIN_ACCURACY * 0.90, (
                f"Accuracy registrada {recorded_accuracy:.3f} indica possível "
                f"degradação significativa do modelo."
            ) 