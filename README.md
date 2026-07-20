# Tirumala Pulse

Tirumala Pulse is an automated ETL pipeline that extracts daily Tirumala Tirupati Devasthanams (TTD) statistics from the official TTD News website, parses operational metrics, and stores them in Supabase for historical analysis and reporting.

The project supports both:

- **Daily ETL** – Processes the latest published statistics every day.
- **Historical Backfill** – Processes all historical statistics with checkpoint-based resume capability.

---

# Features

- Automated daily ETL
- Historical backfill
- Checkpoint resume support
- Duplicate detection
- Supabase integration
- GitHub Actions automation
- Structured logging
- Modular architecture
- Python package with CLI support

---

# Architecture

```
                   +----------------------+
                   |  GitHub Actions      |
                   +----------+-----------+
                              |
                              |
                +-------------v-------------+
                |        ETL Service        |
                +-------------+-------------+
                              |
                  Fetch latest TTD posts
                              |
                              |
                +-------------v-------------+
                |     TTD News API Client   |
                +-------------+-------------+
                              |
                              |
                +-------------v-------------+
                |   Statistics Parser       |
                +-------------+-------------+
                              |
                              |
                +-------------v-------------+
                | ProcessPostService        |
                +-------------+-------------+
                              |
                              |
                +-------------v-------------+
                | Supabase Repository       |
                +---------------------------+
```

---

# Project Structure

```
tirumala-pulse/
│
├── .github/
│   └── workflows/
│       ├── daily-etl.yml
│       └── backfill.yml
│
├── src/
│   └── tirumala_pulse/
│       ├── api/
│       ├── config/
│       ├── database/
│       ├── models/
│       ├── parsers/
│       ├── repositories/
│       ├── services/
│       ├── utils/
│       └── main.py
│
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# Technologies

- Python 3.12+
- Requests
- Supabase
- GitHub Actions
- PostgreSQL
- python-dotenv

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/tirumala-pulse.git
cd tirumala-pulse
```

Install the project.

```bash
pip install -e .
```

---

# Configuration

Create a `.env` file.

```text
SUPABASE_URL=YOUR_SUPABASE_URL
SUPABASE_KEY=YOUR_SUPABASE_KEY

TTD_NEWS_BASE_URL=https://news.tirumala.org
```

---

# Running Daily ETL

```bash
python -m tirumala_pulse.main etl
```

---

# Running Historical Backfill

Process every page.

```bash
python -m tirumala_pulse.main backfill
```

Process only five pages.

```bash
python -m tirumala_pulse.main backfill --max-pages 5
```

Restart from the beginning.

```bash
python -m tirumala_pulse.main backfill --reset
```

---

# GitHub Actions

## Daily ETL

Runs automatically every day.

Also supports manual execution using **Run workflow**.

---

## Historical Backfill

Runs manually from GitHub Actions.

Supports:

- max pages
- checkpoint reset

---

# Logging

The application logs:

- ETL start
- ETL completion
- Processed posts
- Statistics detected
- Execution time
- Exceptions
- Backfill progress
- Checkpoint updates

---

# Database

Main tables:

- daily_statistics
- etl_runs
- checkpoints

---

# Version

Current Version

```
v1.0.0
```

---

# Future Improvements

- Retry with exponential backoff
- Unit tests
- Docker deployment
- Data quality validation
- Monitoring dashboard
- Notifications on ETL failures

---

# License

MIT License

---

# Author

Sharath Nakka
