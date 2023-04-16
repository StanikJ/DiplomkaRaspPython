from helpers.database import db
from datetime import datetime, timedelta

class DrawersModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    MACaddr = db.Column(db.String(80), unique=True, nullable=False)
    drawer1 = db.Column(db.Integer, nullable=False)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, MACaddr, drawer1, drawer2):
        self.MACaddr = MACaddr
        self.drawer1 = drawer1
        self.drawer2 = drawer2

    def update_timestamp(self):
        self.updatedAt = datetime.utcnow()

    def is_record_old(self):
        now = datetime.utcnow()
        now_extract_minute = now - timedelta(minutes=1)
        return now_extract_minute > self.updatedAt

    @staticmethod
    def function_to_check_if_clients_work(self):
        drawers_model_list = DrawersModel.query().all()
        for drawer_model in drawers_model_list:
            if drawer_model.is_record_old():
                db.session.delete(drawer_model)
        db.session.commit()
