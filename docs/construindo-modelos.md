## Pergunta orientada a dados (???)
Justificar a definição / diferença da questão de pesquisa

## Tipos de dados do dataset
Qual o tipo de cada um dos atributos?

# Preparação dos dados

Os dados utilizados no projeto foram coletados no [Portal da Transparência da educação do Governo do estado de São Paulo](https://dados.educacao.sp.gov.br/dataset/portal-da-transpar%C3%AAncia). Inicialmente, as informações da infraestrutura das escolas e as suas respectivas notas do IDESP estavam em tabelas separadas, já que o dataset disponibilizado pelo governo é composto por diversas informações sobre as escolas separadas em tabelas distintas. Devido ao enfoque dado ao projeto, referente a avaliação da nota do IDESP nos anos finais do ensino fundamental (IDESP_AF) e a influência da infraestrutura das escolas nesses resultados, foram selecionadas as tabelas das notas do IDESP e do mapeamento da infraestrutura das escolas para construção do novo dataset a ser utilizado na execução dos modelos de aprendizado de máquina e a tabela escolas foi utilizada para validação dos códigos das escolas constantes nas tabelas anteriores. 

No primeiro tratamento dos dados, as categorias "BANHEIROS", "COZINHA", "LABORATÓRIO", "ESPORTE", "SALAS DE AULA", "LEITURA" e "OUTROS", que correspondiam a linhas na tabela de infraestrutura, foram separadas e transformadas em colunas com as suas respectivas quantidades por escolas para compor o novo dataset. As linhas com valores nulos para o IDESP_AF foram excluídas e também foram eliminadas as informações de datas, notas do IDESP_EM e IDESP_AI e o código da escola. O dataset resultante contemplou com a contabilização dos itens de infraestrutura e a nota IDESP_AF por escola.

Após alguns experimentos com o dataset construído inicialmente e devido às dúvidas apresentadas em aula, o grupo seguiu a orientação da Professora e realizou uma nova transformação dos dados para que as Notas IDESP_AF, que são o atributo alvo, fossem categorizadas. Por esse motivo foi adotado o método de discretização de dados por largura igual, onde foram definidas as categorias de classificação das notas de A até E, sendo A a categoria das notas mais altas e E a das notas mais baixas. Para a definição do intervalo correspondente a cada classe foram levados em consideração o valor máximo e mínimo das notas e a quantidade total de classes definidas. Como resultado, um novo dataset de nome "resultados_completos_classificados” foi criado com o acréscimo da coluna "CLASSIFICACAO_NOTA".

# Descrição dos modelos

Nesta seção, conhecendo os dados e de posse dos dados preparados, é hora de descrever os algoritmos de aprendizado de máquina selecionados para a construção dos modelos propostos. Inclua informações abrangentes sobre cada algoritmo implementado, aborde conceitos fundamentais, princípios de funcionamento, vantagens/limitações e justifique a escolha de cada um dos algoritmos. 

Explore aspectos específicos, como o ajuste dos parâmetros livres de cada algoritmo. Lembre-se de experimentar parâmetros diferentes e principalmente, de justificar as escolhas realizadas.

Como parte da comprovação de construção dos modelos, um vídeo de demonstração com todas as etapas de pré-processamento e de execução dos modelos deverá ser entregue. Este vídeo poderá ser do tipo _screencast_ e é imprescindível a narração contemplando a demonstração de todas as etapas realizadas.

# Avaliação dos modelos criados

## Métricas utilizadas

Nesta seção, as métricas utilizadas para avaliar os modelos desenvolvidos deverão ser apresentadas (p. ex.: acurácia, precisão, recall, F1-Score, MSE etc.). A escolha de cada métrica deverá ser justificada, pois esta escolha é essencial para avaliar de forma mais assertiva a qualidade do modelo construído. 

## Discussão dos resultados obtidos

Nesta seção, discuta os resultados obtidos pelos modelos construídos, no contexto prático em que os dados se inserem, promovendo uma compreensão abrangente e aprofundada da qualidade de cada um deles. Lembre-se de relacionar os resultados obtidos ao problema identificado, a questão de pesquisa levantada e estabelecendo relação com os objetivos previamente propostos. 

# Pipeline de pesquisa e análise de dados

Em pesquisa e experimentação em sistemas de informação, um pipeline de pesquisa e análise de dados refere-se a um conjunto organizado de processos e etapas que um profissional segue para realizar a coleta, preparação, análise e interpretação de dados durante a fase de pesquisa e desenvolvimento de modelos. Esse pipeline é essencial para extrair _insights_ significativos, entender a natureza dos dados e, construir modelos de aprendizado de máquina eficazes. 
