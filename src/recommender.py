from math import sqrt

class Recommender:
    """Implementa o filtro colaborativo baseado em vizinhos mais próximos."""

    # Distância de Minkowski entre dois usuários.
    @staticmethod
    def minkowski(rating1, rating2, r):
        distance = 0
        commonRatings = False
        for key in rating1:
            if key in rating2:
                distance += pow(abs(rating1[key] - rating2[key]), r)
                commonRatings = True

        if commonRatings:
            return pow(distance, 1/r)  # Retorna a raiz da soma das potências
        else:
            return 0  # Indica que não há itens em comum

    @staticmethod
    def euclidean(rating1, rating2):
        distance = 0
        commonRatings = False
        for key in rating1:
            if key in rating2:
                distance += (rating1[key] - rating2[key]) ** 2
                commonRatings = True

        if commonRatings:
            return sqrt(distance)
        else:
            return 0

    # Encontra os vizinhos mais próximos permitindo escolher a métrica
    def compute_nearest_neighbor(self, username, users, metric='euclidiana', r=3, k=5):
        distances = []

        for user in users:
            if user != username:
                if metric == 'minkowski':
                    distance = self.minkowski(users[user], users[username], r)
                else:
                    distance = self.euclidean(users[user], users[username])
                
                distances.append((distance, user))

        distances.sort()
        return distances[:k]  # Retorna apenas os K primeiros (menores distâncias)

    # Método interno para evitar repetir a lógica de agregação das notas
    def _gerar_recomendacoes_dos_vizinhos(self, username, users, nearest_neighbors):
        userRatings = users[username]
        item_scores = {}

        for distance, neighbor in nearest_neighbors:
            neighborRatings = users[neighbor]

            for artist, rating in neighborRatings.items():
                if artist not in userRatings:
                    if artist not in item_scores:
                        item_scores[artist] = [rating, 1]
                    else:
                        item_scores[artist][0] += rating  # Soma a nota
                        item_scores[artist][1] += 1       # Incrementa contador

        # Calcula a média das notas para cada item
        recommendations = []
        for artist, (total_rating, count) in item_scores.items():
            avg_rating = total_rating / count
            recommendations.append((artist, avg_rating))

        # Ordena pela maior nota média recebida dos K vizinhos
        return sorted(recommendations, key=lambda artistTuple: artistTuple[1], reverse=True)

    # FUNÇÃO 1: Recomendar por Euclidiana
    def recommend_euclidiana(self, username, users, k=9):
        nearest_neighbors = self.compute_nearest_neighbor(username, users, metric='euclidiana', k=k)
        return self._gerar_recomendacoes_dos_vizinhos(username, users, nearest_neighbors)

    # FUNÇÃO 2: Recomendar por Minkowski
    def recommend_minkowski(self, username, users, r=3, k=9):
        nearest_neighbors = self.compute_nearest_neighbor(username, users, metric='minkowski', r=r, k=k)
        return self._gerar_recomendacoes_dos_vizinhos(username, users, nearest_neighbors)