import graphene
from dateutil.rrule import rrulestr
from datetime import datetime
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import and_
from sqlalchemy import or_

from app.model import Profile as ProfileModel
from app.model import User as UserModel
from app.model import Calendar as CalendarModel
from app.model import Event as EventModel
from app.model import Queue as QueueModel
from app.model import QueuedUser as QueuedUserModel


class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel
        interfaces = (relay.Node,)

    calendars = graphene.List(lambda: Calendar)
    subscriptions = graphene.List(lambda: User)
    subscribers = graphene.List(lambda: User)

    def resolve_calendars(self, info):
        if len(info.path) > 2 and info.path[-3] == 'subscriptions':
            return [c for c in self.calendars if c.public]
        return self.calendars

    def resolve_subscriptions(self, info):
        return self.subscriptions

    def resolve_subscribers(self, info):
        return self.subscribers


class Profile(SQLAlchemyObjectType):
    class Meta:
        model = ProfileModel
        interfaces = (relay.Node,)


class Calendar(SQLAlchemyObjectType):
    class Meta:
        model = CalendarModel
        interfaces = (relay.Node,)

    events = graphene.List(
        lambda: Event, start=graphene.Date(), end=graphene.Date())

    def resolve_events(self, info, start, end):
        query = Event.get_query(info=info)
        query.filter(
            and_(
                EventModel.id == self.id,
                or_(
                    and_(EventModel.start <= end, EventModel.end >= start),
                    and_(EventModel.start <= end,
                         or_(EventModel.rend == None, EventModel.start <= EventModel.rend))
                )
            )
        )
        return query.all()


class Event(SQLAlchemyObjectType):
    class Meta:
        model = EventModel
        interfaces = (relay.Node,)

    queues = graphene.List(lambda: Queue)

    def resolve_queues(self, info):
        return self.queues


class EventInput(graphene.InputObjectType):
    start = graphene.Date()
    end = graphene.Date()


class Queue(SQLAlchemyObjectType):
    class Meta:
        model = QueueModel
        interfaces = (relay.Node,)

    users = graphene.List(lambda: QueuedUser)

    def resolve_users(self, info):
        return self.users


class QueuedUser(SQLAlchemyObjectType):
    class Meta:
        model = QueuedUserModel
        interfaces = (relay.Node,)
