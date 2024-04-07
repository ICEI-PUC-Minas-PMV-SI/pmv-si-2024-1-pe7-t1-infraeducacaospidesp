# Conhecendo os dados

Nesta seção, você deverá registrar uma detalhada análise descritiva e exploratória sobre a base de dados selecionada na Etapa 1 com o objetivo de compreender a estrutura dos dados, detectar eventuais _outliers_ e também, avaliar/detectar as relações existentes entre as variáveis analisadas.

Para isso, sugere-se que você utilize cálculos de medidas de tendência central, como média, mediana e moda, para entender a centralidade dos dados; explorem medidas de dispersão como desvio padrão e intervalos interquartil para avaliar a variabilidade dos dados; utilizem gráficos descritivos como histogramas e box plots, para representar visualmente as características essenciais dos dados, pois essas visualizações podem facilitar a identificação de padrões e anomalias; analisem a relação aparente entre as variáveis por meio de análise de correlação ou gráficos de dispersões, entre outras técnicas. 

Inclua nesta seção, gráficos, tabelas e demais artefatos que você considere relevantes para entender os dados com os quais você irá trabalhar. 

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

