import pandas as pd
import shap
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from mlxtend.frequent_patterns import apriori, association_rules
import seaborn as sns
import joblib

df=pd.read_csv('resultados_completos_classificados.csv')

# Visualizar as primeiras linhas do DataFrame
print(df.head())

# Verificar informações sobre as colunas
print(df.info())

# Verificar estatísticas descritivas das colunas numéricas
print(df.describe())

# Importar LabelEncoder
from sklearn.preprocessing import LabelEncoder

# Inicializar o codificador de rótulos para a variável target 'CLASSIFICACAO_NOTA'
#label_encoder = LabelEncoder() aqui ensino o modelo a interpretar as categorias como numeros

# Codificar as categorias da variável target 'CLASSIFICACAO_NOTA' em valores numéricos
#df['CLASSIFICACAO_NOTA_encoded'] = label_encoder.fit_transform(df['CLASSIFICACAO_NOTA'])

# Separar as features e o target
X = df.drop(['IDESP_AF', 'CLASSIFICACAO_NOTA'], axis=1)  # features
y = df['CLASSIFICACAO_NOTA']  # target categórica (estamos tentando explicar/prever)

# Importar train_test_split
from sklearn.model_selection import train_test_split

# Dividir os dados em conjuntos de treinamento e teste (70% treino, 30% teste)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# Importar DecisionTreeClassifier /tentando prever classe categorica
from sklearn.tree import DecisionTreeClassifier

# Inicializar e treinar o modelo de Árvore de Decisão
model = DecisionTreeClassifier(random_state=42, max_depth=5)
model.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
predictions = model.predict(X_test)

# Avaliar a precisão do modelo
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, predictions)

print("Accuracy:", accuracy)

from sklearn.model_selection import GridSearchCV #tunning de hiperparametros
import shap

# Definir os parâmetros para o ajuste de hiperparâmetros/um dicionario/ busca todas as combinacoes (otimização pesquisa operacional) e me mostra a melhor
param_grid = {
    'max_depth': [5, 10, 15, 20],  # testar diferentes profundidades máximas da árvore
    'min_samples_split': [2, 5, 10],  # testar diferentes números mínimos de amostras necessárias para dividir um nó
    'min_samples_leaf': [1, 2, 4]  # testar diferentes números mínimos de amostras em folhas finais
}

# Inicializar o classificador de Árvore de Decisão ("semente">>random)
dt_classifier = DecisionTreeClassifier(random_state=42)

# Inicializar a pesquisa em grade pega base de treino e divide em 5 e busca melhor combinação pela melhor acuracia
grid_search = GridSearchCV(estimator=dt_classifier, param_grid=param_grid, cv=5, scoring='accuracy')

# Realizar a pesquisa em grade para encontrar os melhores hiperparâmetros
grid_search.fit(X_train, y_train)

# Obter os melhores hiperparâmetros encontrados
best_params = grid_search.best_params_
print("Melhores hiperparâmetros:", best_params)

# Inicializar e treinar o modelo de Árvore de Decisão com os melhores hiperparâmetros
best_model = DecisionTreeClassifier(**best_params, random_state=42)
best_model.fit(X_train, y_train)

# Fazer previsões no conjunto de teste
predictions = best_model.predict(X_test)

# Avaliar a precisão do modelo
from sklearn.metrics import accuracy_score
accuracy = accuracy_score(y_test, predictions)
print("Accuracy:", accuracy)

dump_modelo = {
    'modelo': best_model,
    'accuracy': accuracy
}
joblib.dump(dump_modelo, 'web/modelo_treinado_decision_tree_classifier.pkl')

from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

# Plotar a árvore de decisão
plt.figure(figsize=(10,20))  # Definir o tamanho da figura
plot_tree(best_model, feature_names=X_train.columns, class_names=y_train.unique(), filled=True, fontsize=10)
plt.show()

# Calcular os SHAP values para interpretabilidade do modelo
explainer = shap.TreeExplainer(best_model)
shap_values = explainer.shap_values(X_test)

