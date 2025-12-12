from datetime import datetime, timezone

from ocpp.routing import on
from ocpp.v201 import ChargePoint as cp
from ocpp.v201 import call_result
from ocpp.v201.datatypes import (
    ChargingStationType,
    EventDataType,
    IdTokenInfoType,
    IdTokenType,
    MessageContentType,
    MeterValueType,
    ReportDataType,
    TransactionType,
)
from ocpp.v201.enums import (
    Action,
    AuthorizationStatusEnumType,
    BootReasonEnumType,
    ConnectorStatusEnumType,
    MessageFormatEnumType,
    RegistrationStatusEnumType,
    TransactionEventEnumType,
    TriggerReasonEnumType,
)


class ChargePoint(cp):
    @on(Action.authorize)
    def on_authorize(self, id_token: dict, **kwargs):
        id_token: IdTokenType = IdTokenType(**id_token)
        print(f"Authorization request for id_token: {id_token}")
        return call_result.Authorize(
            id_token_info=IdTokenInfoType(
                status=AuthorizationStatusEnumType.accepted,
                personal_message=MessageContentType(
                    format=MessageFormatEnumType.utf8, content="Welcome @ ML2Grow!"
                ),
            )
        )

    @on(Action.boot_notification)
    def on_boot_notification(self, reason: BootReasonEnumType, charging_station: dict):
        charging_station: ChargingStationType = ChargingStationType(**charging_station)
        print(f"Got a BootNotification from {charging_station}! Reason: {reason}")
        return call_result.BootNotification(
            current_time=datetime.now(timezone.utc).isoformat(),
            interval=10,
            status=RegistrationStatusEnumType.accepted,
        )

    @on(Action.heartbeat)
    def on_heartbeat(self):
        print("Heartbeat received")
        return call_result.Heartbeat(
            current_time=datetime.now(timezone.utc).isoformat()
        )

    @on(Action.meter_values)
    def on_meter_values(self, evse_id: int, meter_value: dict):
        meter_value: MeterValueType = MeterValueType(**meter_value)
        print(f"Meter Values from connector {evse_id}: {meter_value}")
        return call_result.MeterValues()

    @on(Action.notify_customer_information)
    def on_notify_customer_information(
        self, data: str, generated_at: str, request_id: int, **kwargs
    ):
        generated_at: datetime = datetime.fromisoformat(generated_at)
        print(
            f"Customer Information Notification received at {generated_at} with request ID {request_id}: {data}"
        )
        return call_result.NotifyCustomerInformation()

    @on(Action.notify_event)
    def on_notify_event(self, generated_at: str, event_data: dict, **kwargs):
        generated_at: datetime = datetime.fromisoformat(generated_at)
        event_data: EventDataType = EventDataType(**event_data)
        print(
            f"Event Notification received at {generated_at} with event data: {event_data}"
        )
        return call_result.NotifyEvent()

    @on(Action.notify_report)
    def on_notify_report(self, generated_at: str, report_data: dict, **kwargs):
        generated_at: datetime = datetime.fromisoformat(generated_at)
        report_data: ReportDataType = ReportDataType(**report_data)
        print(
            f"Report Notification received at {generated_at} with report data: {report_data}"
        )
        return call_result.NotifyReport()

    @on(Action.status_notification)
    def on_status_notification(
        self,
        timestamp: str,
        connector_status: ConnectorStatusEnumType,
        evse_id: int,
        connector_id: int,
    ):
        timestamp: datetime = datetime.fromisoformat(timestamp)
        connector_status: ConnectorStatusEnumType = ConnectorStatusEnumType(
            connector_status
        )
        print(
            f"Status Notification: Connector status is {timestamp} - {connector_status} - EVSE {evse_id} - Connector {connector_id}"
        )
        return call_result.StatusNotification()

    @on(Action.transaction_event)
    def on_transaction_event(
        self,
        event_type: str,
        timestamp: str,
        trigger_reason: str,
        transaction_info: dict,
        meter_values: dict | None = None,
        **kwargs,
    ):
        event_type: TransactionEventEnumType = TransactionEventEnumType(event_type)
        timestamp: datetime = datetime.fromisoformat(timestamp)
        trigger_reason: TriggerReasonEnumType = TriggerReasonEnumType(trigger_reason)
        transaction_info: TransactionType = TransactionType(**transaction_info)
        meter_values: MeterValueType | None = (
            MeterValueType(**meter_values) if meter_values else None
        )
        print(
            f"Transaction Event {event_type}: {timestamp} - {trigger_reason} - Transaction Info: {transaction_info}"
        )
        return call_result.TransactionEvent()
