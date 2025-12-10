"""
CRUD operations using SQLAlchemy ORM.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from src.db.models import CovidReport

def create_report(session: Session, report_dict: Dict[str, Any]) -> int:
    """
    Create a new COVID report.
    
    Args:
        session: Database session.
        report_dict: Dictionary containing report data.
        
    Returns:
        int: The ID (sno) of the created report.
    """
    report = CovidReport(**report_dict)
    session.add(report)
    session.commit()
    session.refresh(report)
    return report.sno

def get_reports(
    session: Session, 
    country: Optional[str] = None, 
    start_date: Optional[datetime] = None, 
    end_date: Optional[datetime] = None
) -> List[CovidReport]:
    """
    Retrieve reports with optional filtering.
    
    Args:
        session: Database session.
        country: Filter by country/region.
        start_date: Filter by start date (inclusive).
        end_date: Filter by end date (inclusive).
        
    Returns:
        List[CovidReport]: List of matching reports.
    """
    query = session.query(CovidReport)
    
    if country:
        query = query.filter(CovidReport.country_region == country)
    
    if start_date:
        query = query.filter(CovidReport.observation_date >= start_date)
        
    if end_date:
        query = query.filter(CovidReport.observation_date <= end_date)
        
    return query.all()

def update_report(session: Session, sno: int, updates: Dict[str, Any]) -> bool:
    """
    Update an existing report.
    
    Args:
        session: Database session.
        sno: The Serial Number ID of the report to update.
        updates: Dictionary of fields to update.
        
    Returns:
        bool: True if updated, False if not found.
    """
    report = session.query(CovidReport).filter(CovidReport.sno == sno).first()
    if not report:
        return False
        
    for key, value in updates.items():
        if hasattr(report, key):
            setattr(report, key, value)
            
    session.commit()
    return True

def delete_report(session: Session, sno: int) -> bool:
    """
    Delete a report by ID.
    
    Args:
        session: Database session.
        sno: The Serial Number ID of the report to delete.
        
    Returns:
        bool: True if deleted, False if not found.
    """
    report = session.query(CovidReport).filter(CovidReport.sno == sno).first()
    if not report:
        return False
        
    session.delete(report)
    session.commit()
    return True

def bulk_insert(session: Session, records: List[Dict[str, Any]]) -> int:
    """
    Insert multiple records efficiently.
    
    Args:
        session: Database session.
        records: List of dictionaries containing report data.
        
    Returns:
        int: Number of records inserted.
    """
    # Use bulk_insert_mappings for performance
    session.bulk_insert_mappings(CovidReport, records)
    session.commit()
    return len(records)
