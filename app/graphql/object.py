import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from sqlalchemy import and_

from app.model import Profile as ProfileModel
from app.model import Skill as SkillModel
from app.model import User as UserModel
from app.model import Calendar as CalendarModel
from app.model import Event as EventModel


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

    skills = graphene.List(
        lambda: Skill, name=graphene.String(), score=graphene.Int())

    def resolve_skills(self, info, name=None, score=None):
        query = Skill.get_query(info=info)
        qyery = query.filter(SkillModel.profile_id == self.id)
        if name:
            query = query.filter(SkillModel.name == name)
        if score:
            query = query.filter(SkillModel.score == score)

        return query.all()


class Skill(SQLAlchemyObjectType):
    class Meta:
        model = SkillModel
        interfaces = (relay.Node,)


class SkillInput(graphene.InputObjectType):
    name = graphene.String()
    score = graphene.Int()


class Calendar(SQLAlchemyObjectType):
    class Meta:
        model = CalendarModel
        interfaces = (relay.Node,)

    events = graphene.List(
        lambda: Event, start=graphene.Date(), end=graphene.Date())

    def resolve_events(self, info, start, end):
        query = Event.get_query(info=info)
        query = query.filter(and_(EventModel.id == self.id,
                                  EventModel.start <= end,
                                  EventModel.end >= start))
        return query.all()


class Event(SQLAlchemyObjectType):
    class Meta:
        model = EventModel
        interfaces = (relay.Node,)


class EventInput(graphene.InputObjectType):
    start = graphene.Date()
    end = graphene.Date()
