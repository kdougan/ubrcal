from datetime import timedelta
import graphene
from graphql import GraphQLError
from graphql_relay.node.node import from_global_id
from flask_graphql_auth import create_access_token
from flask_graphql_auth import create_refresh_token
from flask_graphql_auth import mutation_jwt_refresh_token_required
from flask_graphql_auth import get_jwt_identity

from app import db
from app.graphql.object import Profile
from app.graphql.object import SkillInput
from app.graphql.object import User
from app.graphql.object import Calendar
from app.graphql.object import Event
from app.model import Profile as ProfileModel
from app.model import Skill as SkillModel
from app.model import User as UserModel
from app.model import Calendar as CalendarModel
from app.model import Event as EventModel
from app.model import Subscription as SubscriptionModel


# ==================================================
# Authentication

class AuthMutation(graphene.Mutation):
    class Arguments:
        email = graphene.String()
        password = graphene.String()

    access_token = graphene.String()
    refresh_token = graphene.String()

    def mutate(self, info, email, password):
        return AuthMutation(
            access_token=create_access_token(email),
            refresh_token=create_refresh_token(email)
        )


class RefreshMutation(graphene.Mutation):
    class Arguments:
        token = graphene.String()

    new_token = graphene.String()

    @mutation_jwt_refresh_token_required
    def mutate(self, info):
        current_user = get_jwt_identity()
        return RefreshMutation(
            new_token=create_access_token(
                identity=current_user))


# ==================================================
# Users


class CreateUser(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        username = graphene.String(required=True)
        name = graphene.String()

    user = graphene.Field(lambda: User)

    def mutate(self, info, email, username, name):
        user = UserModel(username=username, name=name, email=email)

        db.session.add(user)
        db.session.commit()

        return CreateUser(user=user)


class CreateSubscription(graphene.Mutation):
    class Arguments:
        from_user = graphene.ID(required=True)
        to_user = graphene.ID(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, from_user, to_user):
        if from_user == to_user:
            raise GraphQLError('You may not subscribe to yourself!')
        from_user_id = from_global_id(from_user)
        to_user_id = from_global_id(to_user)
        from_user = UserModel.query.get(from_user_id[1])
        to_user = UserModel.query.get(to_user_id[1])
        if to_user in from_user.subscriptions:
            raise GraphQLError(
                f'You are already subscribed to {to_user.username}!')
        from_user.subscriptions.append(to_user)
        db.session.commit()
        db.session.refresh(from_user)
        return CreateSubscription(user=from_user)


class DestroySubscription(graphene.Mutation):
    class Arguments:
        from_user = graphene.ID(required=True)
        to_user = graphene.ID(required=True)

    user = graphene.Field(lambda: User)

    def mutate(self, info, from_user, to_user):
        if from_user == to_user:
            raise GraphQLError('You may not unsubscribe from yourself!')
        from_user_id = from_global_id(from_user)
        to_user_id = from_global_id(to_user)
        from_user = UserModel.query.get(from_user_id[1])
        to_user = UserModel.query.get(to_user_id[1])
        if to_user not in from_user.subscriptions:
            raise GraphQLError(
                f'You are not already subscribed to {to_user.username}!')
        from_user.subscriptions.remove(to_user)
        db.session.commit()
        db.session.refresh(from_user)
        return CreateSubscription(user=from_user)


class CreateProfile(graphene.Mutation):
    class Arguments:
        role = graphene.String(required=True)
        description = graphene.String(required=True)
        user_id = graphene.Int(required=True)
        skills = graphene.List(SkillInput)
        id = graphene.Int()

    profile = graphene.Field(lambda: Profile)

    def mutate(self, info, role, description, user_id, skills):
        user = UserModel.query.get(user_id)

        profile = ProfileModel(role=role, description=description)
        # Create skills
        skill_list = [SkillModel(
            name=input_skill.name, score=input_skill.score) for input_skill in skills]
        profile.skills.extend(skill_list)

        db.session.add(profile)
        # Update user
        user.profile = profile
        db.session.commit()

        return CreateProfile(profile=profile)


# ==================================================
# Calendars

class CreateCalendar(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        user_id = graphene.Int(required=True)

    calendar = graphene.Field(lambda: Calendar)

    def mutate(self, info, name, user_id):
        user = UserModel.query.get(user_id)

        calendar = CalendarModel(name=name, user_id=user_id)
        db.session.add(calendar)
        db.session.commit()
        return CreateCalendar(calendar=calendar)

# ==================================================
# Events


class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        calendar_id = graphene.Int(required=True)
        start = graphene.DateTime(required=True)
        end = graphene.DateTime(required=True)
        description = graphene.String()

    event = graphene.Field(lambda: Event)

    def mutate(self, info, name, calendar_id, start, end, description=None):
        calendar = CalendarModel.query.get(calendar_id)
        duration = (end - start).seconds // 60 % 60
        event = EventModel(name=name,
                           calendar_id=calendar_id,
                           description=description,
                           start=start,
                           end=end,
                           duration=duration)
        db.session.add(event)
        db.session.commit()
        return CreateEvent(event=event)


class MutateEvent(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        name = graphene.String()
        calendar_id = graphene.Int()
        start = graphene.DateTime()
        end = graphene.DateTime()
        description = graphene.String()

    event = graphene.Field(lambda: Event)

    def mutate(self, info, id, **kwargs):
        event_id = from_global_id(id)
        event = EventModel.query.get(event_id[1])
        changed = False
        for k, v in kwargs.items():
            if hasattr(event, k) and getattr(event, k) != v:
                setattr(event, k, v)
                changed = True
        if changed:
            event.duration = (event.end - event.start).seconds // 60
            db.session.commit()
        return MutateEvent(event=event)


class Mutation(graphene.ObjectType):
    auth = AuthMutation.Field()
    refresh = RefreshMutation.Field()

    create_user = CreateUser.Field()
    createSubscription = CreateSubscription.Field()
    destroySubscription = DestroySubscription.Field()

    create_profile = CreateProfile.Field()
    create_calendar = CreateCalendar.Field()

    create_event = CreateEvent.Field()
    mutate_event = MutateEvent.Field()
