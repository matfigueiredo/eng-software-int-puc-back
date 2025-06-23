# Student Dropout Prediction System

Sistema completo de predição de evasão estudantil desenvolvido como MVP para o curso de Engenharia de Software da PUC.

## Visão Geral

Este projeto implementa uma solução full-stack para predição de evasão estudantil, incluindo:
- Modelo de Machine Learning treinado e validado
- API REST para integração
- Interface web para interação
- Testes automatizados de qualidade

## Estrutura do Projeto

```
eng-software-int-puc-back/
├── notebooks/                  # Jupyter notebook com desenvolvimento do modelo
├── models/                     # Schemas e estruturas de dados
├── services/                   # Lógica de negócio
├── routers/                    # Endpoints da API
├── frontend/                   # Interface web
├── test/                       # Testes automatizados
├── core/                       # Configuração da aplicação
├── utils/                      # Utilitários e validações
├── requirements.txt            # Dependências Python
├── main.py                     # Ponto de entrada da aplicação
└── generate_simple_model.py    # Script de geração do modelo
```

## Requisitos do Sistema

- Python 3.8+
- Flask
- Scikit-learn
- Pandas
- Numpy
- Pytest

## Instalação e Execução

### 1. Clonar o Repositório
```bash
git clone <https://github.com/matfigueiredo/eng-software-int-puc-back>
cd eng-software-int-puc-back
```

### 2. Criar Ambiente Virtual (Recomendado)
```bash
python -m venv .venv

# Linux/Mac
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 4. Gerar o Modelo de Machine Learning
```bash
python generate_simple_model.py
```

### 5. Executar a Aplicação
```bash
python main.py
```

A aplicação estará disponível em: `http://localhost:5000`

Abra o arquivo frontend/index.html para interagir com o frontend da aplicação.

## API Endpoints

### Status da API
- `GET /api/` - Retorna status da aplicação e informações básicas

### Predições
- `POST /api/predict` - Realiza predição baseada nos dados do estudante
- `POST /api/predict-example` - Predição com dados de exemplo

### Informações do Modelo
- `GET /api/model-info` - Retorna informações detalhadas do modelo
- `GET /api/features` - Lista features utilizadas pelo modelo

## Modelo de Machine Learning

O modelo foi desenvolvido seguindo as melhores práticas de ciência de dados:

### Características
- **Algoritmo**: SVM (Support Vector Machine)
- **Features**: 14 variáveis principais relacionadas ao desempenho acadêmico
- **Classes**: Graduate, Dropout, Enrolled
- **Validação**: Cross-validation com GridSearch para otimização de hiperparâmetros

### Performance
- **Cross-validation Score**: 75.6%
- **Test Accuracy**: 75.8%
- **Otimização**: Comparação entre SVM, KNN, Decision Tree e Naive Bayes

## Testes Automatizados

O sistema inclui uma suíte completa de testes:

### Testes Unitários
- **test_prediction_service.py**: Testa lógica de negócio do serviço
- **test_prediction_router.py**: Testa endpoints da API
- **test_schemas.py**: Testa estruturas de dados

### Testes de Performance do Modelo
- **test_model_performance.py**: Valida qualidade e performance do modelo
- Thresholds definidos para accuracy, precision, recall e F1-score
- Proteção contra degradação de performance

### Execução dos Testes
```bash
# Todos os testes
pytest test/ -v

# Apenas testes de performance
pytest test/test_model_performance.py -v

# Testes de integração
pytest -m integration
```

## Interface Web

Interface simples e intuitiva para:
- Inserção de dados do estudante
- Visualização de predições
- Exibição de probabilidades por classe
- Informações sobre o modelo

## Desenvolvimento

### Arquitetura
- **Backend**: Flask com arquitetura em camadas
- **Frontend**: HTML/CSS/JavaScript vanilla
- **Modelo**: Scikit-learn com serialização via joblib
- **Testes**: Pytest com mocks para isolamento

### Padrões de Código
- Código limpo e bem documentado
- Separação de responsabilidades
- Tratamento adequado de erros
- Logs estruturados

## Notebook de Desenvolvimento

O notebook `Pos_PUC_MVP_Eng_Software.ipynb` contém:
- Análise exploratória dos dados
- Processo completo de desenvolvimento do modelo
- Validação e métricas de performance
- Documentação detalhada de cada etapa

## Arquivos do Modelo

- `student_dropout_simple_model.pkl`: Modelo treinado
- `student_dropout_simple_model_info.pkl`: Metadados e informações