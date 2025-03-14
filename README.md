# AI Datacenter Analyst

A sophisticated AI-powered platform for conducting in-depth market research interviews in the AI datacenter industry. This application leverages OpenAI's GPT models to facilitate intelligent conversations with key market participants and synthesize valuable market insights.

## Overview

The AI Datacenter Analyst is designed to:
- Conduct automated, intelligent interviews with various market participants
- Collect and analyze key market data points
- Generate comprehensive market insights
- Track interview progress and data coverage
- Provide interactive visualization of market trends

## Key Features

### 1. AI-Powered Interviews
- Dynamic question generation based on participant type
- Adaptive follow-up questions
- Support for multiple participant categories:
  - Chipset Vendors
  - AI Accelerator Startups
  - Server Vendors
  - Hyperscalers
  - Cloud Service Providers
  - AI Software Companies
  - Datacenter Infrastructure Providers

### 2. Market Intelligence Dashboard
- Real-time data visualization
- Interactive charts and graphs
- Participant type distribution analysis
- Timeline view of interviews
- Comprehensive market coverage tracking

### 3. Market Insights Engine
- Automated correlation analysis
- Trend identification
- Key player analysis
- Technology advancement tracking
- Market outlook generation

### 4. Interactive Chatbot
- On-demand market information access
- Historical data querying
- Customized insights generation

## Technical Setup

### Prerequisites
- Python 3.11+
- PostgreSQL database
- OpenAI API key

### Environment Variables
```
DATABASE_URL=postgresql://[user]:[password]@[host]:[port]/[dbname]
OPENAI_API_KEY=your_openai_api_key
FLASK_SECRET_KEY=your_secret_key
```

### Installation
1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Initialize the database:
```bash
flask db upgrade
```
4. Start the application:
```bash
python main.py
```

## Usage Guide

### For Interviewees
1. Access the main interview page
2. Select your participant type (e.g., Chipset Vendor, Server Vendor)
3. Enter your company name
4. Engage with the AI interviewer
5. Provide detailed responses to questions

### For Research Firm Users
1. Access the dashboard (/dashboard)
2. View interview progress and market coverage
3. Analyze market trends through interactive visualizations
4. Generate market insights reports
5. Use the analyst chatbot for custom queries

## Architecture

### Backend
- Flask web framework
- SQLAlchemy ORM
- OpenAI GPT integration
- PostgreSQL database

### Frontend
- Bootstrap CSS framework
- Chart.js for visualizations
- Vanilla JavaScript
- Responsive design

### Key Components
1. Interview Engine (interview_ai.py)
   - Dynamic question generation
   - Response analysis
   - Data extraction

2. Correlation Engine (correlation_engine.py)
   - Market trend analysis
   - Data point correlation
   - Insight generation

3. Market Model (market_model.py)
   - Data aggregation
   - Statistical analysis
   - Trend visualization

4. Chatbot (chatbot.py)
   - Natural language processing
   - Context-aware responses
   - Data retrieval

## Data Model

### Interview Data
- Participant information
- Interview responses
- Extracted data points
- Market insights
- Temporal data

### Market Categories
- Product offerings
- Market trends
- Competitive landscape
- Technology advancements
- Future outlook

## Contributing

This project is part of a proprietary market research platform. For modifications or customizations, please contact the development team.

## License

Proprietary - All rights reserved

## Support

For technical support or questions about the platform's functionality, please contact the system administrator.
