# n8n Workflows Popularity Tracker

A FastAPI application that fetches and stores popular **n8n workflows** from YouTube, forums, and Google Trends. It calculates popularity scores and provides a REST API to access top workflows.

---

## **Features**

- Fetch popular workflows from:
  - YouTube
  - n8n Forums
  - Google Trends
- Calculate popularity scores for each workflow
- Store data in PostgreSQL (local or cloud)
- Expose REST API for top workflows
- Compatible with Render PostgreSQL deployments

---

## **Technologies Used**

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- LangChain + Gemini for workflow filtering
- dotenv for environment variables

---

## **Installation**

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/popular_n8n_workflows.git
cd popular_n8n_workflows
