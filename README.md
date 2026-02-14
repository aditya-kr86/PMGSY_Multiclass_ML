# PMGSY Multiclass ML Predictor

A production-ready machine learning web application for predicting **Pradhan Mantri Gram Sadak Yojana (PMGSY)** scheme classifications using IBM Cloud Machine Learning. Built with a clean, premium UI and modular architecture for scalability and maintainability.

## 🌟 Features

- **5 PMGSY Scheme Predictions**: Supports all scheme types
  - PMGSY-I (Phase 1)
  - PMGSY-II (Phase 2)
  - PMGSY-III (Phase 3)
  - RCPLWEA (Road Connectivity Project for Left Wing Extremism Areas)
  - PM-JANMAN (PM Janjatiya Adivasi Nyay Maha Abhiyan)

- **Quick Test Cases**: Pre-configured test cases with real dataset patterns for instant testing across all schemes
- **Interactive Visualizations**: 
  - Confidence gauge charts with color-coded zones
  - Probability distribution graphs
  - Real-time prediction feedback
- **Clean Premium UI**: Light theme with subtle shadows, Inter font, and minimal design
- **IBM Cloud Integration**: Secure REST API communication with Watson Machine Learning
- **Dataset Insights**: Live statistics including 2,189 records across 5 schemes

## 🛠️ Tech Stack

- **Frontend**: Streamlit 1.32+
- **Data Processing**: Pandas 2.1+, NumPy 1.26+
- **Visualizations**: Plotly 5.18+
- **ML Platform**: IBM Cloud Watson Machine Learning
- **Configuration**: Python-dotenv
- **HTTP Client**: Requests, urllib3

## 📂 Project Structure

```
PMGSY_Multiclass_ML/
├── app.py                      # Main Streamlit application entry point
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # Documentation
├── test_pmgsy_api.py         # API testing script
├── testApiKey.py             # API key validation
│
├── data/
│   └── PMGSY_DATASET.csv     # Training dataset (2,189 records)
│
└── src/
    ├── config.py             # Configuration singleton
    ├── test_cases.py         # Demo test cases for all schemes
    │
    ├── api/
    │   ├── __init__.py
    │   └── ibm_client.py     # IBM Cloud ML API client
    │
    ├── data/
    │   ├── __init__.py
    │   └── loader.py         # Dataset loader with caching
    │
    ├── ui/
    │   ├── __init__.py
    │   ├── styles.py         # Custom CSS styling
    │   ├── components.py     # UI components (header, forms, results)
    │   └── charts.py         # Plotly visualizations
    │
    └── logo/
        ├── pmgsy-logo.png    # PMGSY official logo
        └── ibm-cloud-logo.png # IBM Cloud logo
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- IBM Cloud account with Watson Machine Learning service

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/aditya-kr86/PMGSY_Multiclass_ML.git
   cd PMGSY_Multiclass_ML
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your IBM Cloud credentials (see Configuration section)
   ```

## ⚙️ Configuration

Create a `.env` file in the project root with your IBM Cloud credentials:

```env
# IBM Cloud API Key
# Get from: https://cloud.ibm.com/iam/apikeys
IBM_API_KEY=your_ibm_cloud_api_key_here

# Watson ML Deployment ID
# Get from: Watson Studio > Deployments > Your Model > Deployment ID
DEPLOYMENT_ID=your_watson_ml_deployment_id_here

# IBM Cloud Region (choose one)
# Options: us-south, eu-gb, eu-de, jp-tok, au-syd, kr-seo
IBM_REGION=us-south
```

### Getting IBM Cloud Credentials

1. **IBM API Key**:
   - Log in to [IBM Cloud](https://cloud.ibm.com)
   - Navigate to **Manage** → **Access (IAM)** → **API keys**
   - Click **Create an IBM Cloud API key**
   - Copy and save the key

2. **Deployment ID**:
   - Go to **Watson Studio** → **Deployments**
   - Select your deployed ML model
   - Copy the **Deployment ID** from the deployment details

3. **Region**:
   - Check your Watson ML service region in IBM Cloud dashboard
   - Common regions: `us-south` (Dallas), `eu-gb` (London), `eu-de` (Frankfurt)

> **⚠️ Security Note**: Never commit `.env` to version control. It's already listed in `.gitignore`.

## 💻 Usage

1. **Start the application**
   ```bash
   streamlit run app.py
   ```

2. **Access the web interface**
   - Open browser to `http://localhost:8501`

3. **Make predictions**
   - **Option A**: Use quick test case buttons for instant demo
   - **Option B**: Manually enter 13 input features:
     - State and District selection
     - New Habitations Connected (0-1000)
     - Total Road Length (km)
     - Number of Roads
     - Length of Roads (km)
     - Upgradation Length (km)
     - Through Routes Count
     - Through Routes Length (km)
     - Major Bridges Count
     - Sanctioned Cost (₹ Crore)
     - Tender Cost (₹ Crore)
     - Agreement Amount (₹ Crore)
     - Work Completion Date (days since epoch)

4. **View results**
   - Predicted PMGSY scheme
   - Confidence level (HIGH/MEDIUM/LOW)
   - Interactive gauge chart
   - Probability distribution across all schemes

## 🔌 API Integration

The application communicates with IBM Watson Machine Learning via REST API:

### Authentication Flow
```python
POST https://iam.cloud.ibm.com/identity/token
Headers:
  Content-Type: application/x-www-form-urlencoded
Body:
  grant_type=urn:ibm:params:oauth:grant-type:apikey
  apikey=<IBM_API_KEY>
```

### Prediction Request
```python
POST <ML_ENDPOINT>/deployments/<DEPLOYMENT_ID>/predictions
Headers:
  Authorization: Bearer <access_token>
  Content-Type: application/json
Body:
  {
    "input_data": [{
      "fields": ["feature1", "feature2", ...],
      "values": [[value1, value2, ...]]
    }]
  }
```

### Response Format
```json
{
  "predictions": [{
    "fields": ["prediction", "probability"],
    "values": [[
      "PMGSY-I",
      [0.75, 0.15, 0.05, 0.03, 0.02]
    ]]
  }]
}
```

## 📊 Dataset Information

- **Records**: 2,189 road connectivity projects
- **Features**: 13 numeric and categorical attributes
- **Target Variable**: PMGSY_SCHEME (5 classes)
- **Geographic Coverage**: Multiple states and districts across India
- **Scheme Distribution**:
  - PMGSY-I: Primary rural road connectivity
  - PMGSY-II: Consolidation and upgradation
  - PMGSY-III: Through routes and major routes
  - RCPLWEA: Left Wing Extremism affected areas
  - PM-JANMAN: Tribal and Adivasi regions

### Test Cases Included
- **Test Case 1**: PMGSY-I - East Godavari (High connectivity, 500 roads)
- **Test Case 2**: PMGSY-II - Guntur (Small upgradation, 13 roads)
- **Test Case 3**: PMGSY-III - Kurnool (Through routes, 23 roads, 8 bridges)
- **Test Case 4**: RCPLWEA - Banka, Bihar (16 major bridges, high cost)
- **Test Case 5**: PM-JANMAN - West Godavari (Recent project, 5 roads)

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings to functions and classes
- Keep modules focused and cohesive

## 📝 License

This project was developed as part of an educational internship program.

## 🙏 Acknowledgments

- **IBM Cloud**: Watson Machine Learning platform
- **PMGSY**: Government of India road connectivity initiative
- **Streamlit**: Open-source web framework
- **Plotly**: Interactive visualization library

## 📧 Contact

For questions or support, please open an issue in the repository.

---

**Built with ❤️ for rural connectivity and data-driven governance**
