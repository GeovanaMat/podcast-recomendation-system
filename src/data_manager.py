import csv
import os
import pandas as pd

class DataManager:
    """Responsável por carregar e salvar os dados de avaliações."""

    PODCASTS_DISPONIVEIS = [
        "The_Daily", "Up_First", "BBC_Global_News", "Today_in_Focus",
        "NPR_Politics", "Lex_Fridman", "Waveform_MKBHD", "Darknet_Diaries",
        "How_I_Built_This", "Radiolab", "Huberman_Lab", "The_Mindset_Mentor",
        "The_Happiness_Lab", "Tim_Ferriss_Show",
    ]

    def __init__(self, caminho_arquivo: str = os.path.join("data", "podcast_ratings_dataset.csv")):
        self.caminho_arquivo = caminho_arquivo

    def load_data(self) -> dict:
        """
        Carrega o arquivo CSV de avaliações e retorna um dicionário no formato:
        { 'ID_DO_USUARIO': {'NOME_DO_PODCAST': NOTA, ...} }
        """
        dados = {}

        with open(self.caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                usuario = linha.pop('Listener_ID')
                # Remove valores vazios e converte as notas válidas para float
                dados[usuario] = {
                    podcast: float(nota)
                    for podcast, nota in linha.items()
                    if nota.strip() != ''
                }

        return dados

    def save_user_rating(self, user_id, podcast_name, rating):
        """Atualiza a nota usando o Pandas."""

        df = pd.read_csv(self.caminho_arquivo)
        
        if podcast_name not in df.columns:
            raise ValueError(f"O podcast '{podcast_name}' não existe no CSV.")

        if user_id in df['Listener_ID'].values:
            df.loc[df['Listener_ID'] == user_id, podcast_name] = rating
        else:
            nova_linha = {'Listener_ID': user_id, podcast_name: rating}
            df = pd.concat([df, pd.DataFrame([nova_linha])], ignore_index=True)

        df.to_csv(self.caminho_arquivo, index=False)
