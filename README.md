---

## 🇦🇪 UAE Telecom Recommender System

This repository contains the modular architecture, datasets, and logic for building a **risk-aware recommender system** tailored to telecom infrastructure projects in the UAE.

### 🎯 Project Objective
To design a **stakeholder-ready recommender system** that supports decision-making across telecom sectors by:
- Mapping risks to RMS lifecycle stages  
- Aligning with sector-specific methodologies (Waterfall, Agile, Hybrid)  
- Enabling supervisor review, QA tracking, and recommender training

### 🧱 Repo Structure
- `risks_network_infra_waterfall_v1.csv` – 60-row lifecycle-tagged dataset  
- `risks_it_support_agile_v1.csv` – Agile risk register (coming soon)  
- `risks_cybersecurity_hybrid_v1.csv` – Hybrid risk register (coming soon)  
- `sample_network_risk_recommender.py` – Sample recommender logic  
- `test_risk_recommender.py` – Unit tests for recommender behavior  
- `legacy/` – Archived datasets and deprecated logic  
- `README.md` – Project overview and roadmap  
- `LICENSE` – Open-source license (MIT or custom)  
- `CHANGELOG.md` – Version history and lifecycle tagging

### 📊 Methodology Alignment
| Sector                  | Methodology | Rows | RMS Coverage       |
|------------------------|-------------|------|--------------------|
| Network Infrastructure | Waterfall   | 60   | Full lifecycle     |
| IT Support & Delivery  | Agile       | 60   | Full lifecycle     |
| Cybersecurity Ops      | Hybrid      | 60   | Full lifecycle     |

### 🧠 Recommender Logic
Each dataset includes:
- `Recommender_Tag` for model training  
- `Flag_Status` for QA tracking  
- Lifecycle-aware `Risk_ID` and `RMS_Stage` fields  
- Modular schema with 27 consistent headers

### 🔍 QA & Governance
- All datasets are flagged `Pending QA` until reviewed  
- Commit history reflects lifecycle blocks (e.g. R001–R060)  
- Branch protection and signed commits enforced for auditability

### 🚀 Roadmap
- [x] Upload Network Infrastructure dataset  
- [ ] Upload IT Support & Cybersecurity datasets  
- [ ] Draft README per sector  
- [ ] Finalize recommender logic and dashboard  
- [ ] Publish supervisor-ready portfolio

---
