from tortoise import fields
import uuid


class UUIDModelMixin:
	uuid = fields.UUIDField(pk=True, default=uuid.uuid4)


class SoftDeleteModelMixin:
	is_deleted = fields.DatetimeField(null=True)


class AuditMixin:
	created_at = fields.DatetimeField(auto_now_add=True)
	updated_at = fields.DatetimeField(null=True, auto_now=True)


class TrackingMixin:
	ip_address = fields.CharField(max_length=20, null=True)
	user_agent = fields.CharField(max_length=255, null=True)


class ExpireMixin:
	start_at = fields.DatetimeField(null=False)
	end_at = fields.DatetimeField(null=False)
