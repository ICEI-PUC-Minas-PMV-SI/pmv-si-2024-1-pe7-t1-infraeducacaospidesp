from flask import Flask, render_template, request
import joblib
import numpy as np
from collections import Counter
import random as r

app = Flask(__name__)

# Carregar os modelos salvos
ada_boost_classifier = joblib.load('modelo_treinado_ada_boost_classifier.pkl')
decision_tree_classifier = joblib.load('modelo_treinado_decision_tree_classifier.pkl')
gaussian_nb = joblib.load('modelo_treinado_gaussian_nb.pkl')
linear_regression = joblib.load('modelo_treinado_linear_regression.pkl')

@app.route('/')
def home():
    return render_template('form.html')

def classificar_nota(nota):
    # Categorias para classificar as notas
    categorias_classificacao_notas = ["A", "B", "C", "D", "E"]
    for index, item in enumerate(categorias_classificacao_notas):
        if nota <= (index + 1):
            return item
    return categorias_classificacao_notas[-1]

def aplicar_politicas(resultados):
    previsoes = [resultado["previsao"] for resultado in resultados]
    accuracies = [resultado["accuracy"] for resultado in resultados]
    
    # Contar as ocorrências de cada previsão
    contador_previsoes = Counter(previsoes)
    previsao_mais_comum, frequencia = contador_previsoes.most_common(1)[0]
    
    # Política 1: Se a maioria das previsões são iguais, usar a previsão mais comum
    if frequencia > 2:
        return previsao_mais_comum, "Política aplicada: Resultado com maior frequência entre os modelos utilizados"
    
    # Política 2: Se todas as previsões são diferentes, usar a previsão com maior accuracy
    if frequencia == 1:
        index_maior_accuracy = accuracies.index(max(accuracies))
        return resultados[index_maior_accuracy]["previsao"], "Política aplicada: Utilizado modelo com maior acurácia"
    
    # Política 3: Se todas as previsões são iguais, usar qualquer uma (já que são todas iguais)
    if len(set(previsoes)) == 1:
        return previsoes[0],  "Política aplicada: Resultado semelhante em todos os modelos utilizados"
    
    # Caso nenhum dos acima se aplique, o que seria improvável com base nas regras fornecidas,
    # vamos por segurança retornar a previsão com maior accuracy.
    index_maior_accuracy = accuracies.index(max(accuracies))
    return resultados[index_maior_accuracy]["previsao"], "Política aplicada: Utilizado modelo com maior acurácia"

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



if __name__ == '__main__':
    app.run(debug=True)