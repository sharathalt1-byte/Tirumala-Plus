# Tirumala Pulse

Tirumala Pulse is a Python ETL application that collects daily Tirumala Tirupati Devasthanams (TTD) statistics from the official TTD News Portal, parses them, and stores them in Supabase for analytics and reporting.

## Features

- Official TTD REST API integration
- Daily statistics parser
- Raw report archival
- Duplicate detection
- Centralized logging
- ETL execution history
- Supabase integration

## Technology Stack

- Python 3.14
- Supabase (PostgreSQL)
- Requests
- WordPress REST API
- GitHub

## Project Structure

```
src/
    api/
    config/
    database/
    models/
    parsers/
    repositories/
    services/
    utils/
```

## Roadmap

- ✅ ETL Pipeline
- ✅ Logging
- ✅ Raw Report Storage
- ✅ ETL Monitoring
- 🚧 GitHub Actions
- 🚧 Historical Backfill
- 🚧 Power BI Dashboard