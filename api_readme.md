# Student Dropout Prediction API

API para predição de dropout, matrícula ou graduação de estudantes usando Machine Learning.

- Modelo otimizado com apenas campos essenciais e intuitivos
- API: `main.py` (porta 8000)
- Frontend: `frontend/`

---

## 🎯 Como usar - Versão Simplificada

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Gerar o modelo simplificado

```bash
python generate_simple_model.py
```

Este script vai:
- Baixar os dados do GitHub
- Selecionar apenas 14 campos essenciais e intuitivos
- Treinar diferentes modelos (KNN, CART, SVM, Naive Bayes)
- Selecionar o melhor modelo
- Salvar os arquivos pickle (`student_dropout_simple_model.pkl` e `student_dropout_simple_model_info.pkl`)

### 3. Executar a API simplificada

```bash
python main.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

A API estará disponível em: http://localhost:8001

### 4. Usar o frontend simplificado

Abra o arquivo `frontend/index.html` no navegador ou use um servidor local:

```bash
# Abrir frontend/index.html diretamente
# Ou usar servidor local
cd frontend
python -m http.server 8080
```

---

## 📋 Campos do Modelo Simplificado

### **👤 Informações Pessoais (3 campos)**
- `age_at_enrollment`: Idade na matrícula (16-80)
- `gender`: Gênero (0=Feminino, 1=Masculino)
- `marital_status`: Estado civil (1=Solteiro, 2=Casado, 3=Divorciado, 4=Viúvo)

### **🎯 Informações Acadêmicas (2 campos)**
- `admission_grade`: Nota de admissão (0-200)
- `daytime_evening_attendance`: Período (0=Noturno, 1=Diurno)

### **💰 Situação Financeira (2 campos)**
- `scholarship_holder`: Bolsa de estudos (0=Não, 1=Sim)
- `tuition_fees_up_to_date`: Mensalidades em dia (0=Não, 1=Sim)

### **📈 Desempenho 1º Semestre (3 campos)**
- `curricular_units_1st_sem_enrolled`: Matérias matriculadas
- `curricular_units_1st_sem_approved`: Matérias aprovadas
- `curricular_units_1st_sem_grade`: Nota média (0-20)

### **📊 Desempenho 2º Semestre (3 campos)**
- `curricular_units_2nd_sem_enrolled`: Matérias matriculadas
- `curricular_units_2nd_sem_approved`: Matérias aprovadas
- `curricular_units_2nd_sem_grade`: Nota média (0-20)

### **📈 Contexto Econômico (1 campo)**
- `unemployment_rate`: Taxa de desemprego (%)

---

## 🌐 Endpoints da API

### GET `/`
Retorna status da API e informações do modelo.

### GET `/model-info`
Retorna informações detalhadas sobre o modelo simplificado.

### GET `/features`
Lista todos os campos com descrições detalhadas.

### POST `/predict`
Faz predição para um estudante. Requer apenas 14 parâmetros.

### POST `/predict-example`
Faz predição usando dados de exemplo simplificados (para testes).

---

## 💻 Exemplo de uso da API

```python
import requests

# Dados simplificados do estudante
student_data = {
    # Informações Pessoais
    "age_at_enrollment": 18,
    "gender": 0,  # Feminino
    "marital_status": 1,  # Solteiro
    
    # Informações Acadêmicas
    "admission_grade": 140.0,
    "daytime_evening_attendance": 1,  # Diurno
    
    # Situação Financeira
    "scholarship_holder": 1,  # Sim
    "tuition_fees_up_to_date": 1,  # Sim
    
    # Desempenho 1º Semestre
    "curricular_units_1st_sem_enrolled": 8,
    "curricular_units_1st_sem_approved": 8,
    "curricular_units_1st_sem_grade": 14.0,
    
    # Desempenho 2º Semestre
    "curricular_units_2nd_sem_enrolled": 8,
    "curricular_units_2nd_sem_approved": 8,
    "curricular_units_2nd_sem_grade": 14.5,
    
    # Contexto Econômico
    "unemployment_rate": 10.8
}

# Fazer predição
response = requests.post("http://localhost:8001/predict", json=student_data)
result = response.json()

print(f"Predição: {result['prediction']}")
print(f"Confiança: {result['confidence']}")
print(f"Modelo: {result['model_info']['model_name']}")
```