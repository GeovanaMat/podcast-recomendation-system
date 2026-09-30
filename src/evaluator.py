import random
from math import sqrt
from statistics import mean, pstdev


class Evaluator:
    """
    Avaliação offline do recomendador (focada apenas em MAE e RMSE).

    Passos:
      1. Sorteia usuários de teste.
      2. Esconde parte das notas de cada um (mantendo as dos demais usuários).
      3. Gera recomendações com os dados restantes.
      4. Compara previsões com as notas escondidas usando MAE e RMSE.
    """

    MODES = ("random", "given_n", "all_but_n")
    METRICS = ("euclidiana", "minkowski")
    MIN_KNOWN = 1  # mínimo de notas que o usuário de teste mantém

    def __init__(self, recommender, relevance_threshold: float = 4.0):
        self.recommender = recommender
        self.relevance_threshold = relevance_threshold

    def _recommend(self, user, train, k, metric, r):
        """Chama o método do Recommender correspondente à métrica escolhida."""
        if metric == "minkowski":
            return self.recommender.recommend_minkowski(user, train, r=r, k=k)
        return self.recommender.recommend_euclidiana(user, train, k=k)

    # ---------- divisão treino / teste ----------
    @classmethod
    def _n_hide(cls, total, mode, n, rng):
        if mode == "given_n":
            hide = total - n
        elif mode == "all_but_n":
            hide = n if total - n >= cls.MIN_KNOWN else 0
        else:  # random
            max_hide = total - cls.MIN_KNOWN
            hide = rng.randint(1, max_hide) if max_hide >= 1 else 0
        return max(hide, 0)

    def split(self, users, mode="random", n=3, num_test_users=20, rng=None):
        """Retorna (treino, escondidas). Só os usuários de teste têm notas removidas."""
        rng = rng or random.Random()
        candidates = sorted(users)
        rng.shuffle(candidates)

        train = {u: dict(r) for u, r in users.items()}
        hidden = {}

        for user in candidates:
            if len(hidden) >= num_test_users:
                break
            ratings = users[user]
            n_hide = self._n_hide(len(ratings), mode, n, rng)
            if n_hide < 1:
                continue
            items = rng.sample(sorted(ratings), n_hide)
            hidden[user] = {item: ratings[item] for item in items}
            for item in items:
                del train[user][item]

        return train, hidden

    # ---------- métricas de uma execução (Apenas MAE e RMSE) ----------
    def evaluate_once(self, train, hidden, k_neighbors=9, top_n=5, metric="euclidiana", r=3):
        errors = []
        total_hidden = 0

        for user, hidden_ratings in hidden.items():
            recs = self._recommend(user, train, k_neighbors, metric, r)
            predicted = dict(recs)

            total_hidden += len(hidden_ratings)
            for item, real in hidden_ratings.items():
                if item in predicted:
                    errors.append(predicted[item] - real)

        def avg(values):
            return mean(values) if values else None

        return {
            "MAE": avg([abs(e) for e in errors]),
            "RMSE": sqrt(mean([e ** 2 for e in errors])) if errors else None,
            "Usuários testados": len(hidden),
            "Notas escondidas": total_hidden,
        }

    # ---------- execução completa (várias repetições) ----------
    def run(self, users, mode="random", n=3, num_test_users=5, k_neighbors=9,
            top_n=5, repetitions=5, seed=None, metric="euclidiana", r=3):
        if metric not in self.METRICS:
            raise ValueError(f"Métrica inválida: {metric}. Use uma de {self.METRICS}")
        if mode not in self.MODES:
            raise ValueError(f"Modo inválido: {mode}. Use um de {self.MODES}")

        runs = []
        for i in range(repetitions):
            rng = random.Random(None if seed is None else seed + i)
            train, hidden = self.split(users, mode, n, num_test_users, rng)
            if not hidden:
                continue
            runs.append(self.evaluate_once(train, hidden, k_neighbors, top_n, metric, r))

        summary = {}
        if runs:
            for metrica_chave in runs[0]:
                if metrica_chave in ("Usuários testados", "Notas escondidas"):
                    continue
                values = [r[metrica_chave] for r in runs if r[metrica_chave] is not None]
                if values:
                    summary[metrica_chave] = (mean(values), pstdev(values))

        return {"runs": runs, "summary": summary}