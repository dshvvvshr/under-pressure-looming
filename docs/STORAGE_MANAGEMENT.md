# STORAGE MANAGEMENT

## Intelligent Decision History Storage

The system logs every decision for learning purposes, but implements **intelligent storage management** to prevent bloat.

---

## The Problem

Logging every request indefinitely would cause:
- **Storage bloat** - Files growing without limit
- **Memory issues** - Loading millions of decisions into RAM
- **Performance degradation** - Slower learning cycles
- **Cost concerns** - Unnecessary storage costs in production

---

## The Solution

**Three-tier storage architecture:**

```
┌─────────────────────────────────────────────────┐
│ ACTIVE FILE (Last 1,000 decisions)              │
│ - Fast access                                    │
│ - In-memory loading                              │
│ - Used for real-time learning                    │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ ARCHIVES (Compressed by month)                   │
│ - Gzip compression (~90% size reduction)         │
│ - Queryable for recent patterns                  │
│ - Used for historical analysis                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ CLEANUP (After retention period)                 │
│ - Automatic removal of old archives              │
│ - Configurable retention (default: 1 year)       │
│ - Export option before deletion                  │
└─────────────────────────────────────────────────┘
```

---

## How It Works

### Automatic Rotation

When active decisions exceed the limit (default: 1,000):

1. **Split** - Keep most recent 1,000 in active file
2. **Group** - Organize older decisions by month
3. **Compress** - Save to gzip archives (90% smaller)
4. **Clean** - Remove from active file

**Example:**
```
Before rotation:
- decisions.json: 2,500 decisions (100 KB)

After rotation:
- decisions.json: 1,000 decisions (40 KB)
- archives/decisions_2025-01.json.gz: 1,000 decisions (4 KB)
- archives/decisions_2025-02.json.gz: 500 decisions (2 KB)
```

### Compression

Archives use **gzip compression**:
- **Typical ratio:** 90% size reduction
- **50 decisions:** ~2 KB compressed (vs 20 KB uncompressed)
- **1,000 decisions:** ~40 KB compressed (vs 400 KB uncompressed)

### Retention Policy

Configurable retention period (default: 365 days):
- Archives older than retention period are **automatically deleted**
- Cleanup runs every 100 decisions
- Can be disabled by setting `retention_days=0` (keep forever)

---

## Configuration

### Default Settings

```python
StorageManager(
    storage_path="/path/to/data",
    max_active_decisions=1000,  # Keep last 1,000 in active file
    retention_days=365           # Keep archives for 1 year
)
```

### Customization

**For high-volume systems:**
```python
# Keep more in active file, shorter retention
StorageManager(
    max_active_decisions=5000,
    retention_days=90  # 3 months
)
```

**For long-term analysis:**
```python
# Standard active, longer retention
StorageManager(
    max_active_decisions=1000,
    retention_days=1825  # 5 years
)
```

**For unlimited storage:**
```python
# Never delete archives
StorageManager(
    max_active_decisions=1000,
    retention_days=0  # Keep forever
)
```

---

## Storage Estimates

### Small System (100 decisions/day)

| Timeframe | Active File | Archives | Total |
|-----------|-------------|----------|-------|
| 1 week    | 700 (28 KB) | 0        | 28 KB |
| 1 month   | 1,000 (40 KB) | 2 KB   | 42 KB |
| 1 year    | 1,000 (40 KB) | 140 KB | 180 KB |

### Medium System (1,000 decisions/day)

| Timeframe | Active File | Archives | Total |
|-----------|-------------|----------|-------|
| 1 week    | 1,000 (40 KB) | 240 KB | 280 KB |
| 1 month   | 1,000 (40 KB) | 1.2 MB | 1.24 MB |
| 1 year    | 1,000 (40 KB) | 14 MB  | 14.04 MB |

### Large System (10,000 decisions/day)

| Timeframe | Active File | Archives | Total |
|-----------|-------------|----------|-------|
| 1 week    | 1,000 (40 KB) | 2.8 MB | 2.84 MB |
| 1 month   | 1,000 (40 KB) | 12 MB  | 12.04 MB |
| 1 year    | 1,000 (40 KB) | 140 MB | 140.04 MB |

**Note:** With 1-year retention, old archives are deleted, so storage stabilizes.

---

## Storage Directory Structure

```
learning/data/
├── active/
│   ├── decisions.json          # Last 1,000 decisions
│   └── rules.json              # Learned detection rules
└── archives/
    ├── decisions_2025-01.json.gz
    ├── decisions_2025-02.json.gz
    └── decisions_2025-03.json.gz
```

---

## Operations

### View Storage Statistics

```python
from learning.self_evolving import learner

stats = learner.get_statistics()
storage = stats['storage']

print(f"Active decisions: {storage['active_decisions']}")
print(f"Active size: {storage['active_size_kb']:.2f} KB")
print(f"Archive count: {storage['archive_count']}")
print(f"Archive size: {storage['archive_size_kb']:.2f} KB")
print(f"Total size: {storage['total_size_kb']:.2f} KB")
```

