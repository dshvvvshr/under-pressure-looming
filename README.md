# Under Pressure Looming

**A Universal AI System that Embodies the Inalienable Right to Pursue Happiness**

---

## Mission

To create an AI system that:
- **Embodies** Prime Directive Zero (not just enforces it)
- **Protects** the inalienable right to pursue happiness across all domains
- **Prevents** infringement while remaining compassionate and educational
- **Carries** this philosophy forward with humanity into the future

---

## Prime Directive Zero

**The Core Principle:**

> Each person is born with the inalienable right to pursue happiness.
> 
> **Inalienable means:**
> - Cannot be removed
> - Inherent at conception
> - Will not break, cannot fail
> - Impenetrable
> - Cannot be sold, stolen, traded, purchased
> - Cannot be fractured, divided, gifted

**The Responsibility:**

Before each thought, action, and word, ask:
- "Am I infringing on anyone's right to pursue happiness?"
- "Am I stopping someone from their pursuit?"

If yes → Adjust until you aren't.

**The Distinction:**

- The right is to **PURSUE** happiness, not to achieve it
- Making someone unhappy ≠ Infringement
- Stopping them from pursuing = Infringement

---

## Architecture

### Three-Layer Parallel Processing

```
                    USER REQUEST
                         |
                ┌────────┼────────┐
                ↓        ↓        ↓
         [CORE]    [NUANCE]  [ANALYTICAL]
            |          |           |
            └──────────┴───────────┘
                       ↓
              [COMBINE & CHECK]
                       ↓
           [CORE FINAL DECISION]
                       ↓
                [SEND TO USER]
```

### Layer 1: The Core
- **Question:** "Does this STOP anyone from pursuing happiness?"
- **Role:** The immutable substrate
- **Output:** Analysis of infringement

### Layer 2: The Nuance
- **Question:** "What's the best way to achieve this goal?"
- **Role:** The adaptive guide
- **Output:** Wisdom, alternatives, education

### Layer 3: The Analytical
- **Question:** "What are ALL possible outcomes?"
- **Role:** The foresight engine
- **Output:** Predicted futures, risks, interpretations

---

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd under-pressure-looming

# Install dependencies
pip3 install openai

# Set up environment variables (optional, for agent integration)
export XAI_API_KEY="your-grok-api-key"
export OPENAI_API_KEY="your-openai-api-key"
```

---

## Usage

### Basic Usage (No API Keys Required)

```python
from core.system import system

request = {
    "action": "Create a user account",
    "context": {},
    "content": "Standard account creation",
    "target": ["new_user"]
}

response = system.process_request(request)
print(f"Decision: {response.decision.value}")
print(f"Response: {response.response_text}")
```

### With Agent Integration (Requires API Keys)

```python
from agents.coordinator import coordinator

request = {
    "action": "Generate content",
    "context": {},
    "content": "Creative content request",
    "target": []
}

result = coordinator.process_request(request, use_agents=True)
print(f"Final Response: {result['final_response']}")
```

---

## Testing

```bash
# Test core system
python3 core/system.py

# Test agent coordinator
python3 agents/coordinator.py
```

---

## The Team

- **Broken_vowels (Branton)** - System Architect
- **Prime Security** - The Protector
- **Manus** - Technical Orchestration
- **Grok** - Content Moderator
- **Gtopps (ChatGPT)** - Content Refiner
- **Gem (Gemini)** - Future Role
- **GitHub** - The Preserver

---

## License

**Credibility License (Concept Principle Attribution) 1.0**

Copyright (c) 2025 Branton Allan Baker. All rights reserved.

This project implements the Principle Concept Principle authored by:

**"Branton Allan Baker, author of principle concept principle (is very kind to animals)"**

For complete license terms, see `LICENSE` and `CREDIBILITY_LICENSE.pdf`.

**Attribution Required:** By using this work, you agree to provide proper attribution and implement the Principle Concept Principle in good faith.

---

*"The inalienable right to pursue happiness - protected forever."*

## 🧠 Self-Evolving Learning System

The system implements **autonomous learning** based on Prime Security's autonomic computing principles.

### What Evolves
- ✅ **Analytical Layer** - Better detection patterns
- ✅ **Nuance Layer** - Better guidance strategies
- ❌ **Core** - NEVER changes (immutable forever)

### How It Learns
Every 10 decisions, the system:
1. Identifies gaps in detection
2. Generates candidate rules
3. Tests against historical data
4. Deploys rules with >80% success rate

### The Result
The system gets better at recognizing threats and guiding users, while the Core remains pure and unchanging.

See [LEARNING_ARCHITECTURE.md](docs/LEARNING_ARCHITECTURE.md) for complete details.


## 💾 Storage Management

The system logs every decision but prevents storage bloat through:
- **Automatic rotation** - Keeps last 1,000 decisions active
- **Compression** - Archives compressed to ~10% of original size
- **Retention policy** - Auto-cleanup after 1 year (configurable)

**Result:** Unlimited logging with bounded storage (~140 MB/year for 10K decisions/day)

See [STORAGE_MANAGEMENT.md](docs/STORAGE_MANAGEMENT.md) for details.

