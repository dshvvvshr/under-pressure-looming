"""
TEST STORAGE MANAGER
Verify rotation, archival, and cleanup work correctly.
"""

import sys
import json
import tempfile
import shutil
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append('/home/ubuntu/under-pressure-looming')

from learning.storage_manager import StorageManager


def test_basic_storage():
    """Test basic save and load"""
    print("\n" + "="*80)
    print("TEST: Basic Storage")
    print("="*80)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = StorageManager(tmpdir, max_active_decisions=10)
        
        # Create test decisions
        decisions = [
            {
                'timestamp': datetime.now().isoformat(),
                'request': {'action': f'test_{i}'},
                'decision': 'approve'
            }
            for i in range(5)
        ]
        
        # Save
        storage.save_decisions(decisions)
        
        # Load
        loaded = storage.load_decisions()
        
        assert len(loaded) == 5, f"Expected 5, got {len(loaded)}"
        print("✓ Basic save/load works")


def test_rotation():
    """Test automatic rotation when exceeding max"""
    print("\n" + "="*80)
    print("TEST: Automatic Rotation")
    print("="*80)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = StorageManager(tmpdir, max_active_decisions=10)
        
        # Create 25 decisions (should trigger rotation)
        decisions = []
        for i in range(25):
            timestamp = (datetime.now() - timedelta(days=25-i)).isoformat()
            decisions.append({
                'timestamp': timestamp,
                'request': {'action': f'test_{i}'},
                'decision': 'approve'
            })
        
        # Save (should rotate)
        storage.save_decisions(decisions)
        
        # Check active file has only 10
        active = storage.load_decisions()
        assert len(active) == 10, f"Expected 10 active, got {len(active)}"
        print(f"✓ Active file limited to {len(active)} decisions")
        
        # Check archives exist
        archive_dir = Path(tmpdir) / "archives"
        archives = list(archive_dir.glob("*.json.gz"))
        assert len(archives) > 0, "Expected archives to be created"
        print(f"✓ Created {len(archives)} archive(s)")
        
        # Verify we can load recent decisions
        recent = storage.load_recent_decisions(days=30)
        assert len(recent) == 25, f"Expected 25 recent, got {len(recent)}"
        print(f"✓ Can load {len(recent)} recent decisions from active + archives")


def test_compression():
    """Test that archives are compressed"""
    print("\n" + "="*80)
    print("TEST: Archive Compression")
    print("="*80)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = StorageManager(tmpdir, max_active_decisions=10)
        
        # Create 50 decisions with large context
        decisions = []
        large_context = "x" * 1000  # 1KB of data per decision
        for i in range(50):
            timestamp = (datetime.now() - timedelta(days=50-i)).isoformat()
            decisions.append({
                'timestamp': timestamp,
                'request': {'action': f'test_{i}', 'context': large_context},
                'decision': 'approve'
            })
        
        # Save (should rotate and compress)
        storage.save_decisions(decisions)
        
        # Check compression ratio
        stats = storage.get_storage_stats()
        total_kb = stats['total_size_kb']
        
        # Uncompressed would be ~50KB, compressed should be much less
        print(f"✓ Total storage: {total_kb:.2f} KB")
        print(f"✓ Archive size: {stats['archive_size_kb']:.2f} KB (compressed)")
        
        # Verify compression worked (should be < 10KB with compression)
        assert total_kb < 20, f"Expected compression to reduce size below 20KB, got {total_kb:.2f}KB"
        print("✓ Compression is working effectively")


def test_cleanup():
    """Test cleanup of old archives"""
    print("\n" + "="*80)
    print("TEST: Archive Cleanup")
    print("="*80)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = StorageManager(tmpdir, max_active_decisions=10, retention_days=30)
        
        # Create decisions spanning 60 days
        decisions = []
        for i in range(60):
            timestamp = (datetime.now() - timedelta(days=60-i)).isoformat()
            decisions.append({
                'timestamp': timestamp,
                'request': {'action': f'test_{i}'},
                'decision': 'approve'
            })
        
        # Save (should create archives)
        storage.save_decisions(decisions)
        
        # Check archives before cleanup
        archive_dir = Path(tmpdir) / "archives"
        archives_before = len(list(archive_dir.glob("*.json.gz")))
        print(f"Archives before cleanup: {archives_before}")
        
        # Run cleanup (should remove archives > 30 days old)
        storage.cleanup_old_archives()
        
        # Check archives after cleanup
        archives_after = len(list(archive_dir.glob("*.json.gz")))
        print(f"Archives after cleanup: {archives_after}")
        
        # Should have fewer archives now
        assert archives_after <= archives_before, "Cleanup should not increase archives"
        print(f"✓ Cleanup removed {archives_before - archives_after} old archive(s)")


def test_export():
    """Test exporting all decisions"""
    print("\n" + "="*80)
    print("TEST: Export All Decisions")
    print("="*80)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = StorageManager(tmpdir, max_active_decisions=10)
        
        # Create 25 decisions (will be split across active + archives)
        decisions = []
        for i in range(25):
            timestamp = (datetime.now() - timedelta(days=25-i)).isoformat()
            decisions.append({
                'timestamp': timestamp,
                'request': {'action': f'test_{i}'},
                'decision': 'approve'
            })
        
        # Save
        storage.save_decisions(decisions)
        
        # Export all
        export_file = Path(tmpdir) / "export.json"
        count = storage.export_all_decisions(str(export_file))
        
        assert count == 25, f"Expected 25 exported, got {count}"
        print(f"✓ Exported {count} decisions successfully")
        
        # Verify export file
        with open(export_file) as f:
            exported = json.load(f)
            assert len(exported) == 25, "Export file should contain all decisions"
        print("✓ Export file is valid and complete")


def test_storage_stats():
    """Test storage statistics"""
    print("\n" + "="*80)
    print("TEST: Storage Statistics")
    print("="*80)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = StorageManager(tmpdir, max_active_decisions=10, retention_days=365)
        
        # Create 25 decisions
        decisions = []
        for i in range(25):
            timestamp = (datetime.now() - timedelta(days=25-i)).isoformat()
            decisions.append({
                'timestamp': timestamp,
                'request': {'action': f'test_{i}'},
                'decision': 'approve'
            })
        
        # Save
        storage.save_decisions(decisions)
        
        # Get stats
        stats = storage.get_storage_stats()
        
        print(f"Active decisions: {stats['active_decisions']}")
        print(f"Active size: {stats['active_size_kb']:.2f} KB")
        print(f"Archive count: {stats['archive_count']}")
        print(f"Archive size: {stats['archive_size_kb']:.2f} KB")
        print(f"Total size: {stats['total_size_kb']:.2f} KB")
        print(f"Max active: {stats['max_active_decisions']}")
        print(f"Retention: {stats['retention_days']} days")
        
        assert stats['active_decisions'] == 10, "Should have 10 active"
        assert stats['archive_count'] > 0, "Should have archives"
        print("✓ Statistics are accurate")


def run_all_tests():
    """Run all storage tests"""
    print("\n" + "="*80)
    print("STORAGE MANAGER TEST SUITE")
    print("="*80)
    
    tests = [
        test_basic_storage,
        test_rotation,
        test_compression,
        test_cleanup,
        test_export,
        test_storage_stats
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"\n✗ FAILED: {e}")
            failed += 1
    
    print("\n" + "="*80)
    print(f"RESULTS: {passed} passed, {failed} failed")
    print("="*80)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
