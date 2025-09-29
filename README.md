# HireMetrics - Job Market Analytics Dashboard

<div align="center">

<img src="frontend/src/assets/img/hire-metrics-logo-transparent.png" width="500" height="500">

**Comprehensive job market analytics for Brazilian developers, HR professionals and recruiters**

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
