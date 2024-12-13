# Importar librerías necesarias
from datasets import load_dataset
import pandas as pd
import numpy as np  # Agregamos la importación de numpy
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, accuracy_score
from urllib.parse import urlparse

# Cargar el dataset desde Hugging Face
dataset = load_dataset('bgspaditya/byt-mal-minpro', split='train')

# Convertir a DataFrame de pandas
df = pd.DataFrame(dataset)

# Inspeccionar los nombres de las columnas
print(df.columns)

# Asegurarse de que los nombres de las columnas son correctos
print(df.head())

# Función para extraer características de la URL
def extraer_caracteristicas(url):
    parsed_url = urlparse(url)
    return {
        'longitud_url': len(url),
        'longitud_dominio': len(parsed_url.netloc),
        'tiene_subdominio': 1 if len(parsed_url.netloc.split('.')) > 2 else 0,
        'es_https': 1 if parsed_url.scheme == 'https' else 0
    }

# Aplicar la función a todas las URLs del dataset
features = df['url'].apply(extraer_caracteristicas)
features_df = pd.json_normalize(features)

# Vectorizar las URLs
vectorizer = TfidfVectorizer(max_features=1000)  # Limitar las características a 1000 para reducir uso de memoria
url_vectorized = vectorizer.fit_transform(df['url'])

# Combinar todas las características en un solo DataFrame
X = np.hstack([features_df.values, url_vectorized.toarray()])
y = df['type_code']  # Asegurarse de usar el nombre correcto de la columna

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Entrenar el modelo de árbol de decisión
clf = DecisionTreeClassifier()
clf.fit(X_train, y_train)

# Realizar predicciones
y_pred = clf.predict(X_test)

# Evaluar el modelo
print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))

# Ejemplo de predicción con nuevas URLs
nuevas_urls = ["http://example.com", "http://phishingsite.com"]
nuevas_features = pd.json_normalize([extraer_caracteristicas(url) for url in nuevas_urls])
nuevas_url_vectorized = vectorizer.transform(nuevas_urls)

# Combinar todas las características de las nuevas URLs
nuevas_X = np.hstack([nuevas_features.values, nuevas_url_vectorized.toarray()])

# Realizar predicciones con las nuevas URLs
predicciones = clf.predict(nuevas_X)
print(predicciones)
