from django.shortcuts import render
from django.db import connections, OperationalError
from django.conf import settings
import pandas as pd
import sqlite3
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import re
import os


# 기존 뷰 함수들
def main(request):
    return render(request, 'index.html')


def anime_details(request):
    return render(request, 'anime-details.html')


def anime_watching(request):
    return render(request, 'anime-watching.html')


def blog(request):
    return render(request, 'blog.html')


def blog_details(request):
    return render(request, 'blog-details.html')


def categories(request):
    return render(request, 'categories.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


# 추가된 검색 기능
def check_table_exists(table_name):
    try:
        connection = connections['default']
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT 1 FROM {table_name} LIMIT 1;")
        return True
    except OperationalError:
        return False


def load_data():
    if check_table_exists('mainapp_steamgame'):
        connection = sqlite3.connect(os.path.join(settings.BASE_DIR, 'demo.db'))
        df_local = pd.read_sql_query('SELECT * FROM steam_game_data', connection)
        connection.close()
        return df_local
    return pd.DataFrame()  # Return an empty DataFrame if the table does not exist


df_global = load_data()


def preprocess_text(text):
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    text = text.lower()
    return text


if not df_global.empty:
    df_global['release_date'] = df_global['release_date'].fillna(pd.Timestamp.now())
    df_global['developer'] = df_global['developer'].fillna('')
    df_global['detailed_description'] = df_global['detailed_description'].fillna('')
    df_global['genre'] = df_global['genre'].fillna('')
    df_global['recommendation_count'] = df_global['recommendation_count'].fillna(0)
    df_global['detailed_description'] = df_global['detailed_description'].apply(preprocess_text)

    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df_global['detailed_description'])

    cosine_sim_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)
else:
    tfidf = None
    tfidf_matrix = None
    cosine_sim_matrix = None


def get_recommendations(query, cosine_sim_matrix_param=cosine_sim_matrix):
    if cosine_sim_matrix_param is None:
        return pd.DataFrame()

    query = preprocess_text(query)
    query_vec = tfidf.transform([query])
    sim_scores = linear_kernel(query_vec, tfidf_matrix).flatten()

    sim_scores = list(enumerate(sim_scores))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[:10]  # Get top 10 similar games

    game_indices = [i[0] for i in sim_scores]
    results = df_global.iloc[game_indices]
    results['similarity_score'] = [score for idx, score in sim_scores]
    results['similarity_score_int'] = (results['similarity_score'] * 10).astype(int)
    results = results.sort_values(by=['similarity_score_int', 'recommendation_count'], ascending=[False, False])
    results = results.drop(columns=['similarity_score_int'])

    return results


def search(request):
    query = request.GET.get('q', '')
    if query:
        results = get_recommendations(query, cosine_sim_matrix)
    else:
        results = pd.DataFrame()

    context = {
        'query': query,
        'results': results.to_dict('records')
    }
    return render(request, 'search_results.html', context)
