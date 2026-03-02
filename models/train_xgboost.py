"""
XGBoost Model Training Script for PMGSY Scheme Classification

This script trains an offline backup model that can be used when IBM Cloud ML
is unavailable. The model uses XGBoost with a preprocessing pipeline.

Usage:
    python -m models.train_xgboost
    
    Or from project root:
    python models/train_xgboost.py

Output:
    - models/pmgsy_xgboost_model.pkl (trained pipeline)
    - models/label_encoder.pkl (target encoder)
    - models/training_report.txt (metrics and info)
"""

import os
import sys
import pickle
import warnings
from datetime import datetime

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score, 
    classification_report, 
    confusion_matrix,
    f1_score
)
from xgboost import XGBClassifier

# Suppress warnings
warnings.filterwarnings('ignore')

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, "data", "PMGSY_DATASET.csv")
MODEL_PATH = os.path.join(SCRIPT_DIR, "pmgsy_xgboost_model.pkl")
ENCODER_PATH = os.path.join(SCRIPT_DIR, "label_encoder.pkl")
REPORT_PATH = os.path.join(SCRIPT_DIR, "training_report.txt")
IMPORTANCE_PATH = os.path.join(SCRIPT_DIR, "feature_importance.png")


def load_data():
    """Load and prepare the dataset."""
    print("📂 Loading dataset...")
    df = pd.read_csv(DATA_PATH)
    
    # Clean column names (remove trailing spaces)
    df.columns = df.columns.str.strip()
    
    # Drop empty/unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    
    print(f"   ✓ Loaded {len(df)} records")
    print(f"   ✓ Columns: {list(df.columns)}")
    
    return df


def analyze_data(df):
    """Analyze dataset for class imbalance and statistics."""
    print("\n📊 Dataset Analysis:")
    print("-" * 40)
    
    # Target distribution
    print("\n🎯 Target Distribution (PMGSY_SCHEME):")
    scheme_counts = df["PMGSY_SCHEME"].value_counts()
    for scheme, count in scheme_counts.items():
        pct = count / len(df) * 100
        print(f"   {scheme}: {count} ({pct:.1f}%)")
    
    # Check for imbalance
    imbalance_ratio = scheme_counts.max() / scheme_counts.min()
    print(f"\n   ⚖️ Imbalance Ratio: {imbalance_ratio:.2f}x")
    
    if imbalance_ratio > 3:
        print("   ⚠️ Significant class imbalance detected!")
    
    # Feature info
    print(f"\n📋 Features: {len(df.columns) - 1}")
    print(f"   Categorical: STATE_NAME, DISTRICT_NAME")
    print(f"   Numerical: {len(df.columns) - 3} columns")
    
    return scheme_counts


def prepare_features(df):
    """Prepare features and target for training."""
    print("\n🔧 Preparing features...")
    
    # Target
    y = df["PMGSY_SCHEME"]
    
    # Features (drop target)
    X = df.drop("PMGSY_SCHEME", axis=1)
    
    # Encode target
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    print(f"   ✓ Target classes: {list(le.classes_)}")
    print(f"   ✓ Encoded as: {list(range(len(le.classes_)))}")
    
    # Define column types
    cat_cols = ["STATE_NAME", "DISTRICT_NAME"]
    num_cols = [col for col in X.columns if col not in cat_cols]
    
    print(f"   ✓ Categorical columns: {cat_cols}")
    print(f"   ✓ Numerical columns: {len(num_cols)}")
    
    return X, y_encoded, le, cat_cols, num_cols


def create_pipeline(cat_cols, num_cols, use_tuning=True):
    """Create preprocessing and model pipeline."""
    print("\n🏗️ Creating pipeline...")
    
    # Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cat_cols),
            ("num", "passthrough", num_cols)
        ]
    )
    
    # Base model configuration
    base_params = {
        "objective": "multi:softprob",
        "eval_metric": "mlogloss",
        "n_estimators": 300,
        "learning_rate": 0.05,
        "max_depth": 6,
        "min_child_weight": 1,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "random_state": 42,
        "n_jobs": -1
    }
    
    model = XGBClassifier(**base_params)
    
    # Full pipeline
    pipeline = Pipeline(steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])
    
    print("   ✓ Pipeline created: Preprocessor → XGBClassifier")
    
    return pipeline


def train_with_tuning(pipeline, X_train, y_train):
    """Train with hyperparameter tuning using GridSearchCV."""
    print("\n🔍 Hyperparameter Tuning (GridSearchCV)...")
    print("   This may take a few minutes...")
    
    param_grid = {
        "model__n_estimators": [200, 300],
        "model__max_depth": [4, 6, 8],
        "model__learning_rate": [0.01, 0.05, 0.1]
    }
    
    grid = GridSearchCV(
        pipeline, 
        param_grid, 
        cv=3, 
        scoring="accuracy",
        verbose=1,
        n_jobs=-1
    )
    
    grid.fit(X_train, y_train)
    
    print(f"\n   ✓ Best Parameters: {grid.best_params_}")
    print(f"   ✓ Best CV Score: {grid.best_score_:.4f}")
    
    return grid.best_estimator_, grid.best_params_, grid.best_score_


def train_simple(pipeline, X_train, y_train):
    """Train without tuning for faster execution."""
    print("\n🚀 Training model (no tuning)...")
    
    pipeline.fit(X_train, y_train)
    
    # Cross-validation score
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=3, scoring="accuracy")
    cv_mean = cv_scores.mean()
    
    print(f"   ✓ Cross-validation scores: {cv_scores}")
    print(f"   ✓ Mean CV Score: {cv_mean:.4f}")
    
    return pipeline, {}, cv_mean


