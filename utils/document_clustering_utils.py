from gensim import corpora, models
import nltk
import pyLDAvis
import pyLDAvis.gensim_models
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.preprocessing import Normalizer
from sklearn.pipeline import make_pipeline
from sklearn.metrics import silhouette_score
stop_words = nltk.corpus.stopwords.words()

# list_of_list_of_tokens = [["a","b","c"], ["d","e","f"]]
# ["a","b","c"] are the tokens of document 1, ["d","e","f"] are the tokens of document 2...


def lda(submissions, n):
    print('lda starting')
    dictionary_LDA = corpora.Dictionary(submissions)
    dictionary_LDA.filter_extremes(no_below=3, no_above=.4)
    corpus = [dictionary_LDA.doc2bow(list_of_tokens)
              for list_of_tokens in submissions]
    print('premodel')
    num_topics = n
    lda_model = models.LdaModel(corpus, num_topics=num_topics,
                                id2word=dictionary_LDA,
                                passes=4, alpha=[0.01]*num_topics,
                                eta=[0.01]*len(dictionary_LDA.keys()))
    return pyLDAvis.prepared_data_to_html(pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary_LDA))


def tfidf(submissions):
    vec = TfidfVectorizer(max_df=25, sublinear_tf=True)
    X = vec.fit_transform(submissions)
    return(X,vec)


def dim_reduction(X, n_comps):
    print(n_comps)
    svd = TruncatedSVD(n_components=n_comps)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)
    return (svd, lsa.fit_transform(X))


def choose_dim(X, max_n, percent_explained):
    for n in range(2, max_n):
        svd, X_lsa = dim_reduction(X, n)
        if svd.explained_variance_ratio_.sum() >= percent_explained:
            return(X_lsa,svd,n)
    return ('couldnt explain','','')


def cluster(X, n):
    km = KMeans(n_clusters=n)
    km.fit(X)
    return(km)

def choose_cluster(X, max_n):
    sil_max = 0
    best_n = 2
    best_km = None
    for n in range(2, max_n):
        km = cluster(X, n)
        sil = silhouette_score(X, km.labels_)
        print(f'sil:{sil}\nk:{n}')
        if sil > sil_max:
            sil_max = sil
            best_n = n
            best_km = km
    return (best_km, n)


def top_terms_cluster(svd,km,vec,k):
    original_space_centroids = svd.inverse_transform(km.cluster_centers_)
    order_centroids = original_space_centroids.argsort()[:, ::-1]
    terms = vec.get_feature_names()
    for i in range(k):
        print("Cluster %d:" % i, end='')
        for ind in order_centroids[i, :10]:
            print(' %s' % terms[ind], end='')
        print()


def lsa_cluster(submissions, max_dims, max_clusters, percent_variance):
    X, vec = tfidf(submissions)
    X_lsa, svd, dims = choose_dim(X, max_n=max_dims, percent_explained=percent_variance)
    if type(X_lsa) == str:
        print('couldnt explain variance')
        return
    km,n_clusters = choose_cluster(X_lsa,max_clusters if max_clusters<dims else dims)
    top_terms_cluster(svd,km,vec,n_clusters)

def load():
    s = None
    with open('posts.csv','r') as f:
        s = f.readlines()
    s = [x.rstrip() for x in s]
    lsa_cluster(s,100,15,.8)