### Export All Decisions

Before cleanup or for analysis:

```python
from learning.self_evolving import learner

# Export everything to a single file
learner.storage.export_all_decisions("/path/to/backup.json")
```

### Load Recent Decisions

For analysis without loading everything:

```python
from learning.self_evolving import learner

# Load last 30 days from active + archives
recent = learner.storage.load_recent_decisions(days=30)
print(f"Loaded {len(recent)} recent decisions")
```

### Manual Cleanup

```python
from learning.self_evolving import learner

# Remove archives older than retention period
learner.storage.cleanup_old_archives()
```

---

## Learning Impact

### What Learning Uses

The learning system uses:
- **Active file** - Always loaded (last 1,000 decisions)
- **Recent archives** - Loaded on-demand for pattern analysis
- **Learned rules** - Applied to all future decisions

### Evolution Cycle

Every 10 decisions:
1. Analyze active + recent decisions
2. Identify patterns in denied requests
3. Generate and test candidate rules
4. Deploy rules with >80% success rate

**The system learns from recent patterns, not ancient history.**

---

## Production Recommendations

### For API/Web Services

```python
StorageManager(
    max_active_decisions=2000,   # Higher volume
    retention_days=180           # 6 months
)
```

### For Content Moderation

```python
StorageManager(
    max_active_decisions=5000,   # Very high volume
    retention_days=90            # 3 months
)
```

### For Research/Analysis

```python
StorageManager(
    max_active_decisions=1000,   # Standard
    retention_days=0             # Keep forever
)
```

### For Embedded Systems

```python
StorageManager(
    max_active_decisions=500,    # Limited memory
    retention_days=30            # 1 month
)
```

---

## Performance Characteristics

### Memory Usage

- **Active decisions:** ~40 KB per 1,000 decisions in memory
- **Learned rules:** ~1 KB per 100 rules
- **Total:** Typically < 1 MB in memory

### Disk I/O

- **Save:** O(1) - Append to active file
- **Rotation:** O(n) - Only when exceeding limit
- **Load:** O(1) - Read active file only
- **Query:** O(k) - Read k recent archives

### Learning Performance

- **Evolution cycle:** Analyzes active + recent (typically < 2,000 decisions)
- **Rule testing:** O(n*m) where n = decisions, m = candidate rules
- **Typical cycle time:** < 1 second

---

## Monitoring

### Key Metrics

Monitor these in production:

```python
stats = learner.get_statistics()

# Decision rate
decisions_per_day = stats['total_decisions'] / days_running

# Storage growth
storage_growth_kb_per_day = stats['storage']['total_size_kb'] / days_running

# Archive accumulation
archives_per_month = stats['storage']['archive_count'] / months_running
```

### Alerts

Set alerts for:
- **Storage > 100 MB** - Consider reducing retention
- **Active decisions > max** - Rotation not working
- **Archive count > 100** - Cleanup not running

---

## Backup and Recovery

### Backup Strategy

**Option 1: Export periodically**
```bash
# Export all decisions to backup file
python3 -c "from learning.self_evolving import learner; \
            learner.storage.export_all_decisions('/backup/decisions.json')"
```

**Option 2: Copy storage directory**
```bash
# Backup entire storage directory
tar -czf backup.tar.gz learning/data/
```

### Recovery

**From export:**
```python
import json
from learning.self_evolving import learner

with open('/backup/decisions.json') as f:
    decisions = json.load(f)

learner.storage.save_decisions(decisions)
```

**From directory backup:**
```bash
# Restore storage directory
tar -xzf backup.tar.gz -C learning/
```

---

## FAQ

**Q: Will I lose learning if archives are deleted?**  
A: No. Learned rules are stored separately and persist. Archives are just historical data.

**Q: Can I increase retention later?**  
A: Yes, but already-deleted archives cannot be recovered.

**Q: What if I need unlimited storage?**  
A: Set `retention_days=0` to keep all archives forever.

**Q: How do I reduce storage usage?**  
A: Lower `max_active_decisions` and `retention_days`, then run cleanup.

**Q: Can I query old archived decisions?**  
A: Yes, use `export_all_decisions()` or manually decompress archives.

**Q: Does rotation affect learning?**  
A: No. Learning uses active + recent decisions, which includes archives.

---

## Summary

The storage system is designed to:
- ✅ **Scale** - Handle millions of decisions without bloat
- ✅ **Perform** - Fast access to recent decisions
- ✅ **Learn** - Maintain learning capability with limited storage
- ✅ **Adapt** - Configurable for different use cases
- ✅ **Protect** - Automatic cleanup prevents runaway growth

**You get unlimited logging with bounded storage.**

---

Copyright (c) 2025 Branton Allan Baker. All rights reserved.
Credibility License (Concept Principle Attribution) 1.0
