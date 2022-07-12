# @ TODO Check this
# import datetime
#
# import factory
# from enums.histories import OrderHistoryTypeEnum
# from enums.orders import OrderContractType
# from enums.orders import OrderStatusEnum
# from factory import fuzzy
# from models import Order
# from models import OrderHistoryRecord
# from tests.common import TestGlobalSession
#
#
# class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
#     id = factory.Faker("uuid4")  # noqa: A003
#     created_at = factory.LazyFunction(lambda: datetime.datetime.now(tz=datetime.timezone.utc))
#     updated_at = factory.LazyFunction(lambda: datetime.datetime.now(tz=datetime.timezone.utc))
#
#
# class OrderFactory(BaseFactory):
#     sequence_id = factory.Sequence(lambda n: n)
#     vehicle_id = factory.Sequence(lambda n: n)
#     vehicle_brand = factory.Faker("word")
#     vehicle_model = factory.Faker("word")
#     contract_type = fuzzy.FuzzyChoice([i.value for i in OrderContractType])
#     contract_number = factory.Faker("word")
#     planned_issue_date = fuzzy.FuzzyDate(start_date=datetime.date.today())
#     status = OrderStatusEnum.NEW
#     contract_id = factory.Faker("uuid4")
#     client_id = factory.Faker("uuid4")
#     is_urgent = False
#     is_manual = False
#
#     class Meta:
#         model = Order
#         sqlalchemy_session = TestGlobalSession
#         sqlalchemy_session_persistence = "commit"
#
#
# class HistoryFactory(BaseFactory):
#     history_type = OrderHistoryTypeEnum.STATUS_CHANGED
#     order = factory.SubFactory(OrderFactory)
#     data = {"status": OrderStatusEnum.NEW}
#
#     class Meta:
#         model = OrderHistoryRecord
#         sqlalchemy_session = TestGlobalSession
#         sqlalchemy_session_persistence = "commit"
