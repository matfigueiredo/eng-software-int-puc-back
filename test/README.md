# Testes Unitários

## Estrutura dos Testes

### test_prediction_service.py
Testes para a classe `PredictionService` que gerencia o modelo de machine learning.

**Métodos testados:**
- `__init__()` - Inicialização do serviço
- `load_model()` - Carregamento do modelo e metadados
- `is_model_loaded()` - Verificação se modelo está carregado
- `get_model_info()` - Obtenção de informações do modelo
- `predict()` - Execução de predições
- `get_features_info()` - Obtenção de informações das features

**Cenários cobertos:**
- Carregamento bem-sucedido do modelo
- Falha no carregamento (arquivos não encontrados)
- Exceções durante carregamento
- Predições com e sem probabilidades
- Validação de estado do modelo

### test_prediction_router.py
Testes para os endpoints HTTP do blueprint `prediction_bp`.

**Endpoints testados:**
- `GET /api/` - Status da API
- `GET /api/model-info` - Informações do modelo
- `POST /api/predict` - Predição de dados
- `OPTIONS /api/predict` - Suporte CORS
- `POST /api/predict-example` - Predição com dados de exemplo
- `GET /api/features` - Lista de features

**Cenários cobertos:**
- Respostas HTTP corretas (200, 400, 503)
- Headers CORS configurados
- Validação de dados de entrada
- Tratamento de erros de validação
- Comportamento com modelo não carregado

### test_schemas.py
Testes para os dataclasses em `models/schemas.py`.

**Classes testadas:**
- `SimpleStudentData` - Dados do estudante
- `PredictionResponse` - Resposta de predição
- `ModelInfo` - Informações do modelo
- `FeatureInfo` - Informação de feature
- `FeaturesResponse` - Lista de features

**Funcionalidades testadas:**
- Serialização (`to_dict()`)
- Deserialização (`from_dict()`)
- Criação de instâncias
- Integridade dos dados

## Configuração

### conftest.py
Configurações compartilhadas dos testes:
- Setup do Python path
- Fixtures de configuração de teste

### pytest.ini
Configuração do pytest no diretório raiz do projeto.

## Execução

```bash
# Executar todos os testes
pytest test/

# Executar com verbosidade
pytest test/ -v

# Executar testes específicos
pytest test/test_prediction_service.py
pytest test/test_prediction_router.py
pytest test/test_schemas.py
```