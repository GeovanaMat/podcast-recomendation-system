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
Na filtragem colaborativa, para encontrar boas recomendaçõe para um usuário, é preciso encontrar outros usuários que possuem comportamentos parecidos, e para isso, precisamos calcular a distância de um usuário a outro para encontrar itens que um usuários avaliou e outro não, e saber quais recomendações são melhores para enviar a um determinado usuário. Será aplicado nesse projeto uma comparação entre dois métodos de calcular a distância entre esses usuários, a Distância Euclidiana e Distância de Minkowski. Esses dois métodos foram escolhidos pela natureza dos dados, que são dados densos e que muito usuário realizaram a avaliação de vários podcasts.



## Dados
## Método
## Resultados
## Limitações
## Conclusão
## Inicialização e Excução do Projeto

