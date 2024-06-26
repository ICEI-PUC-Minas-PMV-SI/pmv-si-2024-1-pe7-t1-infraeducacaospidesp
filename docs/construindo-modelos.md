## Perguntas das Aulas

### Pensando o problema como orientado a dados, a pergunta orientada a dados é diferente da questão de pesquisa?

Sim, a pergunta orientada a dados ajuda a direcionar a forma de como tratar os dados para nos trazerem respostas a estas perguntas, já a questão de pesquisa é mais direcionada a métodos de investigação sobre o que os dados falam de maneira mais simples, porém, se pode entender que a primeira é em decorrência da segunda, uma vez que a investigação nos leva ao entendimento mais profundo de como esses dados podem ser interpretados e utilizados.

### Outras bases podem ser combinadas (ou são necessárias) com a base selecionada para resolver o problema identificado?

Acreditamos que precisaremos de mais insumos para conseguir entender os motivos de tantos outliers nas nossas análises iniciais (quais insumos utilizar é a grande pergunta).

Não sabemos se precisamos relacionar outras bases e, ao menos por enquanto, não vamos fazer isso porque acreditamos que a metodologia utilizada pode nos dar um direcionamento.

### Como são os dados que serão trabalhados considerando os tipos de dados (qualitativos/quantitativos)?

Nossa base possui muitos dados quantitativos, porém, a questão central abrange o fator de estrutura como um todo, e isso é um quantitativo discreto, pois poderemos explicar se uma escola com uma boa infraestrutura tem melhores notas, essa infraestrutura deve ser classificada em faixas de rating onde transformaremos os dados qualitativos em quantitativos

Nota: A Estruturação disso gerará uma união dos dados e isso pode causar um tipo de erro.

### Prof. Hugo citou alguma medida de estatística descritiva que não foi abordada na Etapa 02?

Sim, citou.
Inclusive, nós não realizamos intervalo nem variância ou desvio padrão, nem cálculo de interquartil.

### Quais foram as técnicas de limpeza e transformação de dados utilizados?

- Tentamos identificar os outliers;
- Exclusão dos Dados faltantes (notas nos anos específicos);
- Fizemos uma verificação por amostragem dos dados que poderiam ser desconsiderados (outras data e etc);
- Agrupamos os atributos de infraestrutura de todos os anos com Normalização via Python.

## Tipos de dados do dataset

O dataset utilizado para construção dos modelos de aprendizado de máquina deste projeto possui os atributos descritos na tabela a seguir, que apresenta os seus respectivos tipos de dados e a descrição da informação correspondente.

|      Atributo      | Informação correspondente                                | Tipo de dado            |
| :----------------: | -------------------------------------------------------- | ----------------------- |
|     BANHEIROS      | quantidade de banheiros da escola                        | Inteiro                 |
|      COZINHA       | quantidade de cozinhas                                   | Inteiro                 |
|    LABORATORIO     | quantidade de laboratórios                               | Inteiro                 |
|      ESPORTE       | quantidade de quadras de esporte                         | Inteiro                 |
|   SALAS DE AULA    | quantidade de salas de aula                              | Inteiro                 |
|       OUTROS       | quantidade de outros itens de infraestrutura             | Inteiro                 |
|      IDESP_AF      | nota da escola para os anos finais do ensino fundamental | Valor númerico contínuo |
| CLASSIFICACAO_NOTA | classe a qual a nota da escola pertence                  | Valor categorico        |

# Preparação dos dados

