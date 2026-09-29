"""Ponto de entrada. Execute com: streamlit run app.py"""
from src.data_manager import DataManager
from src.recommender import Recommender
from src.ui import RecommenderApp


def main():
    data_manager = DataManager()
    recommender = Recommender()
    app = RecommenderApp(data_manager, recommender)
    app.run()


if __name__ == "__main__":
    main()