# Selecionar uma amostra de teste para visualização
sample_idx = 0  # Você pode selecionar qualquer índice de amostra que desejar

# Criar um objeto Explanation com os SHAP values calculados para a amostra selecionada
shap_explanation = shap.Explanation(values=shap_values[0][sample_idx], base_values=explainer.expected_value[0], data=X_test.iloc[sample_idx], feature_names=X_test.columns)

# Visualizar o SHAP waterfall plot para a amostra selecionada
shap.plots.waterfall(shap_explanation, max_display=10)  # Plotar o waterfall plot para a amostra selecionada

#interpretação do gráfico:

shap.summary_plot(shap_values, X_test, plot_size=(15, 8),max_display=7) #pedir para prof ajudar a entender o que aconteceu aqui(pode ser que o shap esta sendo usado errado)

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

# Calcular as métricas de classificação binária
accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average='weighted')  # ou average='macro' ou average=None
recall = recall_score(y_test, predictions, average='weighted')  # ou average='macro' ou average=None
f1 = f1_score(y_test, predictions, average='weighted')  # ou average='macro' ou average=None

# Armazenar as métricas em um dicionário (pesquisar como cada métrica é interpretada)
metrics_dict = {
    'Accuracy': accuracy,
    'Precision': precision,
    'Recall': recall,
    'F1 Score': f1,

}
for metric, value in metrics_dict.items():
    print(f"{metric}: {value}")

    #Accuracy: 0.5847216578626575
    #Precision: 0.5922180273860579
    #Recall: 0.5847216578626575
    #F1 Score: 0.5720398220693316

from sklearn.metrics import confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Plotar a matriz de confusão do conjunto de teste (confirmar na documentação se os valores reais estão no eixo X ou Y)
plt.figure(figsize=(8, 6))  # Definir o tamanho da figura
cm = confusion_matrix(y_test, predictions)  # Calculate confusion matrix
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=y_train.unique(), yticklabels=y_train.unique())
plt.title('Matriz de Confusão - Conjunto de Teste')
plt.show()

# Codificar as labels
label_encoder = LabelEncoder()
df['CLASSIFICACAO_NOTA'] = label_encoder.fit_transform(df['CLASSIFICACAO_NOTA'])

# Separar as features e o target
X = df.drop(['IDESP_AF', 'CLASSIFICACAO_NOTA'], axis=1)
y = df['CLASSIFICACAO_NOTA']

# Dividir o dataset em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Inicializar o modelo AdaBoost com DecisionTreeClassifier como base estimator
base_estimator = DecisionTreeClassifier(max_depth=1, random_state=42)
ada_model = AdaBoostClassifier(estimator=base_estimator, n_estimators=50, random_state=42)

# Treinar o modelo
ada_model.fit(X_train, y_train)

# Fazer previsões
y_pred = ada_model.predict(X_test)

# Calcular as métricas de avaliação
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')
recall = recall_score(y_test, y_pred, average='weighted')
f1 = f1_score(y_test, y_pred, average='weighted')
conf_matrix = confusion_matrix(y_test, y_pred)

dump_modelo = {
    'modelo': ada_model,
    'accuracy': accuracy
}
joblib.dump(dump_modelo, 'web/modelo_treinado_ada_boost_classifier.pkl')

# Armazenar as métricas em um dicionário
metrics_dict = {
    'Accuracy': accuracy,
    'Precision': precision,
    'Recall': recall,
    'F1 Score': f1,
    'Confusion Matrix': conf_matrix
}

# Imprimir as métricas
for metric, value in metrics_dict.items():
    if metric != 'Confusion Matrix':
        print(f"{metric}: {value}")

# Plotar a matriz de confusão usando seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Matriz de Confusão - Conjunto de Teste')
plt.show()

# Accuracy: 0.46816580872392305
# Precision: 0.44342866618571475
# Recall: 0.46816580872392305
# F1 Score: 0.44117248803954046

