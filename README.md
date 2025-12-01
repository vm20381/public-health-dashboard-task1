# Github Repo for PAI Individual Assignemnet Task 1
Task 1: Data Insights Dashboard for Public Health Reports
You have been asked to develop a Python-based data insights tool for a team of researchers analysing public health data (e.g., vaccination rates, disease outbreaks, or mental health reports).
The goal is to support data access, filtering, cleaning, summarisation, and presentation (not predictive modelling). This simulates what a software developer might build to support an AI or data science team.
Design and implement a Python program that:
 Core Functionalities*:
1.	Data Access & Loading
    o	Read data from at least one source:
        	Public dataset (e.g. CSV, JSON)
        	Public API (e.g. WHO, UK government data, etc.)
          	A database (e.g. relational database)
    o	Load the data into a local or cloud database.
2.	Data Cleaning & Structuring
    o  	Handle missing or inconsistent data
    o	Convert types (dates, numbers)
    o	Create data structures (e.g., dictionaries, lists of records)
3.	Filtering and Summary Views
    o	Allow users to filter data by criteria (e.g., country, date range, age group)
    o	Generate summaries such as:
        	Mean, min, max, or counts
        	Trends over time
        	Grouped results (e.g., by country or region)
4.	Presentation Layer
    o	Command-line interface (CLI), menu, or simple UI
    o	Generate visual outputs (e.g., charts with matplotlib, tables with pandas)
5.	Extension Features (according to the scenario’s requirements)  
    o	CRUD functionalities on the DB to create, read, update and delete the data.
    o	Export filtered data or summaries as CSV
    o	Log all the user activities into a log file
________________________________________

## Installation

To set up the project locally, follow these steps:

1.  **Clone the repository** or download the source code.
2.  **Create a virtual environment**:
    ```bash
    python3 -m venv .venv
    ```
3.  **Activate the virtual environment**:
    *   On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
    *   On Windows:
        ```bash
        .venv\Scripts\activate
        ```
4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run app**:
    ```bash
    streamlit run src/app.py
    ```
2. **Run tests:**:
    ```bash
    pytest -q
    ```

## Data

**Dataset**
The project uses the "Novel Corona Virus 2019 Dataset" from Kaggle, which contains comprehensive data on COVID-19 cases worldwide. Avaliable at the link below:
https://www.kaggle.com/datasets/sudalairajkumar/novel-corona-virus-2019-dataset