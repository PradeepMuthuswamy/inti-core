"""
Database module for storing and retrieving estimates
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
import os

class EstimationDatabase:
    """Handles database operations for estimates"""
    
    def __init__(self, db_path: str = "data/estimates.db"):
        self.db_path = db_path
        self._create_database()
    
    def _create_database(self):
        """Create database and tables if they don't exist"""
        # Create data directory if it doesn't exist
        db_dir = os.path.dirname(self.db_path)
        if db_dir:  # Only create directory if there is one
            os.makedirs(db_dir, exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create estimates table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS estimates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                material TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                finish TEXT NOT NULL,
                testing TEXT NOT NULL,
                cad_properties TEXT NOT NULL,
                cost_breakdown TEXT NOT NULL,
                total_cost REAL NOT NULL,
                lead_time INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_estimate(self, 
                     filename: str,
                     material: str,
                     quantity: int,
                     finish: str,
                     testing: str,
                     cad_properties: Dict[str, Any],
                     cost_breakdown: Dict[str, Any]) -> int:
        """Save estimate to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO estimates 
            (filename, material, quantity, finish, testing, cad_properties, 
             cost_breakdown, total_cost, lead_time)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            filename,
            material,
            quantity,
            finish,
            testing,
            json.dumps(cad_properties),
            json.dumps(cost_breakdown),
            cost_breakdown['total_per_piece'],
            cost_breakdown['lead_time_weeks']
        ))
        
        estimate_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return estimate_id
    
    def get_estimates(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent estimates"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM estimates 
            ORDER BY created_at DESC 
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        estimates = []
        for row in rows:
            estimates.append({
                'id': row[0],
                'filename': row[1],
                'material': row[2],
                'quantity': row[3],
                'finish': row[4],
                'testing': row[5],
                'cad_properties': json.loads(row[6]),
                'cost_breakdown': json.loads(row[7]),
                'total_cost': row[8],
                'lead_time': row[9],
                'created_at': row[10]
            })
        
        return estimates
    
    def get_estimate_by_id(self, estimate_id: int) -> Optional[Dict[str, Any]]:
        """Get specific estimate by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM estimates WHERE id = ?
        ''', (estimate_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                'id': row[0],
                'filename': row[1],
                'material': row[2],
                'quantity': row[3],
                'finish': row[4],
                'testing': row[5],
                'cad_properties': json.loads(row[6]),
                'cost_breakdown': json.loads(row[7]),
                'total_cost': row[8],
                'lead_time': row[9],
                'created_at': row[10]
            }
        
        return None
    
    def delete_estimate(self, estimate_id: int) -> bool:
        """Delete estimate by ID"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM estimates WHERE id = ?', (estimate_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted

