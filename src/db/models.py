from sqlalchemy import Column, Integer, String, Float, DateTime, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class CovidReport(Base):
    """
    SQLAlchemy model for COVID-19 daily reports.
    
    Corresponds to the cleaned data schema:
    - sno: Integer (Primary Key)
    - observation_date: Date/DateTime
    - province_state: String (Nullable)
    - country_region: String
    - last_update: DateTime
    - confirmed: Integer (Nullable)
    - deaths: Integer (Nullable)
    - recovered: Integer (Nullable)
    """
    __tablename__ = "covid_reports"

    # We use 'sno' from the CSV as the primary key as it is unique, 

    sno = Column(Integer, primary_key=True, index=True)
    
    observation_date = Column(DateTime, index=True)
    province_state = Column(String, nullable=True)
    country_region = Column(String, index=True)
    last_update = Column(DateTime)
    
    # Counts are nullable integers
    confirmed = Column(Integer, nullable=True)
    deaths = Column(Integer, nullable=True)
    recovered = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<CovidReport(sno={self.sno}, country={self.country_region}, date={self.observation_date})>"