Os dados utilizados no projeto foram coletados no [Portal da Transparência da educação do Governo do estado de São Paulo](https://dados.educacao.sp.gov.br/dataset/portal-da-transpar%C3%AAncia). Inicialmente, as informações da infraestrutura das escolas e as suas respectivas notas do IDESP estavam em tabelas separadas, já que o dataset disponibilizado pelo governo é composto por diversas informações sobre as escolas separadas em tabelas distintas. Devido ao enfoque dado ao projeto, referente a avaliação da nota do IDESP nos anos finais do ensino fundamental (IDESP_AF) e a influência da infraestrutura das escolas nesses resultados, foram selecionadas as tabelas das notas do IDESP e do mapeamento da infraestrutura das escolas para construção do novo dataset a ser utilizado na execução dos modelos de aprendizado de máquina e a tabela escolas foi utilizada para validação dos códigos das escolas constantes nas tabelas anteriores.

No primeiro tratamento dos dados, as categorias "BANHEIROS", "COZINHA", "LABORATÓRIO", "ESPORTE", "SALAS DE AULA", "LEITURA" e "OUTROS", que correspondiam a linhas na tabela de infraestrutura, foram separadas e transformadas em colunas com as suas respectivas quantidades por escolas para compor o novo dataset. As linhas com valores nulos para o IDESP_AF foram excluídas e também foram eliminadas as informações de datas, notas do IDESP_EM e IDESP_AI e o código da escola. O dataset resultante contemplou com a contabilização dos itens de infraestrutura e a nota IDESP_AF por escola.

Após alguns experimentos com o dataset construído inicialmente e devido às dúvidas apresentadas em aula, o grupo seguiu a orientação da Professora e realizou uma nova transformação dos dados para que as Notas IDESP_AF, que são o atributo alvo, fossem categorizadas. Por esse motivo foi adotado o método de discretização de dados por largura igual, onde foram definidas as categorias de classificação das notas de A até E, sendo A a categoria das notas mais altas e E a das notas mais baixas. Para a definição do intervalo correspondente a cada classe foram levados em consideração o valor máximo e mínimo das notas e a quantidade total de classes definidas. Como resultado, um novo dataset de nome "resultados_completos_classificados” foi criado com o acréscimo da coluna "CLASSIFICACAO_NOTA".

# Descrição dos modelos

O estudo aqui realizado apresenta a construção de modelos de aprendizado de máquina e um fluxo completo de análise destes dados obtidos. O procedimento abrange desde o consumo dos dados previamente preparados a avaliação e interpretação dos modelos escolhidos. Um conjunto de dados contendo informações sobre infraestrutura escolar e a classificação de notas associadas foi preparado, tratado e disponibilizado aos modelos para realização do estudo.
Foram utilizadas bibliotecas populares como pandas, sklearn, shap, matplotlib, seaborn e mlxtend, dentre outras. Algumas técnicas como ajuste de hiperparâmetros e uso de SHAP values, foram adotadas para explanação e mineração de dados com o algoritmo, sendo aplicadas para garantir a robustez e a interpretabilidade do modelo final.
Após todo o treino dos modelos, realizamos uma análise detalhada dos dados obtidos, ajustamos modelos preditivos e extraímos regras de associação.
Os modelos finais, após esses processos, serão apresentados a seguir.

## Modelo Classificador de Árvore de Decisão, Classificador AdaBoost e Regras de Associação

Esses modelos foram escolhidos, para o arquivo "analise_arvore.py", baseando-se no fato de que, em um muitas análises, eles são usados para tomada de decisão, como seria o fato da tomada de decisão de investir-se mais em infraestrutura das escolas, e por preverem, comumente, valores numéricos com precisão, além desses fatores, por estre projeto se tratar de um projeto baseado em fundamentos explicados durante um semestre letivo, havia o interesse em aplicar regras já vistas nos materiais de estudo do curso.
O modelo final foi baseado nos trabalhos de Pedregosa et al. (2011), Lundberg & Lee (2017) e Agrawal, Imieliński & Swami (1993).

### Importação das bibliotecas necessárias

Inicialmente, foram importadas as bibliotecas necessárias para manipulação e análise de dados, construção de modelos preditivos, visualização e interpretação de resultados.

    import pandas as pd
    import shap
    import matplotlib.pyplot as plt
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score, confusion_matrix
    from sklearn.model_selection import train_test_split
    from sklearn.model_selection import cross_val_score
    from sklearn.preprocessing import LabelEncoder
    from sklearn.ensemble import AdaBoostClassifier
    from sklearn.tree import DecisionTreeClassifier
    from mlxtend.frequent_patterns import apriori, association_rules
    import seaborn as sns
    from sklearn.model_selection import GridSearchCV
    from sklearn.tree import plot_tree

### Carregamento, Visualização Inicial e preparação dos Dados:

Depois das importações, foram feitos os seguintes processos:

Carregamoento do dataset a partir de um arquivo CSV (disponibilizado no repositório) e realização das visualizações iniciais para permitir o entendimento da estrutura dos dados 'resultados_completos_classificados.csv';

Preparação dos dados para a modelagem, com a codificação da variável target CLASSIFICACAO_NOTA em valores numéricos e a separação das features (X) e da target (y).

    X = df.drop(['IDESP_AF', 'CLASSIFICACAO_NOTA'], axis=1)
    y = df['CLASSIFICACAO_NOTA']

### Divisão do Conjunto de Dados

Depois, os dados foram divididos em conjuntos de treinamento e teste, selecionando 80% dos dados para treino e 20% para teste.

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

### Construção e Avaliação do Modelo de Árvore de Decisão

Posteriormente, um modelo de Árvore de Decisão foi inicializado e treinado, avaliando-se sua acurácia.

    model = DecisionTreeClassifier(random_state=42, max_depth=5)
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

### Ajuste de Hiperparâmetros

Foi realuzado o ajuste de hiperparâmetros utilizando GridSearchCV para encontrar a melhor combinação de parâmetros.

    param_grid = {
        'max_depth': [5, 10, 15, 20],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4]
    }
    grid_search = GridSearchCV(estimator=DecisionTreeClassifier(random_state=42), param_grid=param_grid, cv=5, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    best_params = grid_search.best_params_

### Avaliação do Modelo Otimizado

Foi realizado o Re-treino do modelo de Árvore de Decisão com os melhores hiperparâmetros e foi reavaliada a sua acurácia.

    best_model = DecisionTreeClassifier(**best_params, random_state=42)
    best_model.fit(X_train, y_train)
    predictions = best_model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

### Visualização e Interpretação do Modelo

![Figura 8 - Árvore de Decisão ](./img/arvore1.png)

Figura 8 - Árvore de Decisão

![Figura 9 - Shap1 ](./img/shap1.png)

Figura 9 - Shap tipo 1

![Figura 10 - Shap2 ](./img/shap2.png)

Figura 10 - Shap tipo 2

Foram feitos a Plotagem da árvore de decisão e os calculos dos SHAP values para interpretação.

    plt.figure(figsize=(10,20))
    plot_tree(best_model, feature_names=X_train.columns, class_names=y_train.unique(), filled=True, fontsize=10)
    plt.show()
    explainer = shap.TreeExplainer(best_model)
    shap_values = explainer.shap_values(X_test)
    shap.summary_plot(shap_values, X_test, plot_size=(15, 8), max_display=7)

### Cálculo de Métricas de Desempenho

Foram calculadas várias métricas de desempenho, incluindo acurácia, precisão, recall e F1 Score.

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, average='weighted')
    recall = recall_score(y_test, predictions, average='weighted')
    f1 = f1_score(y_test, predictions, average='weighted')

