"""
CRUD operations using Raw SQL.
"""
from typing import List, Dict, Any, Optional
from sqlalchemy import text
from sqlalchemy.engine import Connection

def create_report_sql(conn: Connection, report: Dict[str, Any]) -> None:
    """
    Create a new report using raw SQL INSERT.
    """
    sql = text("""
        INSERT INTO covid_reports (
            sno, observation_date, province_state, country_region, 
            last_update, confirmed, deaths, recovered
        ) VALUES (
            :sno, :observation_date, :province_state, :country_region, 
            :last_update, :confirmed, :deaths, :recovered
        )
    """)
    conn.execute(sql, report)
    conn.commit()

def get_reports_sql(
    conn: Connection, 
    country: Optional[str] = None, 
    start_date: Optional[str] = None, 
    end_date: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Retrieve reports using raw SQL SELECT with dynamic filtering.
    """
    query_str = "SELECT * FROM covid_reports WHERE 1=1"
    params = {}
    
    if country:
        query_str += " AND country_region = :country"
        params["country"] = country
        
    if start_date:
        query_str += " AND observation_date >= :start_date"
        params["start_date"] = start_date
        
    if end_date:
        query_str += " AND observation_date <= :end_date"
        params["end_date"] = end_date
        
    result = conn.execute(text(query_str), params)
    return [dict(row) for row in result.mappings()]

def update_report_sql(conn: Connection, sno: int, updates: Dict[str, Any]) -> bool:
    """
    Update a report using raw SQL UPDATE.
    """
    if not updates:
        return False
        
    set_clauses = []
    params = {"sno": sno}
    
    for key, value in updates.items():
        set_clauses.append(f"{key} = :{key}")
        params[key] = value
        
    query_str = f"UPDATE covid_reports SET {', '.join(set_clauses)} WHERE sno = :sno"
    
    result = conn.execute(text(query_str), params)
    conn.commit()
    
    return result.rowcount > 0

def delete_report_sql(conn: Connection, sno: int) -> bool:
    """
    Delete a report using raw SQL DELETE.
    """
    sql = text("DELETE FROM covid_reports WHERE sno = :sno")
    result = conn.execute(sql, {"sno": sno})
    conn.commit()
    
    return result.rowcount > 0
