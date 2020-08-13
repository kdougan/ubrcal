import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id

from app.graphql.object import Profile
from app.graphql.object import Skill
from app.graphql.object import User
from app.graphql.object import Calendar
from app.graphql.object import Event
from app.model import User as UserModel
from app.model import Event as EventModel


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    user = graphene.Field(lambda: User, id=graphene.ID())

    def resolve_user(self, info, id):
        user_id = from_global_id(id)[1]
        return UserModel.query.get(user_id)

    users = graphene.List(
        lambda: User, username=graphene.String())

    def resolve_users(self, info, username=None):
        query = User.get_query(info)
        if username:
            query = query.filter(UserModel.username == username)
        return query.all()

    events = graphene.List(
        lambda: Event, start=graphene.Date(), end=graphene.Date())

    def resolve_events(self, info, start, end):
        query = Event.get_query(info)
        query = query.filter(EventModel.start <= end, EventModel.end >= start)
        return query.all()

    event = graphene.Field(lambda: Event, id=graphene.ID())

    def resolve_event(self, info, id):
        event_id = from_global_id(id)[1]
        return EventModel.query.get(event_id)

    profiles = SQLAlchemyConnectionField(Profile)
    skills = SQLAlchemyConnectionField(Skill)
    calendars = SQLAlchemyConnectionField(Calendar)

    # event = SQLAlchemyConnectionField(Event)
