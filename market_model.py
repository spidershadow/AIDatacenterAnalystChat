from app import db
from models import Interview
import json
from collections import defaultdict
from datetime import datetime
from flask import current_app

class MarketModel:
    def __init__(self):
        self.model = defaultdict(lambda: defaultdict(list))
        self.last_updated = None

    def update_model(self):
        with current_app.app_context():
            interviews = Interview.query.all()
            for interview in interviews:
                self._process_interview(interview)
        self.last_updated = datetime.utcnow()

    def _process_interview(self, interview):
        data = json.loads(interview.data)
        for category, items in data.items():
            if isinstance(items, list):
                for item in items:
                    self.model[category][interview.participant_type].append({
                        'value': item,
                        'company': interview.company_name,
                        'date': interview.interview_date
                    })

    def add_data_point(self, category, participant_type, value, company, date):
        self.model[category][participant_type].append({
            'value': value,
            'company': company,
            'date': date
        })
        self.last_updated = datetime.utcnow()

    def get_model_summary(self):
        summary = {}
        for category, participants in self.model.items():
            summary[category] = {
                participant: len(data) for participant, data in participants.items()
            }
        return summary

    def get_category_data(self, category):
        return dict(self.model[category])

market_model = MarketModel()

def update_market_model():
    market_model.update_model()

def add_interview_to_model(interview):
    market_model._process_interview(interview)

def get_market_model_summary():
    return market_model.get_model_summary()

def get_category_data(category):
    return market_model.get_category_data(category)