### Plotagem da Matriz de Confusão (img matrizC1)

Foi plotada a matriz de confusão para avaliar o desempenho do modelo.

    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, predictions)
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=y_train.unique(), yticklabels=y_train.unique())
    plt.title('Matriz de Confusão - Conjunto de Teste')
    plt.show()

### Modelagem com AdaBoost

![Figura 11 - Matriz ](./img/matrizC2.png)

Figura 11 - Matriz

O modelo AdaBoost com uma Árvore de Decisão como base estimator e realizamos a validação cruzada foi inicializado.

    base_estimator = DecisionTreeClassifier(max_depth=1, random_state=42)
    ada_model = AdaBoostClassifier(estimator=base_estimator, n_estimators=50, random_state=42)
    ada_model.fit(X_train, y_train)
    y_pred = ada_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

### Mineração de Dados com Apriori

![Figura 12 - Shap2 ](./img/regras1.png)

Figura 12 - Regras

Foi aplicado, ao fim, o algoritmo Apriori para calcular itens frequentes e gerar regras de associação

    infra_cols = ['BANHEIROS', 'COZINHA', 'LABORATORIO', 'ESPORTE', 'SALAS DE AULA', 'LEITURA', 'OUTROS']
    df_bin = df[infra_cols].applymap(lambda x: 1 if x > 0 else 0)
    frequent_items = apriori(df_bin, min_support=0.1, use_colnames=True)
    rules = association_rules(frequent_items, metric="lift", min_threshold=1.0)

