# 🎬 Bollywood Movie Recommendation System

A **Bollywood Movie Recommendation System** built using **content-based filtering**, enhanced with **popularity-aware ranking**, and deployed using **Streamlit Cloud**.  
The application dynamically displays **IMDb movie posters and ratings** using the **OMDb API** and provides an explainable, interactive user interface.

---

## 🔗 Live Demo
👉 **Live App**: https://bollywood-movie-recommendation-system.streamlit.app/
👉 **GitHub Repo**: https://github.com/pranayk15/Bollywood-Movie-Recommendation-System

---

## 🚀 Features

- 🎥 Bollywood-only movie recommendations  
- 🧠 Content-based filtering using TF-IDF  
- ⭐ Popularity-aware ranking to avoid outdated movies  
- 🖼️ IMDb posters & ratings via OMDb API  
- 🌙 Netflix-style dark UI  
- 🖱️ Hover animations and fixed-size movie cards  
- 📊 Explainable sidebar describing model logic  
- ☁️ Deployed on Streamlit Cloud  

---

## 🧠 How the Recommendation Model Works

### 🔹 Model Type
**Content-Based Recommendation System**

The model recommends movies based on similarity in content rather than user behavior.

---

### 🔹 Features Used
- Movie overview  
- Genre  
- Director  
- Cast  
- Release year (used as popularity signal)

---

### 🔹 Text Vectorization
- TF-IDF Vectorizer  
- Removes common stopwords  
- Highlights important descriptive words  

**Key Parameters**
```
max_features = 8000
stop_words = "english"
```

---

### 🔹 Similarity Metric
- Cosine Similarity  
- Measures similarity between movie vectors  
- Score range: 0 (no similarity) to 1 (very similar)

---

### 🔹 Final Scoring Strategy
```
Final Score =
0.7 × Content Similarity
+ 0.3 × Popularity Score
```

- Content similarity ensures relevance  
- Popularity score reduces very old or obscure recommendations  

---

## 📐 System Architecture

### Recommendation Flow
mermaid
```
flowchart TD
    A[User selects a movie] --> B[Find movie index]
    B --> C[Compute cosine similarity]
    C --> D[Apply popularity weighting]
    D --> E[Select top 5 movies]
    E --> F[Fetch posters & IMDb ratings]
    F --> G[Display results in Streamlit UI]
```
