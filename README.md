# Sistemas de Recomendação de Podcasts

## Objetivo
Construir e avaliar um sistema de recomendação de podcasts utilizando filtragem colaborativa, com isso, a partir das notas que os ouvintes já deram a alguns podcasts, o sistema sugere outros que a pessoa ainda não avaliou e que provavelmente vai gostar.
## Fundamentação
Um sistema de recomendação é um algoritmo de inteligência artificial, que usa grandes bases de dados para prever, filtrar e sugerir aos usuários itens relevantes quando a um número grande de opções. As sugestões podem se basear em compras anteriores, histórico de buscas, informações demográficas e outros fatores, ajudando as pessoas a descobrirem produtos e serviços que não são tão populares, o que seria difícil encontrar sozinha. Como esses sitemas conseguem prever os interesses e desejos dos consumidores, os sistemas de recomendação são muito usados em streaming, marketplaces e e-commerce. [1](https://www.nvidia.com/en-us/glossary/recommendation-system/)

Para os sistemas de recomendação funcionar é preciso fazer coleta de dados, e estes dados podem ser explícitos (avaliações, classificações, curtidas e comentários dados pelo usuário) ou implícitos  (comportamento observado, como histórico de navegação, cliques, compras e buscas), não excluindo dados demográficos e psicográficos, para que seja possível encontrar usários com interesses semelhantes. Após isso, os dados são reunidos e armazenados, e podem ser estruturados ou não estruturados. Com esses dados devidamentes organizados e processados, é possível aplicar algoritmos de aprendizado de máquina para detectar padrões e correlações e assim gerar boas recomendações. Por último, realizamos a filtragem, onde são selecionados o itens mais relevantes resultantes da análise, aplicando regras e fórmulas matemáticas que dependem do tipo de mecanismo de recomendação usado. [2](https://www.ibm.com/br-pt/think/topics/recommendation-engine)

Existem vários algoritmos e técnicas de recomendação, porém será aplicado nesse projeto a Filtragem Colaborativa. 

### Filtragem Colaborativa

Os algoritmos de filtragem colaborativa recomendam itens (parte "filtragem") com base nas preferências de um grupo de usuários (parte "colaborativa"). Eles exploram a similaridade de comportamento entre os usuários e, a partir das interações anteriores entre usuários e itens, aprendem a prever interações futuras. Assim, se pessoas tomaram decisões parecidas no passado, é alta a probabilidade de concordarem em escolhas futuras, por isso, se o sistema sabe que dois usuários têm gostos semelhantes em filmes, pode recomendar a um deles um filme de que o outro já gosta. [1](https://www.nvidia.com/en-us/glossary/recommendation-system/)

<img width="200" height="200" alt="img-2" src="https://github.com/user-attachments/assets/6e434f45-02a7-49e8-ac0b-4db0d8db5434" />

Fonte: [Sistema de recomendação - Nvidia](https://www.nvidia.com/en-us/glossary/recommendation-system/)

### Recomendação por vizinhos mais próximos (K-nearest neighbors)
Na filtragem colaborativa, para encontrar boas recomendaçõe para um usuário, é preciso encontrar outros usuários que possuem comportamentos parecidos, e para isso, precisamos calcular a distância de um usuário a outro para encontrar itens que um usuários avaliou e outro não, e saber quais recomendações são melhores para enviar a um determinado usuário. Será aplicado nesse projeto uma comparação entre dois métodos de calcular a distância entre esses usuários, a Distância Euclidiana e Distância de Manhattan. Esses dois métodos foram escolhidos pela natureza dos dados, que são dados densos e que muito usuário realizaram a avaliação de vários podcasts.

#### Distância Euclidiana

É a medida em linha reta entre dois pontos, como a de uma régua, aplicada a espaços com qualquer quantidade de dimensões. Sua base é o teorema de Pitágoras, que relaciona a hipotenusa aos catetos de um triângulo retângulo [3](https://www.datacamp.com/pt/tutorial/euclidean-distance). 

Com 2 dimensões, a distância é:

<img width="598" height="144" alt="image" src="https://github.com/user-attachments/assets/5f925c4b-9e86-45bf-be42-e3740189e9bc" />

Neste trabalho, cada usuário é um ponto no espaço, cada podcast é um eixo e a nota é a posição naquele eixo. Quanto mais próximos dois pontos, mais semelhantes os gostos.

#### Distância Manhattan

Mede a separação entre dois pontos como se só fosse possível andar em linhas de uma malha quadriculada, e não em linha reta como na distância euclidiana. O nome faz alusão a um táxi que percorre os quarteirões de Manhattan, obrigado a seguir as ruas em ângulo reto. Em vez de elevar ao quadrado, ela simplesmente soma, dimensão por dimensão, o tamanho da diferença entre as coordenadas [4](https://www.datacamp.com/pt/tutorial/manhattan-distance).

<img width="480" height="154" alt="2022_11_image_480x360" src="https://github.com/user-attachments/assets/1ae87f57-f18a-436d-a728-5aeefc21e64b" />


## Dados

O dataset utilizando para aplicação do sistema de recomendação foi ["Podcast Listener Ratings Dataset"](https://www.kaggle.com/datasets/vatsalvaghasiya/podcast-listener-ratings-dataset), que pode ser encontrada no Kaggle. O dataset tem o contexto da popularização de podcasts nas áreas de notícias, tecnologia, ciência e desenvolvimento pessoal. O conjunto de dados reúne notas dadas por ouvintes a um grupo selecionado de podcasts populares e foi pensado para pesquisadores, estudantes e cientistas de dados interessados em sistemas de recomendação, modelagem de preferências e análise de entretenimento.

Estrutura:
- Identificador: uma coluna com o código único de cada ouvinte (Listener_ID no arquivo; a descrição do dataset a chama de User_ID).
- Itens: 14 colunas, cada uma representando um podcast, dentre eles: The Daily, The Joe Rogan Experience, Serial, TED Radio Hour, Freakonomics Radio, Planet Money, Science Vs, Radiolab, The Tim Ferriss Show, How I Built This, Huberman Lab, The School of Greatness, On Purpose, Hidden Brain.
- Notas: de 1 a 5, sendo 5 a maior preferência.
- Valores ausentes: células vazias indicam que o ouvinte não avaliou ou não ouviu aquele podcast.
- Formato: CSV, com uma linha por ouvinte e uma coluna por podcast, ou seja, uma matriz usuário × item. A descrição a classifica como esparsa, por ter muitas células vazias em potencial. Ao carregar, o código a converte em um dicionário {usuario: {podcast: nota}}.

## Método

### Visão geral

Adotou-se uma abordagem de **filtragem colaborativa baseada em usuários** (*user-based k-nearest neighbors*), na qual a nota que um usuário daria a um podcast ainda não avaliado é estimada a partir das notas dadas por usuários de perfil semelhante. O estudo compara duas medidas de dissimilaridade entre usuários, a distância **Euclidiana** e a distância de **Manhattan**, mantendo fixos os demais componentes do algoritmo. 

### Protocolo para avaliação

Na literatura de sistemas de recomendação, a qualidade costuma ser medida de duas maneiras: por métricas de erro, que comparam a nota prevista com a nota real (MAE e RMSE), ou por métricas de acurácia de classificação, que verificam se os itens certos aparecem na lista sugerida. Como o algoritmo produz uma nota prevista para cada podcast, é possível compará-la diretamente com a nota real escondida, o que torna as métricas de erro a escolha a melhor opção, no qual se oculta parte do perfil do usuário e tentar recuperá-la. Adotaram-se duas delas por serem complementares:

- o MAE é fácil de interpretar, já que está na mesma escala das notas (um MAE de 0,8 significa erro médio de 0,8 ponto);
- o RMSE eleva os erros ao quadrado antes de promediá-los e, por isso, penaliza mais as previsões muito erradas.

<img width="270" height="268" alt="image" src="https://github.com/user-attachments/assets/e88844e9-4899-4398-b1dd-7734264718d3" />


A avaliação segue um esquema de ocultação de notas (hold-out), aplicado repetidamente:

- Sorteia-se, com semente fixa, um conjunto de 20 usuários de teste.
- Para cada um, oculta-se uma parte de suas notas, mantendo-se ao menos uma nota visível. As notas dos demais usuários permanecem intactas. Os itens ocultados são escolhidos por amostragem sem reposição.
- O recomendador é executado sobre os dados restantes e prevê as notas dos itens ocultados.
- As previsões são comparadas com as notas reais.
- O procedimento é repetido 5 vezes, com sementes 42 a 46. As duas distâncias usam as mesmas sementes e, portanto, as mesmas divisões, o que torna a comparação pareada.

## Resultados

Parâmetros: `K = 9`, Manhattan calculada com `r = 1`, 20 usuários de teste, 5 repetições, `seed = 42`. Valores em média ± desvio entre repetições. Menor é melhor.

**Modo `random` (configuração do `evaluate.py`):**

| Método | MAE | RMSE |
|---|---|---|
| Euclidiana | 0,809 ± 0,016 | 1,020 ± 0,035 |
| Manhattan | 0,842 ± 0,033 | 1,048 ± 0,047 |



## Limitações

Os resultados possui algumas limitações em relação dos método e dos dados.  Um podcast só pode ser previsto se ao menos um dos K vizinhos o avaliou, e o catálogo tem apenas 14 itens. Na prática, a lista de sugestões é curta e pouco diversa.Outra limitação é o problema da partida a frio (cold start), que afeta usuários sem histórico. O conjunto de dados contém um caso extremo, o ouvinte L0438, sem nenhuma nota, e a interface bloqueia a geração de recomendações para quem tem menos de cinco avaliações. Essa trava, porém, está apenas na interface e o o algoritmo em si não reconhece a falta de informação. A avaliação também é restrita e utilizaram-se apenas o MAE e o RMSE, que medem a precisão das notas previstas, e não a qualidade da lista ordenada que o usuário de fato veria.

## Conclusão

O projeto entrega um recomendador colaborativo user-based funcional, com avaliação offline reprodutível e uma interface interativa. Os resultados mostram que o método supera uma linha de base simples (MAE ≈ 0,81 a 0,84 contra ≈ 0,95). Entre as duas distâncias comparadas, a Euclidiana teve desempenho um pouco melhor que a Manhattan neste conjunto de dados.

## Inicialização e Excução do Projeto

**Pré-requisitos:** Python 3.11 ou superior (as versões fixadas em `requirements.txt`, como `numpy 2.4` e `pandas 3.0`, exigem uma versão recente) e `pip`.

**1. Clonar/extrair o projeto e entrar na pasta**

```bash
cd podcast-recomendation
```

**2. Criar e ativar o ambiente virtual**

```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# Linux / macOS
source venv/bin/activate
```

**3. Instalar as dependências**

```bash
pip install -r requirements.txt
```

**4. Executar a interface web**

```bash
streamlit run app.py
```

O navegador abrirá em `http://localhost:8501`. Selecione um usuário, avalie podcasts (é preciso ter ao menos 5 avaliações) e clique em **Gerar Recomendações**.

**5. Executar a avaliação offline (opcional)**

Execute a partir da **raiz do projeto**, como módulo:

```bash
python -m src.evaluate
```

O script imprime MAE e RMSE (média ± desvio) para as métricas Euclidiana e Minkowski (com `r = 3` no código atual). Para obter os resultados da Manhattan descritos acima, altere `r = 3` para `r = 1` em `src/evaluate.py`. Parâmetros como `mode`, `num_test_users`, `k_neighbors`, `repetitions`, `seed` e `r` podem ser ajustados em `src/evaluate.py`.

