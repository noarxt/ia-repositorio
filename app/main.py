from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import joblib
import os

data = load_iris()
X = data.data
y = data.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)


predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"✅ Acurácia do modelo: {accuracy:.2f}")


caminho_modelo = os.path.join(os.path.dirname(__file__), "..", "models", "meu_modelo.pkl")
joblib.dump(model, caminho_modelo)
print("💾 Modelo salvo em: models/meu_modelo.pkl")