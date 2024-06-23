# Apresentação da Solução
Vídeo com o escopo todo o projeto, um resumo do trabalho desenvolvido, comprovação de que a implantação foi realizada e conclusões alcançadas: [Apresentação da API.](https://youtu.be/5ecyhv273S4)

# Implantação da solução
Nessa seção, será apresentado como foi desenvolvida a seguinte Aplicação: [Influência da Infraestrutura escolar nas notas do IDESP-AF de escolas públicas do estado de São Paulo.](http://34.227.72.111/)

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

## Front-End

Para implementar o Front-End da aplicação, foram usadas as seguintes tecnologias:

- HTML 5;
- CSS3;
- Biblioteca de CSS e JS Bootstrap;
- Conjunto de ícones para uso junto com o Bootstrap, o Bootstrap Icons;
- Motor de templates do Flask para renderização dinâmica do HTML, o Jinja2;
- Microframework web Flask, em Python.

### Detalhamento do Projeto

Os dados a seguir estão presentes no arquivos do Front-End do projeto, representado pelo arquivo principal "form.html" (juntamente com ele, implementado por definições do "bootstrap.min.css" e "bootstrap-icons.min.css" também presentes no projeto).

#### Inicialização do Projeto/ Configurações de entrada

    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simulação dos dados treinados</title>

- Definição do tipo de documento como HTML5;
- Definição do elemento raiz do documento HTML, com o atributo lang definido como "en" para indicar que o conteúdo está em inglês;
- Implementação do cabeçalho do documento, onde são incluídas metadados e links para arquivos externos;
- Definição da codificação de caracteres do documento como UTF-8;
- Configuração da visualização para dispositivos móveis, definindo a largura da página como igual à largura da tela do dispositivo e o nível de zoom inicial como 1.0;
- Definição do título da página que será exibido na aba do navegador, mais especificamente "Simulação dos dados treinados".

#### Link para arquivos externos

        <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.min.css') }}">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">

- Link para o arquivo CSS do Bootstrap, sendo que o "{{ url_for('static', filename='css/bootstrap.min.css') }}" é uma função do Flaskpara gerar a URL do arquivo estático;
- Link para um arquivo CSS que inclui ícones do Bootstrap Icons, hospedado em uma CDN.

#### Definindo configurações de tela e divisões

    <body>
        <div class="container" style="">
            <main>
                <div class="py-5 text-center">
                    <h2>Previsão da nota IDESP-AF da escola com base na infraestrutura</h2>
                    <p class="lead">Previsão baseada em 4 modelos previamente treinados. Preencha os campos abaixo e clique em "Enviar" para obter a previsão.</p>
                    <p></p>
                </div>
                <div class="row g-5">
                    <div class="col-md-4 col-lg-3 order-md-last">

- Inicia corpo do documento HTML, onde o conteúdo visível da página fica;
- Criação de um contêiner fluido com margens e preenchimento, utilizando a classe container do Bootstrap;
- Insere um wlemento HTML5 que indica o conteúdo principal da página;
- Criação de uma seção com padding vertical "py-5", com alinhamento do texto ao centro (text-center);
- Criação de um cabeçalho de nível 2 com o título da página, que é "Previsão da nota IDESP-AF da escola com base na infraestrutura";
- Inclusão de classe lead do Bootstrap, que estiliza o texto como destaque;
- Criação de uma linha "row" com um espaçamento "g-5" entre os elementos filhos;
- Definição de uma coluna que ocupa 4 unidades em telas médias e 3 unidades em telas grandes, sendo exibida por último em telas médias e superiores.

#### Bloco condicional

                        {% if previsoes %}
                        <div class="d-flex align-items-center p-3 my-3 text-white rounded shadow-sm" style="background-color: var(--bs-success);">
                            <div class="rounded me-3" style="height: 50px;
                            min-width: 50px;
                            background-color: #fff;
                            padding: 15px;
                            padding-top: 3px;
                            font-size: 1.8rem;
                            font-weight: 700;"><span style="color: {{ cor_previsao }};">{{melhor_previsao}}</span></div>
                            <div class="lh-1" style="border-left: 1px solid #ffffff59;
                            padding-left: 10px;">
                            <h1 class="h6 mb-0 text-white lh-1">Nota prevista</h1>
                            <br/>
                            <small>{{descricao_politica}}</small>
                            </div>
                        </div>
                        {% endif %}
                        <h4 class="d-flex justify-content-between align-items-center mb-3">
                        <span class="">Previsões</span>
                        </h4>
                        {% if previsoes %}
                        <ul class="list-group mb-3">
                            {% for previsao in previsoes %}
                            {% if previsao.previsao == melhor_previsao %}
                            <li class="list-group-item d-flex justify-content-between bg-body-tertiary">
                                <div class="text-success">
                                <h6 class="my-0">{{ previsao.nome }}</h6>
                                <small class="text-body-secondary">{{ previsao.detalhe }}</small>
                                </div>
                                <span class="fw-bolder badge text-bg-success p-3"> {{ previsao.previsao }}</span>
                            </li>
                            {% else %}
                            <li class="list-group-item d-flex justify-content-between lh-sm">
                                <div>
                                <h6 class="my-0">{{ previsao.nome }}</h6>
                                <small class="text-body-secondary">{{ previsao.detalhe }}</small>
                                </div>
                                <span class="fw-bolder badge text-bg-light p-3">{{ previsao.previsao }}</span>
                            </li>
                            {% endif %}
                            {% endfor %}
                        </ul>
                        {% else %}
                        <p class="lead mb-3" style="font-size: 1rem;">Nenhuma previsão calculada...</p>
                        {% endif %}

                    </div>

- Inicialização um bloco condicional em "Jinja2" (motor de templates do Flask), verificando se a variável "previsoes" está definida;
- Inclusão de uma divisão com várias classes Bootstrap para alinhamento flexível, padding, margem, texto branco, cantos arredondados e sombra. O background-color usa uma variável CSS para definir a cor de fundo;
- Inclusão de uma divisão com estilo inline e conteúdo dinâmico usando variáveis do Flask/"Jinja2" para exibir a melhor previsão com uma cor específica;
- Configura o cabeçalho de nível 1 estilizado como h6 do Bootstrap;
- Inclui uma lista não ordenada com a classe "list-group" do Bootstrap para estilizar como um grupo de itens;
- Inicialização de um loop for em "Jinja2" para iterar sobre cada "previsao" na lista "previsoes";
- Inclusão de item da lista com classes Bootstrap para flexbox e espaçamento entre itens, e cor de fundo alternativa.

#### Inclusão de itens de formulário

                    </div>
                    <div class="col-md-4 col-lg-6">
                        <h4 class="mb-3">Infraestrutura</h4>
                        <form action="/predict" method="POST" class="row g-3">
                            <div class="form-group col-md-4">
                                <label for="banheiros">Banheiros</label>
                                <input type="number" class="form-control" id="banheiros" name="banheiros" required value="{{ banheiros }}">
                            </div>
                            <div class="form-group col-md-4">
                                <label for="cozinha">Cozinha</label>
                                <input type="number" class="form-control" id="cozinha" name="cozinha" required  value="{{ cozinha }}">
                            </div>
                            <div class="form-group col-md-4">
                                <label for="laboratorio">Laboratorio</label>
                                <input type="number" class="form-control" id="laboratorio" name="laboratorio" required  value="{{ laboratorio }}">
                            </div>
                            <div class="form-group col-md-4">
                                <label for="esporte">Esporte</label>
                                <input type="number" class="form-control" id="esporte" name="esporte" required  value="{{ esporte }}">
                            </div>
                            <div class="form-group col-md-4">
                                <label for="salas_de_aula">Salas De Aula</label>
                                <input type="number" class="form-control" id="salas_de_aula" name="salas_de_aula" required  value="{{ salas_de_aula }}">
                            </div>
                            <div class="form-group col-md-4">
                                <label for="leitura">Leitura</label>
                                <input type="number" class="form-control" id="leitura" name="leitura" required  value="{{ leitura }}">
                            </div>
                            <div class="form-group col-md-4">
                                <label for="outros">Outros</label>
                                <input type="number" class="form-control" id="outros" name="outros" required  value="{{ outros }}">
                            </div>
                            <div class="d-grid gap-2 d-md-flex justify-content-md-end">
                                <a href="/random" class="btn btn-outline-secondary d-inline-flex align-items-center" type="button">
                                <span style="margin-right: 8px;"> Valores aleatórios</span>
                                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-shuffle" viewBox="0 0 16 16">
                                        <path fill-rule="evenodd" d="M0 3.5A.5.5 0 0 1 .5 3H1c2.202 0 3.827 1.24 4.874 2.418.49.552.865 1.102 1.126 1.532.26-.43.636-.98 1.126-1.532C9.173 4.24 10.798 3 13 3v1c-1.798 0-3.173 1.01-4.126 2.082A9.6 9.6 0 0 0 7.556 8a9.6 9.6 0 0 0 1.317 1.918C9.828 10.99 11.204 12 13 12v1c-2.202 0-3.827-1.24-4.874-2.418A10.6 10.6 0 0 1 7 9.05c-.26.43-.636.98-1.126 1.532C4.827 11.76 3.202 13 1 13H.5a.5.5 0 0 1 0-1H1c1.798 0 3.173-1.01 4.126-2.082A9.6 9.6 0 0 0 6.444 8a9.6 9.6 0 0 0-1.317-1.918C4.172 5.01 2.796 4 1 4H.5a.5.5 0 0 1-.5-.5"/>
                                        <path d="M13 5.466V1.534a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384l-2.36 1.966a.25.25 0 0 1-.41-.192m0 9v-3.932a.25.25 0 0 1 .41-.192l2.36 1.966c.12.1.12.284 0 .384l-2.36 1.966a.25.25 0 0 1-.41-.192"/>
                                    </svg>
                                    </a>
                            </div>
                            <hr class="my-4">
                            <button type="submit" class="btn btn-success mt-3">Enviar</button>
                        </form>
                    </div>

- Inclusão de cabeçalho de nível 4 para a seção de infraestrutura;
- Inclusão de formulário HTML com método POST que envia dados para a rota "/predict", estilizado como uma linha do Bootstrap;
- Definição de que cada grupo de formulário ocupa 4 unidades de coluna em telas médias;
- Definição de rótulo associado ao campo de entrada banheiros (isso se repete para os outros campos, por isso não será feito o detalhamento neste documentos dos demais, que são réplicas dessa mesma operação, porém, com nomes distintos);
- Inclusão de campo de entrada para números com a classe "form-control" do Bootstrap. O valor inicial é definido por uma variável "Jinja2";
- Inclusão de Link estilizado como botão que direciona para a rota "/random" para gerar valores aleatórios;
- Inclusão de botão de envio com a classe "btn-success" do Bootstrap.

#### Inclusão dos resultados em tela e links

                    <div class="col-md-4 col-lg-3 order-md-first">
                        <div class="card p-2">
                            <div class="card-body">
                            <p class="card-text">As classes das notas são formadas pelos seguintes intervalos de valores de notas:</p>
                            </div>
                            <ul class="list-group list-group-flush">
                            <li class="list-group-item d-flex justify-content-between"><small class="badge bg-success-subtle text-success-emphasis rounded-pill"> Classe E</small><small class="text-body-secondary">Notas entre <strong>0</strong> e <strong>1,61</strong></small></li>
                            <li class="list-group-item d-flex justify-content-between"><small class="badge bg-success-subtle text-success-emphasis rounded-pill"> Classe D</small><small class="text-body-secondary">Notas entre <strong>1,62</strong> e <strong>3,22</strong></small></li>
                            <li class="list-group-item d-flex justify-content-between" ><small class="badge bg-success-subtle text-success-emphasis rounded-pill"> Classe C</small><small class="text-body-secondary">Notas entre <strong>3,23</strong> e <strong>4,83</strong></small></li>
                            <li class="list-group-item d-flex justify-content-between"><small class="badge bg-success-subtle text-success-emphasis rounded-pill"> Classe B</small><small class="text-body-secondary">Notas entre <strong>4,84</strong> e <strong>6,44</strong></small></li>
                            <li class="list-group-item d-flex justify-content-between"><small class="badge bg-success-subtle text-success-emphasis rounded-pill"> Classe A</small><small class="text-body-secondary">Notas entre <strong>6,45</strong> e <strong>8.1</strong></small></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </main>

        </div>
    </body>
    </html>

- Listagem de itens com a classe "list-group-flush" do Bootstrap, para exibir itens sem bordas;
- Inclusão de rótulo pequeno com a classe badge do Bootstrap para exibir etiquetas de classe de notas.
