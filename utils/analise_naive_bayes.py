import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Carregar os dados
df = pd.read_csv('resultados_completos_classificados.csv')

# Visualizar o início do dataset para validar se os dados foram carregados corretamente
print(df.head())

# Contar a quantidade de ocorrências das classes de A a E no dataset
class_counts = df['CLASSIFICACAO_NOTA'].value_counts().sort_index()
print("Quantidade de ocorrências das classes no dataset:")
print(class_counts)



# Dividir os dados em atributos (X) e a variável alvo (y)
X = df[['BANHEIROS', 'COZINHA', 'LABORATORIO', 'ESPORTE', 'SALAS DE AULA', 'LEITURA', 'OUTROS']]
y = df['CLASSIFICACAO_NOTA']

# Dividir os conjuntos de dados de treinamento e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Criar o classificador Naïve Bayes
nb = GaussianNB()

# Treinar o modelo
nb.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
y_pred = nb.predict(X_test)

# Avaliar a precisão do modelo
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Salva o modelo treinando em um arquivo
dump_modelo = {
    'modelo': nb,
    'accuracy': accuracy
}
joblib.dump(dump_modelo, 'web/modelo_treinado_gaussian_nb.pkl')


# Gerar o relatório de classificação
print('Classification Report:')
print(classification_report(y_test, y_pred))

# Gerar a matriz de confusão
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))