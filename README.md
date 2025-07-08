# 🛰️ Ogoto: CISA KEV Automation Pipeline

Ogoto is an automated vulnerability tracking system designed to ingest, analyze, and communicate updates from the [CISA Known Exploited Vulnerabilities (KEV) catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog).

The project runs entirely within Docker containers, is orchestrated using Docker Compose, and is developed in modular phases to support evolving threat intelligence and remediation workflows.

---

## 📦 Project Phases

### ✅ Phase 1 – Daily Ingestion
- Download the KEV CSV feed published by CISA.
- Detect new or changed entries.
- Load only new/updated entries into a MySQL database.
- Maintain a historical record of all entries and changes.

### 🛠 Phase 2 – Jira Integration
- Create or update Jira tickets based on KEV data.
- Apply filtering rules by severity, vendor, or due date.
- Add labels, assignees, and projects based on customizable logic.

### 🔔 Phase 3 – Microsoft Teams Notifications
- Push daily summary of new KEVs to a Teams channel.
- Optionally include priority alerts (e.g., ransomware-linked CVEs).
- Format messages using adaptive cards or basic JSON.

### 📊 Phase 4 – Grafana Dashboarding (Optional)
- Visualize trends in KEVs over time.
- Track affected vendors, products, and required actions.
- Display CVEs due soon or overdue.
- Enable alerting for high-risk patterns.

---

## 🧰 Technology Stack

| Component        | Tech                 |
|------------------|----------------------|
| Language         | Python 3.x           |
| Database         | MySQL                |
| Orchestration    | Docker + Docker Compose |
| Visualization    | Grafana (Phase 4)    |
| Integrations     | Jira (Phase 2), Teams (Phase 3) |

---

## 🧪 Development Setup

1. **Clone the repository**

```bash
git clone https://github.com/your-org/ogoto.git
cd ogoto
```

2. **Start the container ecosystem**

```bash
docker-compose up --build
```

3. **View logs and confirm ingestion**

```bash
docker-compose logs -f kev-loader
```

4. **Access MySQL (optional)**

```bash
docker exec -it ogoto-db mysql -u root -p
```

---

## 📁 Repository Structure

```
ogoto/
├── kev-loader/           # Python service to download and load KEV data
├── jira-bridge/          # (Planned) Jira integration
├── teams-notifier/       # (Planned) Teams messaging service
├── grafana-dashboard/    # (Optional) Grafana config and dashboards
├── mysql-init/           # Database schema and initialization scripts
├── docker-compose.yml    # Orchestration
└── README.md
```

---

## 🔒 Security

All containers are sandboxed and communicate via Docker networks. Secrets (such as Jira tokens) are stored in `.env` or Docker secrets and **not** checked into source control.

---

## 📌 Roadmap

- [x] Phase 1 – Ingest CISA KEV and store in MySQL
- [ ] Phase 2 – Jira ticket automation
- [ ] Phase 3 – Teams alert integration
- [ ] Phase 4 – Grafana dashboarding

---

## 🙌 Contributing

Contributions are welcome! Please open an issue or submit a pull request. For major changes, open a discussion first.

---

## 📜 License

Apache License 2.0. See `LICENSE` for details.