## Modelo de Regressão Linear Múltipla

Esse modelo foi escolhido baseando-se em análises feitas por Nepal(2016), que estipulou um bom resultado nas análises feitas entre infraestruturas de escolas e os resultados dos alunos, uma vez que, nesse estudo, ele usou a regressão múltipla para treinar o seu modelo.

O modelo final foi baseado na regressão linear múltipla proposta por Hariharan(2024), em seu código disponível na plataforma Kaggle.

### Importação das bibliotecas necessárias

Aqui, foram importandas as bibliotecas que serão usadas para manipulação de dados (Pandas e NumPy), visualização (Matplotlib e Seaborn) e machine learning (Scikit-Learn).

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.linear_model import LinearRegression
    from sklearn.model_selection import train_test_split
    from sklearn import metrics

### Carregamento do dataset

Carregou-se os dados do arquivo CSV para um DataFrame do Pandas.

    df = pd.read_csv('resultados_completos_classificados.csv')

### Visualização inicial dos dados

Aqui, o modelo criado faz, sucessivamente:

Apresentação de uma amostra aleatória de 5 linhas do DataFrame;

Contagem de número de entradas não nulas em cada coluna;

Contagem de número de valores nulos em cada coluna.

    df.sample(5)
    df.count()
    df.isna().sum()

### Substituição de valores categóricos

O modelo faz, consecutivamente:

Converte a coluna CLASSIFICACAO_NOTA de categórica para numérica, substituindo 'A', 'B', 'C', 'D', 'E' por 1, 2, 3, 4, 5, respectivamente, pois a regressão só trabalha com dados numéricos (embora depois esse dado vá ser dropado da tabela);

Ao fim, são exibidas as primeiras 5 linhas do DataFrame para uma visualização inicial.

    df["CLASSIFICACAO_NOTA"]=df["CLASSIFICACAO_NOTA"].replace(to_replace=['A', 'B', 'C', 'D', 'E'], value=[1, 2, 3, 4, 5])
    df.head()

### Visualização da distribuição dos dados

Nessa parte, para cada coluna relevante, foi plotado um histograma para visualizar a distribuição dos valores e entender melhor como os dados estavam funcionando no dataset (o que, em verdade, seguiu não sendo conclusivo).

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

### Matriz de correlação

Aqui foram feitos, respectivamente:

O Cálculo da matriz de correlação entre as colunas;

A Plotagem de um mapa de calor da matriz de correlação para identificar visualmente a relação entre as variáveis, como já havia sido feito isso antes, a matriz de correlação seguiu não apresentando grandes correlações.

    df.corr()
    sns.heatmap(df.corr(), cmap='coolwarm', annot=True)
    plt.show()

### Correlação com a variável dependente

Nessa parte, foi realizada a ordenação dos coeficientes de correlação das variáveis independentes com a variável dependente "CLASSIFICACAO_NOTA".

    df.corr()['CLASSIFICACAO_NOTA'].sort_values()

### Divisão dos dados em variáveis independentes e dependentes

Nesse caso, os itens representam:

x - DataFrame contendo todas as colunas exceto "CLASSIFICACAO_NOTA" e "IDESP_AF";

y - Série contendo apenas a coluna "IDESP_AF".

Nota: Essa será a base para as análises e as colunas dropadas não podem estar dentro do datafame influenciando o treino, por serem os resultados que desejamos encontrar.

    x = df.drop(['CLASSIFICACAO_NOTA','IDESP_AF'], axis = 1)
    y = df['IDESP_AF']

### Divisão dos dados em conjuntos de treino e teste

Aqui, divide-se os dados em conjuntos de treino (70%) e teste (30%).

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.3, random_state = 100)

### Criação e treino do modelo de regressão linear:

Inicialmente, na seguinte parte, são feitos os processos de:

Criar uma instância do modelo de regressão linear;

