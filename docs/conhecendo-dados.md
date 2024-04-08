# Conhecendo os dados

O processo de exploração dos dados foi baseado na manipulação e análise de dados provenientes de duas tabelas do dataset selecionado, intituladas "INFRAESTRUTURA" e "NOTAS_DO_IDESP". A tabela "INFRAESTRUTURA", representada pela filtragem presente na Tabela 2 a seguir, continha informações sobre diversas escolas, incluindo características de infraestrutura, como categoria, subcategoria, data de cadastro, quantidade e data de atualização e a a tabela "NOTAS_DO_IDESP", demonstrada pela filtragem presente na Tabela 2 a seguir, continha dados sobre o Índice de Desenvolvimento da Educação do Estado de São Paulo (IDESP) de diferentes escolas, bem como outras informações como o ano de aplicação e a data de cadastro.

![Tabela 1 - Infraestrutura das Escolas ](./img/Tabela_Infra_Escolas.png)

Tabela 1 - Infraestrutura das Escolas


![Tabela 2 - Notas do IDESP](./img/Tabela_Notas_Idesp.png)

Tabela 2 - Notas do IDESP

Inicialmente, os dados foram lidos e armazenados em estruturas de dados no VS CODE, em um programa feito em Python, utilizando a biblioteca Pandas. Em seguida, foi realizada uma filtragem e agrupamento dos dados da tabela "INFRAESTRUTURA", baseando-se, para isso, em determinadas categorias relevantes, como banheiros, cozinhas, esportes, laboratórios, leituras, outros e salas de aula. Posteriormente, as colunas foram renomeadas para facilitar a interpretação dos resultados.

Em um segundo momento, os dados das tabelas "INFRAESTRUTURA" e "NOTAS_DO_IDESP" foram mesclados com base no código da escola (COD_ESC). O resultado desse processo foi uma nova tabela contendo informações combinadas sobre infraestrutura e notas do IDESP para cada escola, contendo, inicialmente, as colunas "COD_ESC", "BANHEIROS", "COZINHA", "LABORATÓRIO","ESPORTE", "SALAS DE AULA", "LEITURA", "OUTROS", "IDESP_AI", "IDESP_AF", "DESP_EM", "ANO_APLICACAO" e "DTCADASTRO". Esse processo resultou no arquivo representado, com filtragem aplicada, pela Tabela 3 a seguir (mais detalhes do código aplicado podem ser vistos em ![mesclagem de dados](/./utils/main.py)).


![Tabela 3 - Infraestrutura das Escolas com Notas do IDESP ](./img/Tabela_Infra_E_Notas_Idesp.png)

Tabela 3 - Infraestrutura das Escolas Mescladas com Notas do IDESP



## Descrição dos achados

A análise foi realizada utilizando o mapa de calor como base após fazermos a união dos dados em um único dataset. Para isso utilizamos o python para unir a table de notas com a tabela de infraestrutura das escolas e poder analisar em um único dataset as informações que queremos cruzar.

![Canvas Analítico](./img/mapa_de_calor.png)

As correlações foram medidas através do coeficiente de correlação de Pearson, que indica a força e a direção da relação linear entre duas variáveis.

Resultados e Discussão

### Infraestrutura:

O IDESP_AF não apresentou correlação significativa com a infraestrutura escolar (coeficiente de correlação de Pearson de 0,03), indicando que outros fatores, como gestão escolar, qualificação dos professores e contexto socioeconômico dos alunos, influenciam mais o desempenho das escolas.

### Cozinhas e Salas de Aula:

Similarmente, não foi detectada correlação significativa entre o IDESP_AF e a qualidade das cozinhas (coeficiente de correlação de Pearson de 0,04) e das salas de aula (coeficiente de correlação de Pearson de 0,02).

### Esportes:

Uma correlação positiva fraca (coeficiente de correlação de Pearson de 0,10) foi observada entre o IDESP_AF e a presença de infraestrutura para esportes, sugerindo que escolas com melhores resultados no IDESP_AF tendem a ter mais recursos para atividades esportivas.

### Laboratórios e Leitura:

O IDESP_AF não apresentou correlação significativa com a presença de laboratórios (coeficiente de correlação de Pearson de 0,07) ou com o incentivo à leitura (coeficiente de correlação de Pearson de 0,09).

## Ferramentas utilizadas

Existem muitas ferramentas diferentes que podem ser utilizadas para fazer a análise dos dados. Nesta seção, descreva as ferramentas/tecnologias utilizadas e sua aplicação.

