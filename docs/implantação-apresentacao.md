# Implantação da solução

Nesta seção, a implantação da solução proposta em nuvem deverá ser realizada e detalhadamente descrita. Além disso, deverá ser descrito também, o planejamento da capacidade operacional através da modelagem matemática e da simulação do sistema computacional.

Após a implantação, realize testes que mostrem o correto funcionamento da aplicação.

# Apresentação da solução

Nesta seção, um vídeo de, no máximo, 5 minutos onde deverá ser descrito o escopo todo do projeto, um resumo do trabalho desenvolvido, incluindo a comprovação de que a implantação foi realizada e, as conclusões alcançadas.

## Back-End

Para implementar as análises escolhidas, que são as que faziam uso do Modelo Classificador de Árvore de Decisão, o Classificador AdaBoost, a Regressão Linear Múltipla e o Naïve Bayes, descartando-se, por nos testes não apresentar grande relevância, as Regras de Associação, foram escolhidas as seguintes tecnologias:

- Linguagem em Python 3, especificamente Python 3.6 e superior, com uso de f-strings;
- Microframework web Flask, em Python;
- Módulo Flask, jolib, numpy e random e collections;
- VS Code versão 1,90.

### Detalhamento do Projeto

Os dados aqui apresentados estão presentes no Back-End do projeto, que foi implementado no arquivo "app.py".

#### Importações de bibliotecas

    from flask import Flask, render_template, request
    import joblib
    import numpy as np
    from collections import Counter
    import random as r

- Importação do módulo Flask e funções para criar a aplicação web, renderizar templates HTML e lidar com requisições HTTP;
- Importação do módulo joblib, usado para carregar os modelos de machine learning salvos;
- Importação do módulo numpy, que fornece suporte para arrays e operações matemáticas;
- Importação da classe Counter do módulo collections, usada para contar elementos em uma lista;
- Importação do módulo random e renomeação deste para r para gerar números aleatórios.

#### Inicialização do Flask

    app = Flask(__name__)

- Inicialização da aplicação Flaskrmite para criação de aplicações web.

#### Carregamento dos modelos

    ada_boost_classifier = joblib.load('modelo_treinado_ada_boost_classifier.pkl')
    decision_tree_classifier = joblib.load('modelo_treinado_decision_tree_classifier.pkl')
    gaussian_nb = joblib.load('modelo_treinado_gaussian_nb.pkl')
    linear_regression = joblib.load('modelo_treinado_linear_regression.pkl')

- Carregamento dos modelos selecionados previamente treinados, usando 'joblib' (esses modelos foram previamente transformados em arquivos '.pk1').

#### Definição de rotas e funções

    @app.route('/')
    def home():
        return render_template('form.html')

- Definição da rota para a página inicial ('/').
  Nota: quando essa rota é acessada, a função home renderiza o template form.html.

### Função para classificar notas

    def classificar_nota(nota):
        # Categorias para classificar as notas
        categorias_classificacao_notas = ["A", "B", "C", "D", "E"]
        for index, item in enumerate(categorias_classificacao_notas):
            if nota <= (index + 1):
                return item
        return categorias_classificacao_notas[-1]

- Definição da função "classificar_nota", que classifica uma nota numérica em categorias ("A", "B", "C", "D", "E"), com base nos intervalos definidos anteriormente no DataFrame, na configuração dos arquivos em outras etapas do projeto.

#### Função para aplicar políticas de decisão

    def aplicar_politicas(resultados):
        previsoes = [resultado["previsao"] for resultado in resultados]
        accuracies = [resultado["accuracy"] for resultado in resultados]

        contador_previsoes = Counter(previsoes)
        previsao_mais_comum, frequencia = contador_previsoes.most_common(1)[0]

        if frequencia > 2:
            return previsao_mais_comum, "Política aplicada: Resultado com maior frequência entre os modelos utilizados"

        if frequencia == 1:
            index_maior_accuracy = accuracies.index(max(accuracies))
            return resultados[index_maior_accuracy]["previsao"], "Política aplicada: Utilizado modelo com maior acurácia"

        if len(set(previsoes)) == 1:
            return previsoes[0],  "Política aplicada: Resultado semelhante em todos os modelos utilizados"

        index_maior_accuracy = accuracies.index(max(accuracies))
        return resultados[index_maior_accuracy]["previsao"], "Política aplicada: Utilizado modelo com maior acurácia"