Treinar o modelo usando os dados de treino.

    mlr = LinearRegression()
    mlr.fit(x_train, y_train)

### Exibição dos coeficientes do modelo:

Essa parte do código tem o objetivo de mostrar alguns coeficientes, sendo eles:

Intercept - O valor esperado da variável dependente (IDESP_AF) quando todas as variáveis independentes são zero;

Coeficientes - Representam a mudança esperada na variável dependente para uma unidade de mudança na variável independente correspondente.

    print("Intercept: ", mlr.intercept*)
    print("Coefficients:")
    list(zip(x, mlr.coef*))

### Predição nos dados de teste:

Aqui é feita a previsões usando os dados de teste.

    y_pred_mlr= mlr.predict(x_test)

### Visualização das previsões:

Essa parte é dedicada a plotagem de um gráfico de dispersão das previsões versus os valores reais nessa parte do código.

    sns.regplot(x=y_test, y=y_pred_mlr, ci=None, color='red', line_kws={"color": "black"})
    plt.show()

### Calcula e exibe as métricas de desempenho do modelo:

Aqui se mostra os dados que permitirão uma avaliação do modelo, como:

R squared - que é o ajuste do modelo aos dados que contém "mlr.score(x,y)" que indica a proporção da variância explicada pelo modelo.

Mean Absolute Error - que é a média das diferenças absolutas entre os valores previstos e os valores reais;

Mean Square Error - que é a a média das diferenças ao quadrado entre os valores previstos e os valores reais;

Root Mean Square Error - que é a raiz quadrada do MSE, proporcionando uma métrica de erro na mesma unidade da variável dependente.

    meanAbErr = metrics.mean_absolute_error(y_test, y_pred_mlr)
    meanSqErr = metrics.mean_squared_error(y_test, y_pred_mlr)
    rootMeanSqErr = np.sqrt(metrics.mean_squared_error(y_test, y_pred_mlr))
    print('R squared: {:.2f}'.format(mlr.score(x,y)\*100))
    print('Mean Absolute Error:', meanAbErr)
    print('Mean Square Error:', meanSqErr)
    print('Root Mean Square Error:', rootMeanSqErr)

### Predição com novos dados:

Nessa parte, é feita uma predição com novos dados fornecidos manualmente(usamos aqui métricas presentes na tabela de correlação entre infraestrutura e notas do Idesp_AF, para o resultado ser o mais realista comparativamente).

    Classificacao_Nota_Index= mlr.predict([[3,3,2,2,18,1,8]])
    print(Classificacao_Nota_Index)

## Análise Naïve Bayes

Esse modelo foi escolhido baseando-se nos artigos presentes no estado da arte deste projeto de pesquisa, levando-se em consideração a necessidade de aderência dos textos escolhidos com as análises aqui selecionadas.

O modelo final foi de autoria própria do grupo.

### Importaçao das bibliotecas

Inicialmente, foram importadas as bibliotecas necessárias para manipulação e análise de dados, construção de modelos preditivos, visualização e interpretação de resultados, como o que já foi visto nos demais modelos;

    import pandas as pd from sklearn.model_selection
    import train_test_split from sklearn.naive_bayes
    import GaussianNB from sklearn.metrics
    import accuracy_score, classification_report, confusion_matrix

### Carregamento e Visualização dos Dados

O conjunto de dados foi carregado a partir de um arquivo CSV. A visualização inicial dos dados foi realizada para assegurar que a importação ocorreu corretamente.

    df = pd.read_csv('resultados_completos_classificados.csv')
    print(df.head())

### Análise da Distribuição das Classes

Realizou-se a contagem da quantidade de ocorrências das diferentes classes na variável alvo "CLASSIFICACAO_NOTA" para entender a distribuição dos dados.

    class_counts = df['CLASSIFICACAO_NOTA'].value_counts().sort_index()
    print("Quantidade de ocorrências das classes no dataset:")
    print(class_counts)

### Preparação dos Dados

As features e a target foram separadas para preparar os dados para o treinamento do modelo.

    X = df[['BANHEIROS', 'COZINHA', 'LABORATORIO', 'ESPORTE', 'SALAS DE AULA', 'LEITURA', 'OUTROS']]
    y = df['CLASSIFICACAO_NOTA']

