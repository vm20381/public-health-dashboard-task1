import sys
from pathlib import Path

# Add src to path so imports work
sys.path.append(str(Path(__file__).parent))

from src.data_access import load_csv
from src.cleaning import clean_covid_df, to_records
from src.db.engine import get_engine
from src.db.models import Base
from src.db.crud_orm import bulk_insert
from sqlalchemy.orm import sessionmaker

def main():
    # Define paths
    dataset_path = Path("dataset/covid_19_data.csv")
    db_path = "covid_data.db"  # This will be created in the root folder

    print(f"Loading data from {dataset_path}...")
    try:
        df_raw = load_csv(str(dataset_path))
    except FileNotFoundError:
        print(f"Error: Dataset not found at {dataset_path}")
        return

    print("Cleaning data...")
    df_clean = clean_covid_df(df_raw)
    records = to_records(df_clean)
    print(f"Prepared {len(records)} records.")

    print(f"Creating database at {db_path}...")
    engine = get_engine(db_path)
    
    # Create tables
    Base.metadata.create_all(engine)
    
    # Create session
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    try:
        print("Inserting records (this might take a moment)...")
        # Clear existing data to avoid duplicates if run multiple times
        # session.execute("DELETE FROM covid_reports") 
        # session.commit()
        
        count = bulk_insert(session, records)
        print(f"Successfully inserted {count} records into 'covid_reports'.")
    except Exception as e:
        print(f"Error inserting data: {e}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    main()
