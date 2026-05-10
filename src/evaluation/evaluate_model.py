import joblib
from sklearn.metrics import accuracy_score

def evaluate(model_path, X_test, y_test):
    model = joblib.load(model_path)
    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print("Model Accuracy:", acc)