- Definição da função "aplicar_politicas", que aplica regras de decisão para escolher a melhor previsão com base nos resultados fornecidos pelos modelos. As políticas são:

  - Usar a previsão mais comum se houver maioria;
  - Usar a previsão com maior acurácia se todas forem diferentes;
  - Se todas as previsões forem iguais, usar qualquer uma delas;
  - Em caso de empate, usar a previsão com maior acurácia.

#### Rota para realizar previsões

    @app.route('/predict', methods=['POST'])
    def predict():
        try:
            # Receber dados do formulário
            banheiros = int(request.form['banheiros'])
            cozinha = int(request.form['cozinha'])
            laboratorio = int(request.form['laboratorio'])
            esporte = int(request.form['esporte'])
            salas_de_aula = int(request.form['salas_de_aula'])
            leitura = int(request.form['leitura'])
            outros = int(request.form['outros'])

            # Criar array com os dados recebidos
            dados_entrada = np.array([[banheiros, cozinha, laboratorio, esporte, salas_de_aula, leitura, outros]])

            # Fazer a previsão
            resultados = [
                {
                    "nome": "Gaussian Naive Bayes",
                    "detalhe": f"{round(gaussian_nb['accuracy'] * 100, 2)}% de Acurácia",
                    "previsao": gaussian_nb['modelo'].predict(dados_entrada)[0],
                    "accuracy": gaussian_nb['accuracy']
                },
                {
                    "nome": "Linear Regression",
                    "detalhe": f"{round(linear_regression['accuracy'] * 100, 2)}% de Acurácia",
                    "previsao": classificar_nota(linear_regression['modelo'].predict(dados_entrada)[0]),
                    "accuracy": linear_regression['accuracy']
                },
                {
                    "nome": "Decision Tree Classifier",
                    "detalhe": f"{round(decision_tree_classifier['accuracy'] * 100, 2)}% de Acurácia",
                    "previsao": decision_tree_classifier['modelo'].predict(dados_entrada)[0],
                    "accuracy": decision_tree_classifier['accuracy']
                },
                {
                    "nome": "Adaboost Classifier",
                    "detalhe": f"{round(ada_boost_classifier['accuracy'] * 100, 2)}% de Acurácia",
                    "previsao": classificar_nota(ada_boost_classifier['modelo'].predict(dados_entrada)[0]),
                    "accuracy": ada_boost_classifier['accuracy']
                }
            ]

            melhor_previsao, descricao_politica = aplicar_politicas(resultados)

            cores_previsoes = {
                "A" : "var(--bs-success)",
                "B" : "var(--bs-primary)",
                "C" : "var(--bs-info)",
                "D": "var(--bs-warning)",
                "E" :"var(--bs-danger)"
            }

            return render_template('form.html',
                                    previsoes=resultados,
                                    melhor_previsao=melhor_previsao,
                                    descricao_politica=descricao_politica,
                                    cor_previsao=cores_previsoes[melhor_previsao],
                                    banheiros=banheiros,
                                    cozinha=cozinha,
                                    laboratorio=laboratorio,
                                    esporte=esporte,
                                    salas_de_aula=salas_de_aula,
                                    leitura=leitura,
                                    outros=outros)
        except Exception as e:
            return f'Erro ao realizar a previsão: {e}'

- Define a rota "/predict" para lidar com as requisições do tipo 'POST';
- Realiza as previsões com base nos dados do formulário, aplica políticas de decisão e renderiza o template presente no "form.html" com os resultados obtidos na requisição.

#### Rota para gerar valores aleatórios

    @app.route('/random', methods=['GET'])
    def random():
        valor_minimo = 1
        valor_maximo = 60
        banheiros = r.randint(valor_minimo, valor_maximo)
        cozinha = r.randint(valor_minimo, valor_maximo)
        laboratorio = r.randint(valor_minimo, valor_maximo)
        esporte = r.randint(valor_minimo, valor_maximo)
        salas_de_aula = r.randint(valor_minimo, valor_maximo)
        leitura = r.randint(valor_minimo, valor_maximo)
        outros = r.randint(valor_minimo, valor_maximo)

        return render_template('form.html',
                                banheiros=banheiros,
                                cozinha=cozinha,
                                laboratorio=laboratorio,
                                esporte=esporte,
                                salas_de_aula=salas_de_aula,
                                leitura=leitura,
                                outros=outros)

- Definição de rota "/random" para gerar valores aleatórios para cada campo do formulário
- Renderização o template form.html com os valores aleatórios.

#### Execução da aplicação

    if __name__ == '__main__':
        app.run(debug=True)

- Verificação de que o script está sendo executado diretamente e, se sim, inicialização da aplicação Flask no modo debug.
