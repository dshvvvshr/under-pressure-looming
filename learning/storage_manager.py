"""
STORAGE MANAGER
Handles decision history with rotation, archival, and cleanup.

Prevents storage bloat while maintaining learning capability.
"""

import json
import gzip
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path


class StorageManager:
    """
    Manages decision history storage with intelligent rotation.
    
    Features:
    - Automatic rotation after N decisions
    - Compression of archived data
    - Configurable retention policy
    - Efficient querying of recent decisions
    - Cleanup of old archives
    
    Storage Strategy:
    - Active file: Last N decisions (default: 1000)
    - Archives: Compressed monthly/yearly files
    - Learning uses active + recent archives
    - Old archives can be purged based on retention policy
    """
    
    def __init__(self, 
                 storage_path: str | Path,
                 max_active_decisions: int = 1000,
                 retention_days: int = 365):
        """
        Initialize storage manager.
        
        Args:
            storage_path: Base path for storage
            max_active_decisions: Max decisions in active file before rotation
            retention_days: Days to keep archived data (0 = forever)
        """
        self.storage_path = Path(storage_path)
        self.max_active_decisions = max_active_decisions
        self.retention_days = retention_days
        
        # Create directories
        self.active_dir = self.storage_path / "active"
        self.archive_dir = self.storage_path / "archives"
        self.active_dir.mkdir(parents=True, exist_ok=True)
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        
        self.decisions_file = self.active_dir / "decisions.json"
        self.rules_file = self.active_dir / "rules.json"
    
    def save_decisions(self, decisions: List[Dict]):
        """
        Save decisions with automatic rotation.
        
        If decisions exceed max_active_decisions, rotate older ones to archive.
        """
        # Check if rotation is needed
        if len(decisions) > self.max_active_decisions:
            self._rotate_decisions(decisions)
        else:
            # Just save normally
            with open(self.decisions_file, 'w') as f:
                json.dump(decisions, f, indent=2)
    
    def _rotate_decisions(self, decisions: List[Dict]):
        """
        Rotate old decisions to compressed archive.
        
        Keeps most recent max_active_decisions in active file.
        Archives the rest by month.
        """
        # Split into active and to-archive
        active = decisions[-self.max_active_decisions:]
        to_archive = decisions[:-self.max_active_decisions]
        
        if not to_archive:
            return
        
        # Group archived decisions by month
        by_month = {}
        for decision in to_archive:
            timestamp = decision['timestamp']
            month_key = timestamp[:7]  # YYYY-MM
            if month_key not in by_month:
                by_month[month_key] = []
            by_month[month_key].append(decision)
        
        # Save each month to compressed archive
        for month_key, month_decisions in by_month.items():
            archive_file = self.archive_dir / f"decisions_{month_key}.json.gz"
            
            # If archive exists, append to it
            existing = []
            if archive_file.exists():
                with gzip.open(archive_file, 'rt') as f:
                    existing = json.load(f)
            
            # Combine and save
            combined = existing + month_decisions
            with gzip.open(archive_file, 'wt') as f:
                json.dump(combined, f, indent=2)
        
        # Save active decisions
        with open(self.decisions_file, 'w') as f:
            json.dump(active, f, indent=2)
        
        print(f"📦 Rotated {len(to_archive)} decisions to archive")
    
    def load_decisions(self) -> List[Dict]:
        """Load active decisions"""
        if not self.decisions_file.exists():
            return []
        
        with open(self.decisions_file, 'r') as f:
            return json.load(f)
    
    def load_recent_decisions(self, days: int = 30) -> List[Dict]:
        """
        Load recent decisions from active + archives.
        
        Useful for learning from recent patterns without loading everything.
        """
        cutoff = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff.isoformat()
        
        recent = []
        
        # Load from active file
        active = self.load_decisions()
        recent.extend([d for d in active if d['timestamp'] >= cutoff_str])
        
        # Load from recent archives
        for archive_file in sorted(self.archive_dir.glob("decisions_*.json.gz")):
            with gzip.open(archive_file, 'rt') as f:
                archived = json.load(f)
                recent.extend([d for d in archived if d['timestamp'] >= cutoff_str])
        
        return recent
    
    def save_rules(self, rules: List[Dict]):
        """Save detection rules"""
        with open(self.rules_file, 'w') as f:
            json.dump(rules, f, indent=2)
    
    def load_rules(self) -> List[Dict]:
        """Load detection rules"""
        if not self.rules_file.exists():
            return []
        
        with open(self.rules_file, 'r') as f:
            return json.load(f)
    
    def cleanup_old_archives(self):
        """
        Remove archives older than retention period.
        
        Only runs if retention_days > 0.
        """
        if self.retention_days == 0:
            return  # Keep forever
        
        cutoff = datetime.now() - timedelta(days=self.retention_days)
        cutoff_month = cutoff.strftime("%Y-%m")
        
        removed = 0
        for archive_file in self.archive_dir.glob("decisions_*.json.gz"):
            # Extract month from filename: decisions_YYYY-MM.json.gz
            month = archive_file.stem.replace("decisions_", "").replace(".json", "")
            
            if month < cutoff_month:
                archive_file.unlink()
                removed += 1
        
        if removed > 0:
            print(f"🗑️  Cleaned up {removed} old archives")
    
    def get_storage_stats(self) -> Dict:
        """Get storage statistics"""
        active_size = self.decisions_file.stat().st_size if self.decisions_file.exists() else 0
        
        archive_count = len(list(self.archive_dir.glob("decisions_*.json.gz")))
        archive_size = sum(f.stat().st_size for f in self.archive_dir.glob("decisions_*.json.gz"))
        
        active_count = len(self.load_decisions())
        
        return {
            'active_decisions': active_count,
            'active_size_kb': active_size / 1024,
            'archive_count': archive_count,
            'archive_size_kb': archive_size / 1024,
            'total_size_kb': (active_size + archive_size) / 1024,
            'max_active_decisions': self.max_active_decisions,
            'retention_days': self.retention_days
        }
    
    def export_all_decisions(self, output_file: str):
        """
        Export all decisions (active + archives) to a single file.
        
        Useful for analysis or backup.
        """
        all_decisions = []
        
        # Load active
        all_decisions.extend(self.load_decisions())
        
        # Load all archives
        for archive_file in sorted(self.archive_dir.glob("decisions_*.json.gz")):
            with gzip.open(archive_file, 'rt') as f:
                all_decisions.extend(json.load(f))
        
        # Sort by timestamp
        all_decisions.sort(key=lambda d: d['timestamp'])
        
        # Save
        with open(output_file, 'w') as f:
            json.dump(all_decisions, f, indent=2)
        
        print(f"📤 Exported {len(all_decisions)} decisions to {output_file}")
        return len(all_decisions)