### Divisão do Conjunto de Dados

O conjunto de dados foi dividido em conjuntos de treinamento e teste, com 70% dos dados destinados ao treinamento e 30% ao teste.

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

### Construção e Treinamento do Modelo Naïve Bayes

O modelo Naïve Bayes Gaussiano foi criado e treinado com os dados de treinamento.

    nb = GaussianNB()
    nb.fit(X_train, y_train)

### Avaliação dos testes e precisão dos modelos

As previsões foram realizadas no conjunto de teste e a precisão do modelo foi avaliada.

    y_pred = nb.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Accuracy: {accuracy}')

### Relatório da precisão

Um relatório de classificação foi gerado para fornecer detalhes sobre a precisão, recall e F1 Score para cada classe.

    print('Classification Report:')
    print(classification_report(y_test, y_pred))

### Matriz de confusão

A matriz de confusão foi gerada para visualizar o desempenho do modelo em termos de classificações corretas e incorretas.

    print('Confusion Matrix:')
    print(confusion_matrix(y_test, y_pred))

## Vídeo com a explicação dos Modelos

Para um melhor entendimento do funcionamento de cada modelo, segue vídeo contendo os dados e os tratamentos feitos nos dados para o funcionamento de cada modelo:

[Vídeos da apresentação dos Modelos e seus tratamentos de dados.](https://youtu.be/Wlbj_kwbqxA)

# Avaliação dos modelos criados

## Métricas utilizadas

O critério de seleção das métricas de avaliação dos modelos desenvolvidos respeitou as especificidades dos tipos de problema, quer de classificação, quer de regressão, expressos no nosso conjunto de dados.

Começando pelos modelos de classificação binária, o modelo de árvore de decisão simples resultou numa acurácia de 58%, qual seja, o modelo conseguiu prever adequadamente 58,47% dos dados da amostra. Isso também pode ser observado nas métricas de precisão e recall, aa quais ele obteve, respectivamente, 58,22% e 58,47 de previsões positivas. O equilíbrio entre precisão e recall pode ser visto, principalmente, pela média harmônica de 57,20% expressa pelo F1-Score.

Com relação às métricas definidas para determinar o nível de confiabilidade do modelo ensemble, i.e., Adaptive Boosting, que é um modelo de classificação aprimorado por árvores de decisão simples operadas iterativamente, nós observamos que ele obteve por volta de 48,87% de acerto nas previsões em face dos dados da amostra. Tal acurácia, porém, não foi suficientemente capaz de fornecer um parâmetro avaliativo superior à metade proporcional, pois houve grande assimetria no nosso conjunto de dados, o que, por sua vez, implicou em dificuldades significativas em seu treinamento. Já o exame da precisão e do recall do modelo ensemble expôs, de modo respectivo, que 47,15% e 48,87% dos dados da amostra representaram de modo fidedigno os dados reais. Ambas as métricas evidenciam que o modelo convergiu razoávelmente à realidade, o que se expressa, principalmente, por meio da pontuação do F1-Score de 0.4469, que demonstra o equilíbrio entre os falsos positivos e falsos negativos. A pontuação de ROC AUC Score de 0.6122, por fim, corroborou para consideração de que o modelo ensemble obteve um sucesso razoável de modo que se mostrou superior a um classificador aleatório.

Além do exame dos modelos de classificação, nós também verificamos o grau de convergência ou desvio dos dados da amostra à reta regressão por meio da regressão linear múltipla. Em primeiro lugar, cabe destacar que o nosso coeficiente de determinação (R²) resultou em 1.81, excedendo o intervalo entre 0 e 1, o que evidencia problemas na implementação do modelo. Em segundo lugar, se nos concentrarmos tão somente no Erro Médio Absoluto (MAE) e na Raiz do Erro Quadrático Médio (RMSE) houve desvios significativos que se situam em torno de 1 (uma) unidade, visto que, respectivamente, nós obtivemos 0.9305 e 1.3025. Em um cenário real, tal diferença ou resíduo pode tornar determinada escola boa em média e média em ruim ou vice-versa. Isso, porém, não era o que se esperava alcançar nesta regressão. Nosso objetivo inicial era estabelecer uma reta regressão que apresentasse resultados uniformes em vista dos inputs. Portanto, será preciso corrigir e reavaliar o modelo nas próximas etapas.

## Discussão dos resultados obtidos

Assim como mostrado no "Vídeos da apresentação dos Modelos e seus tratamentos de dados" e nas "métricas utilizadas", foi possível observar que os cinco modelos selecionados não apresentaram um bom desempenho para o tipo de dado escolhido para análise.

Levando-se em consideração o problema da carência de infraestrutura e como ela pode influenciar positivamente no processo de aprendizagem do aluno, a questão proposta de como a infraestrutura escolar influencia no desempenho dos alunos de ensino fundamental nas avaliações do IDESP_AF e no objetivo de apontar a influência da infraestrutura escolar no desempenho desses alunos, pode-se concluir que os nossos resultados não trouxeram algo relevante que dê indícios mínimos de correlação entre os dados e resultados propostos inicialmente.
Esse ponto pode ser entendido como alguns problemas de métricas adotadas, como pensamos inicialmente, porém, com a inconstância de parâmetros iguais de infraestrutura e resultados muitos distintos de notas do IDESP_AF, é viável pensar que os modelos apenas não conseguem definir um parâmetro mínimo para melhorar a acurácia nos resultados, que, no melhor dos caso, não chega a 50% de precisão.

Sendo assim, analisando as métricas ruins em todos os nossos resultados, cabe colocar em destaque que os nossos modelos podem estar pouco regulados, principalmente o de regressão linear múltipla, devido a sua grande imprecisão, mas não se deve descartar a possibilidade considerável de os dados não possuírem a qualidade adequada para qualquer outro modelo de análise, ainda que devidamente regulado.

# Pipeline de Pesquisa e Análise de Dados

![Fluxograma do Pipeline](img/fluxograma.png)

Fluxo 1 - Fluxograma do Pipeline

## Introdução

Este documento descreve o processo utilizado para desenvolver um pipeline de pesquisa e análise de dados com o objetivo de prever a possível nota do IDESP (Índice de Desenvolvimento da Educação do Estado de São Paulo) de alfabetização para escolas, utilizando dados de infraestrutura escolar e notas das escolas. O projeto foi desenvolvido como parte de um trabalho acadêmico.

## Passos do Processo

### 1. Busca e Coleta de Dados

Iniciamos o processo buscando as bases de dados necessárias no site do governo de São Paulo. Encontramos duas bases distintas: uma contendo informações de infraestrutura por escola, como salas de aula e banheiros, e outra com as notas por escola.

### 2. Integração de Dados

Após identificar as bases necessárias, procedemos à integração das mesmas, utilizando o código de cada escola como uma "chave estrangeira". Isso nos permitiu unificar todas as informações relevantes em uma única base de dados.

### 3. Pré-processamento dos Dados

Nesta etapa, realizamos o pré-processamento dos dados, removendo atributos desnecessários da nossa base, como "IDESP_EM", "IDESP_AI", "COD_ESC", "ANO_APLICACAO", "DTCADASTRO" e "DT_UPDATE", uma vez que estávamos focados exclusivamente na nota do IDESP de alfabetização (IDESP_AF).

### 4. Categorização das Notas

Para facilitar a aplicação de modelos de classificação, procedemos à categorização das notas do IDESP. Isso nos permitiu transformar as notas em classes discretas, facilitando a análise e o treinamento dos modelos.

### 5. Desenvolvimento de Modelos

Foram desenvolvidos cinco modelos para prever a nota do IDESP de alfabetização das escolas. Estes incluem modelos de regressão, Naive Bayes, Árvore de Decisão, Adaboost e Regras de Associação. O modelo de regressão foi treinado com as notas sem categorização, enquanto os demais foram treinados com as notas categorizadas.

### 6. Análise dos Modelos

Com os modelos treinados e os resultados obtidos, procedemos à análise de cada modelo. Avaliamos sua precisão, sensibilidade e outras métricas relevantes para determinar sua eficácia na previsão das notas do IDESP de alfabetização.
