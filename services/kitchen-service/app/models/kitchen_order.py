from app import db
from datetime import datetime


class KitchenOrder(db.Model):
    __tablename__ = 'kitchen_orders'

    id              = db.Column(db.Integer, primary_key=True)
    order_id        = db.Column(db.String(36), unique=True, nullable=False)
    kiosk_id        = db.Column(db.String(50), nullable=False)
    status          = db.Column(
        db.Enum('received', 'preparing', 'ready'),
        default='received',
        nullable=False
    )
    notes           = db.Column(db.Text, nullable=True)
    total           = db.Column(db.Numeric(10, 2), nullable=False)
    received_at     = db.Column(db.DateTime, default=datetime.utcnow)
    started_at      = db.Column(db.DateTime, nullable=True)
    completed_at    = db.Column(db.DateTime, nullable=True)

    items = db.relationship(
        'KitchenItem',
        backref='order',
        lazy=True,
        cascade='all, delete-orphan'
    )

    def to_dict(self):
        return {
            'id':           self.id,
            'order_id':     self.order_id,
            'kiosk_id':     self.kiosk_id,
            'status':       self.status,
            'notes':        self.notes,
            'total':        float(self.total),
            'received_at':  self.received_at.isoformat() if self.received_at else None,
            'started_at':   self.started_at.isoformat()  if self.started_at  else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'items':        [item.to_dict() for item in self.items],
        }


class KitchenItem(db.Model):
    __tablename__ = 'kitchen_items'

    id              = db.Column(db.Integer, primary_key=True)
    kitchen_order_id= db.Column(db.Integer, db.ForeignKey('kitchen_orders.id'), nullable=False)
    product_id      = db.Column(db.String(50), nullable=False)
    name            = db.Column(db.String(150), nullable=False)
    quantity        = db.Column(db.Integer, nullable=False)
    unit_price      = db.Column(db.Numeric(10, 2), nullable=False)
    is_ready        = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id':         self.id,
            'product_id': self.product_id,
            'name':       self.name,
            'quantity':   self.quantity,
            'unit_price': float(self.unit_price),
            'is_ready':   self.is_ready,
        }