# Definir as variáveis independentes (X) e dependentes (y)
X = df.drop(columns=['IDESP_AF', 'CLASSIFICACAO_NOTA'])
y = df['CLASSIFICACAO_NOTA']

# Transformar a variável dependente em rótulos numéricos
from sklearn.preprocessing import LabelEncoder
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Inicializar o modelo AdaBoost
ada_model = AdaBoostClassifier(random_state=42)

# Avaliar o modelo usando validação cruzada
scores = cross_val_score(ada_model, X, y, cv=5, scoring='accuracy')

# Plotar um gráfico de boxplot para visualizar a distribuição das pontuações
plt.figure(figsize=(8, 6))
sns.boxplot(data=scores, orient='h')
plt.title('Distribuição das Pontuações de Validação Cruzada do Modelo AdaBoost')
plt.xlabel('Acurácia')
plt.show()

# Treinar o modelo AdaBoost no conjunto de dados completo
ada_model.fit(X, y)

# Prever no conjunto de teste (ou conjunto de validação se houver)
y_pred = ada_model.predict(X)

# Calcular a matriz de confusão
from sklearn.metrics import confusion_matrix
conf_matrix = confusion_matrix(y, y_pred)

# Plotar a matriz de confusão
plt.figure(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=label_encoder.classes_, yticklabels=label_encoder.classes_)
plt.xlabel('Predicted labels')
plt.ylabel('True labels')
plt.title('Matriz de Confusão - Conjunto Completo')
plt.show()

# Calcular as métricas de classificação
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

accuracy = accuracy_score(y, y_pred)
precision = precision_score(y, y_pred, average='weighted')
recall = recall_score(y, y_pred, average='weighted')
f1 = f1_score(y, y_pred, average='weighted')

# Como o problema é multiclasse, ROC AUC é calculado de forma diferente
# Vamos precisar das probabilidades de previsão para calcular corretamente
# o ROC AUC para cada classe e tirar a média

roc_auc = roc_auc_score(y, ada_model.predict_proba(X), multi_class='ovr')

# Armazenar as métricas em um dicionário
metrics_dict = {
    'Accuracy': accuracy,
    'Precision': precision,
    'Recall': recall,
    'F1 Score': f1,
    'ROC AUC Score': roc_auc,
    'Confusion Matrix': conf_matrix
}

# Imprimir as métricas
for metric, value in metrics_dict.items():
    print(f"{metric}: {value}")

# Accuracy: 0.4787415657263637
# Precision: 0.47151970294112866
# Recall: 0.4787415657263637
# F1 Score: 0.4469985823827921
# ROC AUC Score: 0.61225439467249
# Confusion Matrix: [[   0    0   17    4    1]
#  [   0    4  290   67    8]
#  [   3    2 3038 2143   44]
#  [   6    0 2345 2786   44]
#  [   0    1  822  615   61]]

# Selecionar apenas as colunas de infraestrutura
infra_cols = ['BANHEIROS', 'COZINHA', 'LABORATORIO', 'ESPORTE', 'SALAS DE AULA', 'LEITURA', 'OUTROS']

# Binarizar as colunas de infraestrutura
df_bin = df[infra_cols].applymap(lambda x: 1 if x > 0 else 0)

# Calcular os itens frequentes com o algoritmo Apriori
frequent_items = apriori(df_bin, min_support=0.1, use_colnames=True)

# Gerar as regras de associação
rules = association_rules(frequent_items, metric="lift", min_threshold=1.0)

# Filtrar as regras mais relevantes
rules = rules[(rules['confidence'] > 0.6) & (rules['lift'] > 1.2)]

# Exibir as regras de associação
print(rules)

# Visualizar as regras de associação
plt.figure(figsize=(14, 10))
sns.barplot(x="support", y="confidence", data=rules)
plt.title('Regras de Associação')
plt.xlabel('Suporte')
plt.ylabel('Confiança')
plt.show()