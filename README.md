# HireMetrics - Job Market Analytics Dashboard

<div align="center">

![HireMetrics Logo](frontend/src/assets/img/hire-metrics-logo-transparent.png)

**Comprehensive job market analytics for Brazilian HR professionals and recruiters**

[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

</div>

---

## 🎯 Overview

**HireMetrics** is a modern, full-stack SaaS platform designed specifically for Brazilian developers, HR professionals and recruiters. It provides real-time job market analytics, comprehensive data visualization, and advanced reporting capabilities to help make informed hiring decisions.

### ✨ Key Features

- 📊 **Real-time Dashboard Analytics** - Job trends, skills analysis, and market insights
- 🗺️ **Interactive Geographic Visualization** - Job location mapping across Brazilian cities
- 💳 **Subscription Management (planned)** - Stripe-based subscriptions present in codebase but currently disabled
- 💠 **Credits System** - Purchase and consume credits (Mercado Pago integration)
- 📋 **Advanced Reporting** - CSV export with up to 50,000 records and granular filtering
- 🔍 **Smart Filtering System** - Multi-dimensional filters for precise data analysis
- 🌐 **Brazilian Portuguese Localization** - Complete localization for Brazilian market
- 🔒 **Enterprise Security** - JWT authentication, email verification, CORS and security headers

---

## 🚀 Quick Start

### Prerequisites

- **Node.js** (v16 or higher)
- **npm** (v7 or higher)
- **Python** (3.8 or higher)
- **Docker & Docker Compose**
- **PostgreSQL** (13 or higher)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hiremetrics
   ```

2. **Set up environment variables**
   - Create a `.env` file at the repository root using `env.example` as a starting point and add ETL/database variables required by `docker-compose`.

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Run the ETL Pipeline**
    ```bash
    docker exec saas_hiremetrics_etl python etl_flow.py
    ```

5. **Install frontend dependencies and run**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

5. **Access the application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - pgAdmin: http://localhost:5050

## 🏗️ Architecture

### Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Frontend** | Vue 3 + Pinia + Vite | Modern reactive UI with state management |
| **Charts** | ECharts + MapLibre GL JS | Interactive data visualization |
| **Styling** | Tailwind CSS + Naive UI | Professional design system |
| **Backend** | FastAPI + SQLAlchemy | High-performance API with ORM |
| **Database** | PostgreSQL + DuckDB | Production data + analytical processing |
| **ETL** | dbt + Prefect | Data transformation and orchestration |
| **Infrastructure** | Docker + Docker Compose | Containerized deployment |
| **Payments** | Mercado Pago (active), Stripe (planned) | Credits active; subscriptions code present but disabled |

### Project Structure

```
hiremetrics/
├── frontend/                 # Vue.js frontend application
│   ├── src/
│   │   ├── api/             # API integration layer
│   │   ├── assets/          # Images, CSS and static assets
│   │   ├── components/      # Reusable UI components
│   │   │   ├── charts/      # Chart components (ECharts)
│   │   │   ├── common/      # Common UI components
│   │   │   ├── filters/     # Filter components
│   │   │   └── maps/        # Map components (MapLibre)
│   │   ├── config/          # Configuration files
│   │   ├── layouts/         # Layout components
│   │   ├── router/          # Vue Router configuration
│   │   ├── stores/          # Pinia state management
│   │   ├── styles/          # Style tokens and themes
│   │   ├── test/            # Test utilities
│   │   ├── utils/           # Utility functions
│   │   └── views/           # Page components
│   │       └── auth/        # Authentication views
│   ├── docs/                # Frontend documentation
│   ├── public/              # Static assets
│   └── package.json         # Frontend dependencies
├── backend/                  # FastAPI backend application
│   ├── app/
│   │   ├── utils/           # Backend utilities (auth, cache, etc.)
│   │   ├── config.py        # Configuration settings
│   │   ├── crud.py          # Database operations
│   │   ├── database.py      # Database connection
│   │   ├── main.py          # FastAPI application entry
│   │   ├── models.py        # SQLAlchemy database models
│   │   └── schemas.py       # Pydantic data schemas
│   ├── Dockerfile           # Backend container config
│   └── requirements.txt     # Python dependencies
├── etl/                      # Data pipeline
│   ├── dbt/                 # dbt transformation models
│   │   ├── models/          # dbt SQL models
│   │   │   ├── dashboard/   # Dashboard-specific models
│   │   │   ├── marts/       # Business logic layer
│   │   │   └── staging/     # Raw data staging
│   │   └── dbt_project.yml  # dbt configuration
│   ├── scripts/             # ETL orchestration scripts
│   ├── data/                # Raw data files
│   ├── logs/                # ETL process logs
│   ├── etl_flow.py          # Main ETL orchestration
│   └── requirements.txt     # ETL dependencies
├── containers/               # Database initialization
│   └── warehouse/           # SQL migration scripts
├── docker-compose.yml        # Multi-service orchestration
├── env.example              # Environment variables template
├── LICENSE                  # MIT license
└── package.json             # Root project dependencies
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add some amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

### Development Guidelines

- Follow the existing code style and conventions
- Update documentation as needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Vue.js** - Progressive JavaScript framework
- **FastAPI** - Modern Python web framework
- **dbt Labs** - Data transformation platform
- **Naive UI** - Vue 3 component library
- **ECharts** - Data visualization library
- **MapLibre GL JS** - Vector mapping library
- **Stripe** - Payment processing platform
- **Open Source Community** - For all the amazing tools and libraries

---

<div align="center">

**Built with ❤️**

[![Made with Vue.js](https://img.shields.io/badge/Made%20with-Vue.js-4FC08D?style=for-the-badge&logo=vue.js)](https://vuejs.org/)
[![Made with FastAPI](https://img.shields.io/badge/Made%20with-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)

</div>