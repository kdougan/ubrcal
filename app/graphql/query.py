import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyConnectionField
from graphql_relay.node.node import from_global_id
from sqlalchemy import and_
from sqlalchemy import or_

from app.graphql.object import Profile
from app.graphql.object import User
from app.graphql.object import Calendar
from app.graphql.object import Event
from app.model import User as UserModel
from app.model import Event as EventModel


class Query(graphene.ObjectType):
    node = relay.Node.Field()

    user = graphene.Field(lambda: User,
                          id=graphene.ID())
    users = graphene.List(lambda: User,
                          username=graphene.String())
    events = graphene.List(lambda: Event,
                           start=graphene.Date(),
                           end=graphene.Date())
    event = graphene.Field(lambda: Event,
                           id=graphene.ID())
    all_events = graphene.List(lambda: Event)
    profiles = SQLAlchemyConnectionField(Profile)
    calendars = SQLAlchemyConnectionField(Calendar)

    def resolve_user(self, info, id):
        user_id = from_global_id(id)[1]
        return UserModel.query.get(user_id)

    def resolve_users(self, info, username=None):
        query = User.get_query(info)
        if username:
            query = query.filter(UserModel.username == username)
        return query.all()

    def resolve_events(self, info, start, end):
        query = Event.get_query(info)
        query = query.filter(
            or_(
                and_(EventModel.start <= end, EventModel.end >= start),
                and_(EventModel.start <= end,
                     or_(EventModel.rend == None, EventModel.start <= EventModel.rend))
            )
        )
        return query.all()

    def resolve_event(self, info, id):
        event_id = from_global_id(id)[1]
        return EventModel.query.get(event_id)

    def resolve_all_events(self, info):
        query = Event.get_query(info)
        return query.all()
