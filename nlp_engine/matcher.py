
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_match(job_text, resume_text):
    """Calculate text similarity using TF-IDF and cosine similarity."""

    if not job_text or not resume_text:
        return 0.0

    documents = [
        job_text.strip(),
        resume_text.strip()
    ]

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            sublinear_tf=True
        )

        matrix = vectorizer.fit_transform(documents)

        similarity = cosine_similarity(
            matrix[0:1],
            matrix[1:2]
        )[0][0]

        return round(float(similarity) * 100, 2)

    except ValueError:
        return 0.0
