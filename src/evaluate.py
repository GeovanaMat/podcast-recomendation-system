"""Executa a avaliação offline pelo terminal: python evaluate.py"""
from src.data_manager import DataManager
from src.evaluator import Evaluator
from src.recommender import Recommender


def main():
    users = DataManager().load_data()
    evaluator = Evaluator(Recommender())

    for metric in Evaluator.METRICS:
        # mesma semente => mesmas notas escondidas nas duas métricas (comparação justa)
        result = evaluator.run(users, mode="random", num_test_users=20,
                               k_neighbors=9, top_n=5, repetitions=5, seed=20,
                               metric=metric)

        print(f"\n=== {metric} (média ± desvio entre repetições) ===")
        for name, (m, s) in result["summary"].items():
            print(f"  {name:<16} {m:.3f} ± {s:.3f}")


if __name__ == "__main__":
    main()