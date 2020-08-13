from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256), index=True, unique=True)
    name = db.Column(db.String(256))
    last_name = db.Column(db.String(256))
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))
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

    # subscriptions = db.relationship('Subscription',
    #                                 primaryjoin='Subscription.a_user_id==User.id')
    # subscribers = db.relationship('Subscription',
    #                               primaryjoin='Subscription.b_user_id==User.id')

    def __repr__(self):
        return f'<User {self.username}>'


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(256))
    description = db.Column(db.Text)
    skills = db.relationship('Skill')

    def __repr__(self):
        return f'<Profile {self.role}>'


class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    score = db.Column(db.Integer)
    profile_id = db.Column(db.Integer, db.ForeignKey('profiles.id'))

    def __repr__(self):
        return f'<Skill {self.name} with score {self.score}>'


class Calendar(db.Model):
    __tablename__ = 'calendars'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    public = db.Column(db.Boolean, default=False)

    user = db.relationship('User', back_populates='calendars')
    events = db.relationship('Event', back_populates='calendar')

    def __repr__(self):
        return f'<Calendar {self.name}>'


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256))
    description = db.Column(db.Text)
    start = db.Column(db.DateTime, index=True)
    end = db.Column(db.DateTime, index=True)
    calendar_id = db.Column(db.Integer, db.ForeignKey('calendars.id'))
    duration = db.Column(db.Integer)

    calendar = db.relationship('Calendar', back_populates='events')

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

    def __repr__(self):
        return f'<Subscription {self.a_user_id} -> {self.b_user_id}>'
