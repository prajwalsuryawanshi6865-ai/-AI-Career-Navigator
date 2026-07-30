import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_absolute_error, r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC, SVR
from xgboost import XGBClassifier, XGBRegressor
import os

def train_and_evaluate():
    data_path = 'data/dataset.csv'
    if not os.path.exists(data_path):
        print(f"Dataset not found at {data_path}. Please generate it first.")
        return

    df = pd.read_csv(data_path)
    
    # Features
    X = df[['CGPA', 'Attendance', 'Aptitude_Score', 'Coding_Score', 'Communication_Score', 'Number_of_Projects']]
    
    # Targets
    y_placement = df['Placed']
    y_salary = df['Salary']
    
    print("--- Training Placement Models (Classification) ---")
    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(X, y_placement, test_size=0.2, random_state=42)
    
    classifiers = {
        'Logistic Regression': LogisticRegression(max_iter=1000),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'XGBoost': XGBClassifier(eval_metric='logloss', random_state=42),
        'SVM': SVC(probability=True, random_state=42)
    }
    
    best_clf = None
    best_clf_name = ""
    best_clf_acc = 0
    
    clf_results = []
    
    for name, clf in classifiers.items():
        clf.fit(X_train_c, y_train_c)
        y_pred = clf.predict(X_test_c)
        acc = accuracy_score(y_test_c, y_pred)
        clf_results.append({'Model': name, 'Accuracy': acc})
        print(f"{name} Accuracy: {acc:.4f}")
        
        if acc > best_clf_acc:
            best_clf_acc = acc
            best_clf = clf
            best_clf_name = name
            
    print(f"\nBest Classifier: {best_clf_name} with Accuracy {best_clf_acc:.4f}")
    joblib.dump(best_clf, 'models/best_placement_model.pkl')
    
    # Save classifier results to display in dashboard
    pd.DataFrame(clf_results).to_csv('models/clf_metrics.csv', index=False)
    
    print("\n--- Training Salary Models (Regression) ---")
    # Only train salary on placed candidates, or train on all?
    # Usually, we want to predict expected salary if placed.
    # We will use all rows where Placed == 1
    placed_df = df[df['Placed'] == 1]
    X_reg = placed_df[['CGPA', 'Attendance', 'Aptitude_Score', 'Coding_Score', 'Communication_Score', 'Number_of_Projects']]
    y_reg = placed_df['Salary']
    
    X_train_r, X_test_r, y_train_r, y_test_r = train_test_split(X_reg, y_reg, test_size=0.2, random_state=42)
    
    regressors = {
        'Linear Regression': LinearRegression(),
        'Decision Tree': DecisionTreeRegressor(random_state=42),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'XGBoost': XGBRegressor(random_state=42),
        'SVM': SVR()
    }
    
    best_reg = None
    best_reg_name = ""
    best_reg_r2 = -float('inf')
    
    reg_results = []
    
    for name, reg in regressors.items():
        reg.fit(X_train_r, y_train_r)
        y_pred = reg.predict(X_test_r)
        r2 = r2_score(y_test_r, y_pred)
        mae = mean_absolute_error(y_test_r, y_pred)
        reg_results.append({'Model': name, 'R2_Score': r2, 'MAE': mae})
        print(f"{name} R2: {r2:.4f}, MAE: {mae:.2f}")
        
        if r2 > best_reg_r2:
            best_reg_r2 = r2
            best_reg = reg
            best_reg_name = name
            
    print(f"\nBest Regressor: {best_reg_name} with R2 {best_reg_r2:.4f}")
    joblib.dump(best_reg, 'models/best_salary_model.pkl')
    
    pd.DataFrame(reg_results).to_csv('models/reg_metrics.csv', index=False)
    print("Models saved successfully in models/")

if __name__ == "__main__":
    train_and_evaluate()
