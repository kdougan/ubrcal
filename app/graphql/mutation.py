from datetime import datetime
from datetime import timedelta
from dateutil.rrule import rrule
from dateutil.rrule import rrulestr


import graphene
from app import db
from app.graphql.object import Calendar
from app.graphql.object import Event
from app.graphql.object import Profile
from app.graphql.object import User
from app.graphql.object import Queue
from app.graphql.object import QueuedUser
from app.model import Calendar as CalendarModel
from app.model import Event as EventModel
from app.model import Profile as ProfileModel
from app.model import Subscription as SubscriptionModel
from app.model import User as UserModel
from app.model import Queue as QueueModel
from app.model import QueuedUser as QueuedUserModel
from app.model import QueueState
from flask_graphql_auth import create_access_token
from flask_graphql_auth import create_refresh_token
from flask_graphql_auth import get_jwt_identity
from flask_graphql_auth import mutation_jwt_refresh_token_required
from graphql import GraphQLError
from graphql_relay.node.node import from_global_id

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

    def mutate(self, info, email, username, name=None):
        user = UserModel(username=username, email=email)
        profile = ProfileModel(name=name)
        db.session.add(user)
        db.session.add(profile)
        user.profile = profile
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
        id = graphene.Int()

    profile = graphene.Field(lambda: Profile)

    def mutate(self, info, role, description, user_id):
        user = UserModel.query.get(user_id)

        profile = ProfileModel(role=role, description=description)

        db.session.add(profile)
        user.profile = profile
        db.session.commit()
        return CreateProfile(profile=profile)


# ==================================================
# Calendars

class CreateCalendar(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        user_id = graphene.ID(required=True)

    calendar = graphene.Field(lambda: Calendar)

    def mutate(self, info, name, user_id):
        user_id = from_global_id(user_id)
        user = UserModel.query.get(user_id[1])

        calendar = CalendarModel(name=name, user_id=user.id)
        db.session.add(calendar)
        db.session.commit()
        return CreateCalendar(calendar=calendar)

# ==================================================
# Events


class CreateEvent(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        calendar_id = graphene.ID(required=True)
        start = graphene.DateTime(required=True)
        end = graphene.DateTime()
        duration = graphene.Int()
        rrule = graphene.String()
        description = graphene.String()

    event = graphene.Field(lambda: Event)

    def mutate(self, info, name, calendar_id, start, end=None, duration=None, description=None, rrule=None):
        calendar_id = from_global_id(calendar_id)
        calendar = CalendarModel.query.get(calendar_id[1])
        if not end and (not duration or duration > 0):
            raise GraphQLError(
                'You must specify either an end date or duration in minutes!')
        if end:
            duration = (end - start).seconds // 60 % 60
        elif duration:
            end = start + timedelta(minutes=duration)
        if rrule:
            rrule_obj = rrulestr(rrule)
        event = EventModel(name=name,
                           calendar_id=calendar.id,
                           description=description,
                           start=start,
                           end=end,
                           duration=duration,
                           rrule=rrule)
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
        rrule = graphene.String()

    event = graphene.Field(lambda: Event)

    def mutate(self, info, id, **kwargs):
        event_id = from_global_id(id)
        event = EventModel.query.get(event_id[1])
        changed = False
        for k, v in kwargs.items():
            if getattr(event, k) != v:
                setattr(event, k, v)
                changed = True
        if changed:
            event.duration = (event.end - event.start).seconds // 60
            db.session.commit()
        return MutateEvent(event=event)


# ==================================================
# Queues

class CreateQueue(graphene.Mutation):
    class Arguments:
        event_id = graphene.ID(required=True)
        name = graphene.String()
        slot_count = graphene.Int()
        public = graphene.Boolean()
        auto_approve = graphene.Boolean()

    queue = graphene.Field(lambda: Queue)

    def mutate(self, info, event_id, name=None, slot_count=1, public=False, auto_approve=False):
        event_id = from_global_id(event_id)
        event = EventModel.query.get(event_id[1])
        queue = QueueModel(event_id=event.id,
                           name=name,
                           slot_count=slot_count,
                           public=public,
                           auto_approve=auto_approve)
        db.session.add(queue)
        db.session.commit()
        return queue


class AddUserToQueue(graphene.Mutation):
    class Arguments:
        queue_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)

    queued_user = graphene.Field(lambda: QueuedUser)

    def mutate(self, info, user_id, queue_id):
        user_id = from_global_id(user_id)
        queue_id = from_global_id(queue_id)
        queued_user = QueuedUserModel.query.filter(
            QueuedUserModel.user_id == user_id[1],
            QueuedUserModel.queue_id == queue_id[1]
        ).first()
        queue = QueueModel.query.get(queue_id[1])
        if queued_user:
            if queued_user.state in [QueueState.requested,
                                     QueueState.accepted]:
                raise GraphQLError(f'You are already queued!')
            elif queued_user.state == QueueState.blocked:
                raise GraphQLError(f'You are blocked!')
            else:
                queued_user.state = QueueState.requested
                queued_user.queue_date = datetime.now()
        else:
            queued_user = QueuedUserModel(queue_id=queue.id,
                                          user_id=user_id[1])
            db.session.add(queued_user)
        if queue.auto_accept and (not queued_user.state or queued_user.state == QueueState.requested):
            queued_user.state = QueueState.accepted
        if queued_user.state == QueueState.accepted and len(queue.queued_users) < queue.slot_count:
            queued_user.state = QueueState.queued
        db.session.commit()
        return AddUserToQueue(queued_user=queued_user)


class RemoveUserFromQueue(graphene.Mutation):
    class Arguments:
        queue_id = graphene.ID(required=True)
        user_id = graphene.ID(required=True)

    queued_user = graphene.Field(lambda: QueuedUser)

    def mutate(self, info, user_id, queue_id):
        user_id = from_global_id(user_id)
        queue_id = from_global_id(queue_id)
        queued_user = QueuedUserModel.query.filter(
            QueuedUserModel.user_id == user_id[1],
            QueuedUserModel.queue_id == queue_id[1]
        ).first()

        if not queued_user or queued_user.state in [QueueState.removed,
                                                    QueueState.blocked]:
            raise GraphQLError(f'You are not already queued!')
        elif queued_user:
            queued_user.state = QueueState.removed
        db.session.commit()
        return RemoveUserFromQueue(queued_user=queued_user)


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

    create_queue = CreateQueue.Field()
    add_user_to_queue = AddUserToQueue.Field()
    remove_user_from_queue = RemoveUserFromQueue.Field()
