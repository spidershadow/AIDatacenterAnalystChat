from app import db
from datetime import datetime

class Interview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    participant_type = db.Column(db.String(64), nullable=False)
    company_name = db.Column(db.String(128), nullable=False)
    interview_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    data = db.Column(db.JSON, nullable=False)
    completed = db.Column(db.Boolean, default=False)
