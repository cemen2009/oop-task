from datetime import date
import uuid
from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum, auto
from dataclasses import dataclass, field

from bus_service.interfaces import ITrip
from interfaces import IUser


class SortBy(Enum):
    DESTINATION = auto()
    AVAILABLE_SEATS = auto()
    DEPARTURE_DATE = auto()
    ARRIVAL_DATE = auto()
    RATING = auto()


class TicketStatus(Enum):
    AVAILABLE = auto()
    REQUESTED = auto()
    SOLD = auto()


class Trip(ITrip):

    def __init__(
            self,
            price: Decimal,
            departure: str,
            departure_date: date,
            arrival: str,
            arrival_date: date,
            total_seats: int
    ):
        self.price = price
        self.departure = departure
        self.departure_date = departure_date
        self.arrival = arrival
        self.arrival_date = arrival_date
        self.total_seats = total_seats

        self.id = str(uuid.uuid4())
        self.sold_seats = 0
        self.ratings = []

    @property
    def available_seats(self) -> int:
        return self.total_seats - self.sold_seats

    def add_rating(self, user: "User", rating: float) -> None:
        print(f"User {user.id} has added rating with score {rating}")
        self.ratings.append(rating)

    @property
    def average_rating(self) -> float:
        return sum(self.ratings) / len(self.ratings)


@dataclass
class Ticket:
    ticket_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    trip: "Trip"
    status: TicketStatus


class UnauthorizedUser(IUser):

    def get_trips(self, trips: list["Trip"], sort_by: SortBy | None = None) -> list["Trip"]:
        # TODO: implement sorting
        ...
