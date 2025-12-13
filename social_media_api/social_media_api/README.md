# 🚀 Social Media API (social_media_api)

This project serves as the foundation for a scalable social media platform API, built using Django and Django REST Framework (DRF). The initial setup focuses on robust user management and token-based authentication.

**Repository:** `Alx_DjangoLearnLab`
**Directory:** `social_media_api`

---

## 🛠️ Project Setup and Installation

Follow these steps to set up the project environment and run the application locally.

### 1. Prerequisites

* Python 3.8+
* pip (Python package installer)

### 2. Environment Setup

It is highly recommended to use a virtual environment:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment (Linux/macOS)
source venv/bin/activate

# Activate the virtual environment (Windows)
.\venv\Scripts\activate

Method,Endpoint,Description,Authentication Required?
POST,/api/accounts/register/,Creates a new CustomUser and returns an authentication token.,No
POST,/api/accounts/login/,Authenticates an existing user and returns a new token.,No
GET,/api/accounts/profile/,"Retrieves the authenticated user's profile data (bio, follower counts, etc.).",Yes (Token)
PATCH/PUT,/api/accounts/profile/,"Updates the authenticated user's profile details (bio, profile_picture).",Yes (Token)