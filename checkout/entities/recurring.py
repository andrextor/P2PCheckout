from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Recurring(BaseModel):
    periodicity: str = Field(
        ...,
        description="Frequency of the transaction (Y = annual, M = monthly, D = daily)",
    )
    interval: int = Field(..., description="Interval between payments")
    next_payment: str = Field(default="", description="Next payment date", alias="nextPayment")
    max_periods: Optional[int] = Field(
        default=-1, description="Maximum times the recurrence will happen, -1 if unlimited", alias="maxPeriods"
    )
    due_date: str = Field(default="", description="Due date for the recurring charge", alias="dueDate")
    notification_url: str = Field(default="", description="URL for sending notifications", alias="notificationUrl")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    def to_dict(self) -> dict:
        """
        Convert the Recurring object to a dictionary using the Pydantic `model_dump` method.
        """
        return {
            "periodicity": self.periodicity,
            "interval": self.interval,
            "nextPayment": self.next_payment,
            "maxPeriods": self.max_periods,
            "dueDate": self.due_date,
            "notificationUrl": self.notification_url,
        }
