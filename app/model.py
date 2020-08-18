from enum import Enum
from app import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), index=True, unique=True, nullable=False)
    username = db.Column(db.String(256), index=True, nullable=False)
    public = db.Column(db.Boolean(), default=False)
    last_access = db.Column(db.DateTime(), server_default=db.func.now())
    created = db.Column(db.DateTime(), server_default=db.func.now())
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
    meta = db.Column(db.JSON, default={})

    profile = db.relationship('Profile')
    calendars = db.relationship('Calendar', back_populates='user')
    subscriptions = db.relationship('User',
                                    secondary='subscriptions',
                                    primaryjoin='users.c.id==subscriptions.c.a_user_id',
                                    secondaryjoin='users.c.id==subscriptions.c.b_user_id')
    subscribers = db.relationship('User',
                                  secondary='subscriptions',
                                  primaryjoin='users.c.id==subscriptions.c.b_user_id',
                                  secondaryjoin='users.c.id==subscriptions.c.a_user_id')
    queued = db.relationship('QueuedUser', back_populates='user')

    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    show_name = db.Column(db.Boolean, default=False)
    level = db.Column(db.Integer, default=1)
    experience_points = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Profile {self.name}>'


class Calendar(db.Model):
    __tablename__ = 'calendars'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    public = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime(), server_default=db.func.now())
    meta = db.Column(db.JSON, default={})

    user = db.relationship('User', back_populates='calendars')
    events = db.relationship('Event', back_populates='calendar')

    def __repr__(self):
        return f'<Calendar {self.name}>'


class Event(db.Model):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendars.id'))
    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    start = db.Column(db.DateTime, index=True)
    end = db.Column(db.DateTime, index=True)
    duration = db.Column(db.Integer)
    rrule = db.Column(db.Text)
    rend = db.Column(db.Date, index=True)
    created = db.Column(db.DateTime(), server_default=db.func.now())
    meta = db.Column(db.JSON, default={})

    calendar = db.relationship('Calendar', back_populates='events')
    queues = db.relationship('Queue', back_populates='event')

    def __repr__(self):
        return f'<Event {self.name} starts {self.start}>'


class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    a_user_id = db.Column(db.Integer,
                          db.ForeignKey('users.id', onupdate='CASCADE'),
                          primary_key=True)
    b_user_id = db.Column(db.Integer,
                          db.ForeignKey('users.id', onupdate='CASCADE'),
                          primary_key=True)
    sortOrder = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime(), server_default=db.func.now())
    meta = db.Column(db.JSON, default={})

    def __repr__(self):
        return f'<Subscription {self.a_user_id} -> {self.b_user_id}>'


class QueueState(Enum):
    requested = 1
    accepted = 2
    queued = 3
    rejected = 4
    blocked = 5


class Queue(db.Model):
    __tablename__ = 'queues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    slot_count = db.Column(db.Integer, default=1, nullable=False)
    public = db.Column(db.Boolean, default=False)
    auto_accept = db.Column(db.Boolean, default=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    created = db.Column(db.DateTime(), server_default=db.func.now())
    meta = db.Column(db.JSON, default={})

    event = db.relationship('Event', back_populates='queues')
    users = db.relationship('QueuedUser', back_populates='queue')

    @property
    def queued_users(self):
        return sorted([qu for qu in self.users if qu.state == QueueState.queued],
                      key=lambda x: x.queue_date)


class QueuedUser(db.Model):
    __tablename__ = 'queued_users'

    id = db.Column(db.Integer, primary_key=True)
    queue_id = db.Column(db.Integer, db.ForeignKey('queues.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    queue_date = db.Column(db.DateTime(), server_default=db.func.now())
    created = db.Column(db.DateTime(), server_default=db.func.now())
    state = db.Column(db.Enum(QueueState),
                      default=QueueState.requested)
    meta = db.Column(db.JSON, default={})

    user = db.relationship('User', back_populates='queued')
    queue = db.relationship('Queue', back_populates='users')
