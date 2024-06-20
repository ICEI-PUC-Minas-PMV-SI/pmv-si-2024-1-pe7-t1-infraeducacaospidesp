import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import accuracy_score
import joblib

df = pd.read_csv('resultados_completos_classificados.csv')

df.sample(5)

df.count()

df.isna().sum()

df["CLASSIFICACAO_NOTA"]=df["CLASSIFICACAO_NOTA"].replace(to_replace=['A', 'B', 'C', 'D', 'E'], value=[1, 2, 3, 4, 5])

df.head()

plt.hist(df['BANHEIROS'], bins=5)
plt.title('Distribuição de Banheiros')
plt.show()

plt.hist(df['COZINHA'], bins=5)
plt.title('Distribuição de Cozinha')
plt.show()

plt.hist(df['LABORATORIO'], bins=5)
plt.title('Distribuição de Laboratórios')
plt.show()

plt.hist(df['ESPORTE'], bins=5)
plt.title('Distribuição de salas de esporte')
plt.show()

plt.hist(df['SALAS DE AULA'], bins=5)
plt.title('Distribuição de salas de aula')
plt.show()

plt.hist(df['LEITURA'], bins=5)
plt.title('Distribuição de salas de leitura')
plt.show()

plt.hist(df['OUTROS'], bins=5)
plt.title('Distribuição de salas para outros fins')
plt.show()

plt.hist(df['IDESP_AF'], bins=5)
plt.title('Distribuição de notas do idesp AF')
plt.show()


df.corr()

sns.heatmap(df.corr(), cmap='coolwarm', annot=True)

plt.show()

df.corr()['CLASSIFICACAO_NOTA'].sort_values()

x = df.drop(['CLASSIFICACAO_NOTA','IDESP_AF'], axis = 1)
y = df['IDESP_AF']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 100)

mlr = LinearRegression()  
mlr.fit(x_train, y_train)

print("Intercept: ", mlr.intercept_)
print("Coefficients:")
list(zip(x, mlr.coef_))

y_pred_mlr= mlr.predict(x_test)

# Definir um limiar de erro (por exemplo, 0.5)
limiar_erro = 0.5

# Converter previsões em valores binários (correto/incorreto)
y_pred_binario = np.abs(y_pred_mlr - y_test) < limiar_erro

# Converter y_test para binário (verdadeiro, todos são corretos)
y_test_binario = np.ones_like(y_test, dtype=bool)

# Calcular a "acurácia"
accuracy = accuracy_score(y_test_binario, y_pred_binario)

dump_modelo = {
    'modelo': mlr,
    'accuracy': accuracy
}
joblib.dump(dump_modelo, 'web/modelo_treinado_linear_regression.pkl')

print(y_pred_mlr)

sns.regplot(x=y_test,y=y_pred_mlr,ci=None,color ='red',line_kws={"color": "black"})
plt.show()

meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
rootMeanSqErr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))
print('R squared: {:.2f}'.format(mlr.score(x,y)*100))
print('Mean Absolute Error:', meanAbErr)
print('Mean Square Error:', meanSqErr)
print('Root Mean Square Error:', rootMeanSqErr)

Classificacao_Nota_Index= mlr.predict([[3,3,2,2,18,1,8]])
print(Classificacao_Nota_Index)