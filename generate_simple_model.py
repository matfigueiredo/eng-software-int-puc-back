import warnings

import joblib
import pandas as pd
from sklearn.base import clone
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

def load_and_prepare_simple_data():
    """Load and prepare the dataset with selected features only"""
    url = "https://raw.githubusercontent.com/matfigueiredo/student-dropout-mvp/refs/heads/master/data.csv"
    dataset = pd.read_csv(url, delimiter=';')
    
    # Clean column names
    dataset.columns = dataset.columns.str.strip()
    if 'Daytime/evening attendance\t' in dataset.columns:
        dataset = dataset.rename(columns={'Daytime/evening attendance\t': 'Daytime/evening attendance'})
    
    # Select only the most important and interpretable features
    selected_features = [
        # Personal Information (3 features)
        'Age at enrollment',
        'Gender',
        'Marital status',
        
        # Academic Information (2 features)
        'Admission grade',
        'Daytime/evening attendance',
        
        # Financial Status (2 features)
        'Scholarship holder',
        'Tuition fees up to date',
        
        # 1st Semester Performance (3 features)
        'Curricular units 1st sem (enrolled)',
        'Curricular units 1st sem (approved)',
        'Curricular units 1st sem (grade)',
        
        # 2nd Semester Performance (3 features)
        'Curricular units 2nd sem (enrolled)',
        'Curricular units 2nd sem (approved)',
        'Curricular units 2nd sem (grade)',
        
        # Economic Context (1 feature)
        'Unemployment rate'
    ]
    
    # Filter dataset to include only selected features + target
    X = dataset[selected_features]
    y = dataset['Target']
    
    print(f"Original dataset: {dataset.shape}")
    print(f"Simplified dataset: {X.shape}")
    print(f"Selected features: {len(selected_features)}")
    print("\nSelected features:")
    for i, feature in enumerate(selected_features, 1):
        print(f"{i:2d}. {feature}")
    
    return X, y, selected_features

def train_and_save_simple_model():
    """Train the simplified model and save it"""
    print("🔄 Loading and preparing simplified data...")
    X, y, feature_names = load_and_prepare_simple_data()
    
    print("\n📊 Dataset Info:")
    print(f"- Total samples: {len(X)}")
    print(f"- Features: {len(feature_names)}")
    print(f"- Target distribution:\n{y.value_counts()}")
    
    print("\n🤖 Training simplified models...")
    
    # Split data for evaluation
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # Define models with pipelines
    models = {
        'SVM': Pipeline([
            ('StandardScaler', StandardScaler()),
            ('SVM', SVC(random_state=42, probability=True))  # Enable probability for confidence
        ]),
        'KNN': Pipeline([
            ('StandardScaler', StandardScaler()),
            ('KNN', KNeighborsClassifier())
        ]),
        'CART': Pipeline([
            ('StandardScaler', StandardScaler()),
            ('CART', DecisionTreeClassifier(random_state=42))
        ]),
        'NB': Pipeline([
            ('StandardScaler', StandardScaler()),
            ('NB', GaussianNB())
        ])
    }
    
    # Simplified grid search parameters
    param_grids = {
        'SVM': {
            'SVM__C': [0.1, 1, 10],
            'SVM__kernel': ['linear', 'rbf']
        },
        'KNN': {
            'KNN__n_neighbors': [3, 5, 7, 9]
        },
        'CART': {
            'CART__max_depth': [5, 10, None],
            'CART__min_samples_split': [2, 5, 10]
        },
        'NB': {
            'NB__var_smoothing': [1e-9, 1e-6, 1e-3]
        }
    }
    
    best_models = {}
    
    # Train and optimize each model
    for name, model in models.items():
        print(f"🔧 Optimizing {name}...")
        grid_search = GridSearchCV(
            model, 
            param_grids[name], 
            cv=5, 
            scoring='accuracy',
            n_jobs=-1
        )
        grid_search.fit(X_train, y_train)
        best_models[name] = (grid_search.best_score_, grid_search.best_estimator_)
        print(f"   ✅ {name} - Best score: {grid_search.best_score_:.4f}")
    
    # Select best model
    best_model_name = max(best_models.keys(), key=lambda k: best_models[k][0])
    best_model_score = best_models[best_model_name][0]
    best_model = best_models[best_model_name][1]
    
    print(f"\n🏆 Best model: {best_model_name} (Score: {best_model_score:.4f})")
    
    # Train final model with full dataset
    model_final = clone(best_model)
    model_final.fit(X, y)
    
    # Test accuracy
    y_pred = best_model.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    
    print("\n📈 Final Results:")
    print(f"- Cross-validation score: {best_model_score:.4f}")
    print(f"- Test accuracy: {test_accuracy:.4f}")
    
    # Save simplified model
    joblib.dump(model_final, 'student_dropout_simple_model.pkl')
    
    # Save model info
    model_info = {
        'model_name': best_model_name,
        'model_score': best_model_score,
        'test_accuracy': test_accuracy,
        'feature_names': feature_names,
        'classes': list(model_final.classes_),
        'is_simplified': True,
        'feature_count': len(feature_names)
    }
    joblib.dump(model_info, 'student_dropout_simple_model_info.pkl')
    
    print("\n💾 Simplified model saved successfully!")
    print("- student_dropout_simple_model.pkl")
    print("- student_dropout_simple_model_info.pkl")
    print(f"- Features: {len(feature_names)} (reduced from 36)")
    
    # Show feature importance if possible
    if hasattr(model_final.named_steps.get('CART', None), 'feature_importances_'):
        print("\n📊 Feature Importance (CART):")
        importances = model_final.named_steps['CART'].feature_importances_
        feature_importance = list(zip(feature_names, importances))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        for i, (feature, importance) in enumerate(feature_importance[:10], 1):
            print(f"{i:2d}. {feature}: {importance:.4f}")
    
    return model_final, model_info

if __name__ == "__main__":
    print("🚀 Starting simplified model training...")
    train_and_save_simple_model()
    print("\n✅ Simplified model ready for production!") 