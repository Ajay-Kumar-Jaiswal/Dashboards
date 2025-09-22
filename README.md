# 📊 Netflix Data Analysis Dashboard

An interactive **Netflix Dashboard** built with **Plotly Dash** to visualize Netflix data including movies, TV shows, ratings, durations, countries, and yearly trends.

---

## 🌟 Features

- **Type & Rating:** Compare Movies vs TV Shows and their content ratings (PG, R, TV-MA, etc.)  
- **Movie Duration:** Distribution of movie durations with interactive histogram  
- **Release & Country:** Explore releases per year and top 10 countries with the most content  
- **Yearly Comparison:** Movies vs TV Shows released per year  

✅ Fully interactive with **hover info**, **zoom**, and **filtering**  

---

## 📂 Dataset

Dataset used: `netflix_titles.csv`  
You can include your CSV or download from [Kaggle Netflix Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows)

Columns used:  
- `type` – Movie or TV Show  
- `release_year`  
- `rating`  
- `country`  
- `duration`  

---

## 🛠️ Libraries Used

- `pandas` – Data manipulation  
- `plotly` – Interactive charts (Plotly Express & Graph Objects)  
- `dash` – Dashboard and interactive web app  

---

## 📝 Prerequisites

Before running the dashboard, make sure you have:

- Python 3.8 or higher installed  
- pip installed (Python package manager)  
- `netflix_titles.csv` dataset in the project directory  

---

## ⚙️ Installation and Setup

1. **Clone the repository**
```bash
git clone https://github.com/Ajay-Kumar-Jaiswal/Dashboards
cd Dashboards

```
2. **Create a virtual environment (optional but recommended)**
```bash
python -m venv venv

```
3. **Activate the virtual environment**    
For Windows:
```bash
venv\Scripts\activate
```
For macOS/Linux:
```bash
source venv/bin/activate

```
4. **Install dependencies**
```bash
pip install -r requirements.txt

```
5. **Run the dashboard**
```bash
python app.py

```
6. **Open your browser**
```bash
for example http://127.0.0.1:8050

