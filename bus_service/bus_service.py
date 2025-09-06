import datetime
from datetime import date
import uuid
from decimal import Decimal
from enum import Enum, auto
from dataclasses import dataclass, field

from bus_service.interfaces import (
    IUser,
    ITrip,
    IAuthorized,
    ITripManager,
    IBusManager
)


class SortBy(Enum):
    DEPARTURE = auto()
    DEPARTURE_DATE = auto()
    ARRIVAL = auto()
    ARRIVAL_DATE = auto()
    AVAILABLE_SEATS = auto()
    RATING = auto()


class TicketStatus(Enum):
    AVAILABLE = auto()
    REQUESTED = auto()
    APPROVED = auto()
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

    def add_rating(self, user: "IUser", rating: float) -> None:
        print(f"User {user.id} has added rating with score {rating}")
        self.ratings.append(rating)

    def sell_seat(self, amount: int) -> bool:
        if amount < 1:
            print("Amount of seats can not be less than 1.")
            return False

        if self.total_seats < self.sold_seats + amount:
            print("Not enough available seats.")
            return False

        self.sold_seats += amount
        return True

    @property
    def average_rating(self) -> float:
        return sum(self.ratings) / len(self.ratings)

    def __str__(self):
        return f"Trip {self.departure} -> {self.arrival} [{self.departure_date}]"


@dataclass
class Ticket:
    ticket_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    trip: "Trip"
    seats_amount: int
    status: TicketStatus = field(default=TicketStatus.AVAILABLE, init=False)

    def __str__(self):
        return f"Ticket #{self.ticket_id} ({self.status})"


class UnauthorizedUser(IUser):

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

        self.id = str(uuid.uuid4())

    def get_trips(self, trips: list["Trip"], sort_by: SortBy | None = None) -> None:

        def list_trips(trips_list: list):
            for trip in trips_list:
                print(trip)

        if sort_by is None:
            list_trips(trips)

        match sort_by:
            case SortBy.DEPARTURE:
                list_trips(sorted(trips, key=lambda t: t.departure))
            case SortBy.DEPARTURE_DATE:
                list_trips(sorted(trips, key=lambda t: t.departure_date))
            case SortBy.ARRIVAL:
                list_trips(sorted(trips, key=lambda t: t.arrival))
            case SortBy.ARRIVAL_DATE:
                list_trips(sorted(trips, key=lambda t: t.arrival_date))
            case SortBy.AVAILABLE_SEATS:
                list_trips(sorted(trips, key=lambda t: t.available_seats))
            case SortBy.RATING:
                list_trips(sorted(trips, key=lambda t: t.average_rating, reverse=True))

    def __str__(self):
        return f"Unauthorized user ({self.email})"


class AuthorizedUser(UnauthorizedUser, IAuthorized):

    def request_ticket(self, ticket: "Ticket") -> None:
        print(f"{self} requests {ticket}")
        ticket.status = TicketStatus.REQUESTED

    def __str__(self):
        return f"Authorized user ({self.email})"


class TripManager(AuthorizedUser, ITripManager):

    def create_trip(self, price: Decimal, departure: str, departure_date: date, arrival: str, arrival_date: date,
                    total_seats: int) -> "Trip":
        print(f"Creating trip...")
        return Trip(
            price=price,
            departure=departure,
            departure_date=departure_date,
            arrival=arrival,
            arrival_date=arrival_date,
            total_seats=total_seats
        )

    def update_trip(self, trip: "Trip", new_trip_data: dict) -> None:
        print(f"Updating {trip}")

        for key, value in new_trip_data.items():
            if hasattr(trip, key):
                setattr(trip, key, value)

    def delete_trip(self, trip: "Trip") -> None:
        print(f"Deleting {trip}")
        del trip

    def approve_ticket_request(self, ticket: "Ticket") -> None:
        print(f"Approving request for {ticket}")

        ticket.status = TicketStatus.APPROVED

    def __str__(self):
        return f"Trip Manager ({self.email})"


class BusManager(AuthorizedUser, IBusManager):

    def sell_ticket(self, ticket: "Ticket") -> bool:
        if ticket.trip.sell_seat(ticket.seats_amount):
            ticket.status = TicketStatus.SOLD
            return True

        return False

    def refund_ticket(self, ticket: "Ticket") -> bool:
        if ticket.trip.departure_date > date.today():
            print(f"Refund approved for {ticket}")
            ticket.status = TicketStatus.AVAILABLE
            return True

        print("You can not refund ticket from not actual trip.")
        return False

    def __str__(self):
        return f"Bus Manager ({self.email})"


class Superuser(BusManager, TripManager):

    def __str__(self):
        return f"Superuser ({self.email})"
