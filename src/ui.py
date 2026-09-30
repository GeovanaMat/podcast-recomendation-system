import streamlit as st

from src.data_manager import DataManager
from src.recommender import Recommender


class RecommenderApp:
    """Monta a interface Streamlit, usando DataManager e Recommender."""

    def __init__(self, data_manager: DataManager, recommender: Recommender):
        self.data_manager = data_manager
        self.recommender = recommender

    def render_historico(self, selected_user: str, users: dict):
        st.subheader(f"Histórico de {selected_user}")
        user_ratings = users.get(selected_user, {})

        if user_ratings:
            df_ratings = [
                {"Podcast": podcast, "Nota": nota}
                for podcast, nota in user_ratings.items()
            ]
            st.dataframe(df_ratings, use_container_width=True)
        else:
            st.info("Este usuário ainda não avaliou nenhum podcast.")

    def render_avaliacao(self, selected_user: str, podcasts: list):
        st.subheader("Avaliar / Atualizar Notas")
        with st.form("form_avaliacao"):
            podcast_input = st.selectbox("Selecione o Podcast:", podcasts)
            nota_input = st.slider("Nota (1 a 5):", min_value=1.0, max_value=5.0, step=0.5, value=3.0)
            submit_button = st.form_submit_button("Salvar Avaliação")

            if submit_button:
                self.data_manager.save_user_rating(selected_user, podcast_input, nota_input)
                st.success(f"Nota {nota_input} salva para '{podcast_input}'!")
                st.rerun()

    def render_recomendacoes(self, selected_user: str, users: dict):
        st.subheader("💡 Recomendações")
        
        # 1. Busca as avaliações do usuário e conta quantas existem
        user_ratings = users.get(selected_user, {})
        qtd_avaliacoes = len(user_ratings)
        
        # 2. Verifica se a condição de 5 podcasts foi atingida
        historico_suficiente = qtd_avaliacoes >= 5
        
        # 3. Se não for suficiente, exibe a mensagem de aviso
        if not historico_suficiente:
            faltam = 5 - qtd_avaliacoes
            st.warning(f"⚠️ Para gerar recomendações, você precisa avaliar pelo menos 5 podcasts. Faltam {faltam} avaliações (você tem {qtd_avaliacoes}/5).")
        
        # 4. Botão bloqueado (disabled) caso historico_suficiente seja False
        if st.button("Gerar Recomendações", type="primary", use_container_width=True, disabled=not historico_suficiente):
            
            # Cria as duas colunas somente após o clique do botão
            col_euclidiana, col_manhattan = st.columns(2)
            
            # --- COLUNA 1: EUCLIDIANA ---
            with col_euclidiana:
                st.write("**Metodologia: Euclidiana**")
                rec_euclidiana = self.recommender.recommend_euclidiana(selected_user, users)
                
                if not rec_euclidiana:
                    st.info("Não há recomendações disponíveis.")
                else:
                    df_euclidiana = [
                        {"Podcast": podcast, "Pontuação": round(score, 2)} 
                        for podcast, score in rec_euclidiana
                    ]
                    st.dataframe(df_euclidiana, use_container_width=True)

            # --- COLUNA 2: manhattan ---
            with col_manhattan:
                st.write("**Metodologia: manhattan**")
                rec_manhattan = self.recommender.recommend_manhattan(selected_user, users)
                
                if not rec_manhattan:
                    st.info("Não há recomendações disponíveis.")
                else:
                    df_manhattan = [
                        {"Podcast": podcast, "Pontuação": round(score, 2)} 
                        for podcast, score in rec_manhattan
                    ]
                    st.dataframe(df_manhattan, use_container_width=True)

    def run(self):
        st.title("Sistema de Recomendação Colaborativo de Podcast")

        users = self.data_manager.load_data()
        user_ids = list(users.keys())

        selected_user = st.selectbox("Selecione o usuário:", user_ids)

        if selected_user:
            # Layout em colunas para Histórico e Avaliação
            col_historico, col_avaliar = st.columns(2)

            with col_historico:
                self.render_historico(selected_user, users)

            with col_avaliar:
                self.render_avaliacao(selected_user, self.data_manager.PODCASTS_DISPONIVEIS)
                
            st.divider()
            
            # Chama o módulo de recomendações (agora também em colunas)
            self.render_recomendacoes(selected_user, users)