def evaluate_model(pipeline, X_test, y_test, le):
    """Evaluate model performance."""
    print("\n📈 Evaluating model...")
    
    # Predictions
    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)
    
    # Metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    print(f"\n   🎯 Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"   🎯 Weighted F1 Score: {f1:.4f}")
    
    # Classification report
    print("\n📋 Classification Report:")
    print("-" * 60)
    report = classification_report(
        y_test, y_pred, 
        target_names=le.classes_,
        digits=4
    )
    print(report)
    
    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    print("\n🔢 Confusion Matrix:")
    print(cm)
    
    return accuracy, f1, report, cm


def plot_feature_importance(pipeline, cat_cols, num_cols):
    """Generate and save feature importance plot."""
    print("\n📊 Generating feature importance plot...")
    
    try:
        # Get the trained model from pipeline
        model = pipeline.named_steps["model"]
        preprocessor = pipeline.named_steps["preprocessor"]
        
        # Get feature names after preprocessing
        cat_encoder = preprocessor.named_transformers_["cat"]
        cat_feature_names = list(cat_encoder.get_feature_names_out(cat_cols))
        feature_names = cat_feature_names + num_cols
        
        # Get importance
        importance = model.feature_importances_
        
        # Sort by importance
        indices = np.argsort(importance)[::-1][:20]  # Top 20
        
        # Plot
        plt.figure(figsize=(12, 8))
        plt.title("Top 20 Feature Importance", fontsize=14, fontweight='bold')
        plt.bar(range(len(indices)), importance[indices], color='steelblue')
        plt.xticks(range(len(indices)), [feature_names[i] for i in indices], rotation=45, ha='right')
        plt.xlabel("Features")
        plt.ylabel("Importance Score")
        plt.tight_layout()
        plt.savefig(IMPORTANCE_PATH, dpi=150)
        plt.close()
        
        print(f"   ✓ Saved to: {IMPORTANCE_PATH}")
        
        # Print top 10
        print("\n   🏆 Top 10 Features:")
        for i, idx in enumerate(indices[:10]):
            print(f"      {i+1}. {feature_names[idx]}: {importance[idx]:.4f}")
            
    except Exception as e:
        print(f"   ⚠️ Could not generate plot: {e}")


def save_model(pipeline, le, best_params, accuracy, cv_score):
    """Save trained model and artifacts."""
    print("\n💾 Saving model artifacts...")
    
    # Save pipeline
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(pipeline, f)
    print(f"   ✓ Model saved: {MODEL_PATH}")
    
    # Save label encoder
    with open(ENCODER_PATH, 'wb') as f:
        pickle.dump(le, f)
    print(f"   ✓ Label encoder saved: {ENCODER_PATH}")
    
    # Save training report
    report_content = f"""
================================================================================
PMGSY XGBoost Model Training Report
================================================================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Model: XGBoost Classifier with OneHotEncoder preprocessing
Target: PMGSY_SCHEME (Multi-class Classification)

Classes: {list(le.classes_)}

Performance Metrics:
  - Test Accuracy: {accuracy:.4f} ({accuracy*100:.2f}%)
  - Cross-Validation Score: {cv_score:.4f}

Best Hyperparameters: {best_params if best_params else 'Default'}

Files Generated:
  - pmgsy_xgboost_model.pkl (Trained pipeline)
  - label_encoder.pkl (Target encoder)
  - feature_importance.png (Feature importance visualization)

Usage:
  from models import OfflinePredictor
  predictor = OfflinePredictor()
  result = predictor.predict(state, district, ...)

================================================================================
"""
    
    with open(REPORT_PATH, 'w') as f:
        f.write(report_content)
    print(f"   ✓ Report saved: {REPORT_PATH}")


def main():
    """Main training workflow."""
    print("=" * 60)
    print("🚀 PMGSY XGBoost Model Training")
    print("=" * 60)
    
    # Check if data exists
    if not os.path.exists(DATA_PATH):
        print(f"\n❌ Error: Dataset not found at {DATA_PATH}")
        sys.exit(1)
    
    # Load and analyze data
    df = load_data()
    analyze_data(df)
    
    # Prepare features
    X, y, le, cat_cols, num_cols = prepare_features(df)
    
    # Split data
    print("\n📊 Splitting data (80% train, 20% test)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=0.2, 
        random_state=42, 
        stratify=y
    )
    print(f"   ✓ Training samples: {len(X_train)}")
    print(f"   ✓ Test samples: {len(X_test)}")
    
    # Create pipeline
    pipeline = create_pipeline(cat_cols, num_cols)
    
    # Train (with or without tuning)
    use_tuning = True  # Set to False for faster training
    
    if use_tuning:
        trained_pipeline, best_params, cv_score = train_with_tuning(
            pipeline, X_train, y_train
        )
    else:
        trained_pipeline, best_params, cv_score = train_simple(
            pipeline, X_train, y_train
        )
    
    # Evaluate
    accuracy, f1, report, cm = evaluate_model(
        trained_pipeline, X_test, y_test, le
    )
    
    # Feature importance
    plot_feature_importance(trained_pipeline, cat_cols, num_cols)
    
    # Save
    save_model(trained_pipeline, le, best_params, accuracy, cv_score)
    
    print("\n" + "=" * 60)
    print("✅ Training Complete!")
    print(f"   Model Accuracy: {accuracy*100:.2f}%")
    print("=" * 60)
    
    return trained_pipeline, le, accuracy


if __name__ == "__main__":
    main()
