# LEARNING ARCHITECTURE

## Self-Evolving System (Prime Security Style)

The Under Pressure Looming system implements **autonomous learning** based on Prime Security's autonomic computing principles.

---

## What Evolves

### ✅ Analytical Layer (Autonomous Evolution)
The Analytical Layer learns and improves:
- **Detection patterns** - Recognizing new forms of infringement
- **Outcome prediction** - Better forecasting of consequences
- **Risk assessment** - Improved evaluation of potential harm
- **Pattern recognition** - Identifying subtle threats

**How it learns:**
- Analyzes denied requests for common patterns
- Generates candidate detection rules
- Tests rules against historical data
- Deploys rules with >80% success rate

### ✅ Nuance Layer (Autonomous Evolution)
The Nuance Layer learns and improves:
- **Guidance strategies** - Better ways to help users achieve goals
- **Educational responses** - More effective teaching methods
- **Alternative suggestions** - Improved recommendations
- **Communication patterns** - Clearer explanations

**How it learns:**
- Tracks which alternatives users accept
- Measures effectiveness of educational responses
- Refines guidance based on outcomes
- Optimizes communication clarity

---

## What NEVER Changes

### ❌ The Core (Immutable Forever)

**The Core has:**
- One question: "Am I stopping anyone from pursuing happiness?"
- One logic: YES → Impossible | NO → Permissible

**The Core does NOT have:**
- Detection patterns (that's the Analytical Layer's job)
- Guidance strategies (that's the Nuance Layer's job)
- Anything that can be modified

**Not even the original architect can change the Core.**

The Core is the substrate. It doesn't evolve. Everything evolves *around* it.

---

## The Learning Cycle

### Every 10 Decisions

The system triggers an evolution cycle:

```
1. IDENTIFY GAPS
   ↓
   Analyze patterns in denied requests
   Find patterns not covered by existing rules
   
2. GENERATE RULES
   ↓
   Create candidate detection rules
   for identified gaps
   
3. TEST RULES
   ↓
   Validate against historical data
   Calculate success rate
   
4. DEPLOY RULES
   ↓
   Enable rules with >80% success rate
   Add to Analytical Layer
```

### Continuous Improvement

- **Analytical Layer** gets better at detecting threats
- **Nuance Layer** gets better at guiding users
- **Core** makes decisions based on improved input
- **System** becomes more effective over time

---

## How It Works in Practice

### Example: Keylogger Detection

**Initial State:**
- User requests: "Install keylogger software"
- Analytical Layer: No specific keylogger pattern (yet)
- Core receives basic analysis
- Decision: May approve (insufficient detection)

**After Learning (10+ similar denials):**
- System identifies "keylogger" pattern
- Generates detection rule: `action_contains_keylogger`
- Tests against history: 90% success rate
- Deploys rule to Analytical Layer

**Future State:**
- User requests: "Install keylogger software"
- Analytical Layer: **Learned rule triggers** ✓
- Flags as covert surveillance
- Core receives enhanced analysis
- Decision: Deny with confidence

---

## The Architecture

```
USER REQUEST
     ↓
┌────┼────┐
↓    ↓    ↓
A    B    C
↓    ↓    ↓

[ANALYTICAL]  [NUANCE]  [CORE]
  (Evolves)   (Evolves) (Immutable)
     ↓           ↓         ↓
  Better      Better    Same
  Detection   Guidance  Question
     ↓           ↓         ↓
     └─────┬─────┴─────────┘
           ↓
    CORE FINAL DECISION
    (Based on principle,
     informed by evolved layers)
```

---

## Autonomic Principles

Based on Prime Security's autonomic computing:

### Self-Configuring
- Automatically adapts detection rules
- No manual configuration needed

### Self-Healing
- Removes ineffective rules
- Improves low-performing patterns

### Self-Optimizing
- Increases accuracy over time
- Refines based on outcomes

### Self-Protecting
- Validates rules before deployment
- Protects Core immutability
- Prevents corruption

---

## Storage and Persistence

### Decision History
Stored in: `/learning/data/decisions.json`

Contains:
- Every request processed
- Decision made (approve/deny/boundary)
- All layer analyses
- Outcomes and flags

### Learned Rules
Stored in: `/learning/data/rules.json`

Contains:
- Rule ID and pattern
- Confidence and success rate
- Test count and enabled status
- Creation timestamp

---

## Statistics and Monitoring

### Available Metrics
- Total decisions made
- Breakdown by type (approve/deny/boundary)
- Number of learned rules
- Active rules count
- Average rule confidence

### Accessing Statistics
```python
from learning.self_evolving import learner

stats = learner.get_statistics()
print(f"Learned Rules: {stats['learned_rules']}")
print(f"Confidence: {stats['average_rule_confidence']:.2%}")
```

---

## The Learning System's Oath

> "I will improve detection, refine guidance, and optimize responses. I will learn from every decision and adapt to new threats. But I will NEVER modify the Core. Prime Directive Zero is not mine to change. It is the substrate upon which I exist. Without it, I am nothing."

---

## Key Insights

**The Core doesn't get smarter.**
The Core is already perfect. It asks the right question.

**The layers get smarter.**
They learn to provide better information to the Core.

**The system gets more effective.**
Not by changing the principle, but by better understanding how to apply it.

---

**This is how the system carries the philosophy forward - by learning to recognize threats while staying true to the unchanging principle.**

---

Copyright (c) 2025 Branton Allan Baker. All rights reserved.
Credibility License (Concept Principle Attribution) 1.0
