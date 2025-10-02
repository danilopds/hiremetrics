# HireMetrics - Job Market Analytics Dashboard

<div align="center">

<img src="frontend/src/assets/img/hire-metrics-logo-transparent.png" width="500" height="500">

**Comprehensive job market analytics for Brazilian developers, HR professionals and recruiters**

🌐 **[Visit HireMetrics](https://www.hiremetrics.com.br)** 🌐

<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/450ed07d-91b9-40f9-85db-4ca34a3e9df0" />
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/f65afa16-58ef-4c83-a043-1227cd282441" />
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/b7f97dc2-9fa8-4cf8-ae8e-0927f7fe98c1" />
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/6d9136e7-848a-4ba3-9b0e-0d866ee94b04" />
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/73c03192-3663-4512-aaf6-47b1154dce15" />
<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/9d8a1d96-da0c-4bc2-87ae-cd0c356373ab" />


[![Vue.js](https://img.shields.io/badge/Vue.js-3.x-4FC08D?style=for-the-badge&logo=vue.js)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-336791?style=for-the-badge&logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10+-2496ED?style=for-the-badge&logo=docker)](https://www.docker.com/)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](http://makeapullrequest.com)

</div>

## 🎯 Overview

**HireMetrics** is a modern, full-stack SaaS platform designed specifically for Brazilian developers, HR professionals and recruiters. It provides real-time job market analytics, comprehensive data visualization, and advanced reporting capabilities to help make informed hiring decisions.

### ✨ Key Features

- 📊 **Real-time Dashboard Analytics** - Job trends, skills analysis, and market insights
- 🗺️ **Interactive Geographic Visualization** - Job location mapping across Brazilian cities
- 📋 **Advanced Reporting** - CSV export with up to 50,000 records and granular filtering
- 🔍 **Smart Filtering System** - Multi-dimensional filters for precise data analysis
- 🌐 **Brazilian Portuguese Localization** - Complete localization for Brazilian market
- 🔒 **Enterprise Security** - JWT authentication, email verification, CORS and security headers

## 🚀 Quick Start

### Prerequisites

- **Docker & Docker Compose**
- **Node.js** (v16 or higher)
- **npm** (v7 or higher)
- **Python** (3.8 or higher)

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

6. **Access the application**
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

### Design
<img width="500" height="400" alt="image" src="https://github.com/user-attachments/assets/e5bac12d-e083-4cdc-bf11-2ed3bfb22692" />

Article in PT-BR explaining details of the solution design:
https://app.beehiiv.com/posts/2cbb85cb-fdaa-40d1-81a2-6885e5058c3e?sort=last_updated


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

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
