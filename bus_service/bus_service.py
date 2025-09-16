from datetime import date, datetime, timezone
import uuid
from decimal import Decimal
from enum import Enum, auto
from dataclasses import dataclass, field

from bus_service.interfaces import (
    AbstractUser,
    AbstractTrip,
    IAuthorizedUser,
    ITripManager,
    IBusManager
)
# TODO: keep methods in interfaces of users
# update trip interface: implement all necessary methods
# implement trip methods into users methods


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


@dataclass
class Ticket:
    id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    trip: "Trip"
    seats_amount: int = 1
    status: TicketStatus = field(default=TicketStatus.AVAILABLE, init=False)
    price: Decimal = Decimal("0")
    requester: IAuthorizedUser | None = None
    owner: IBusManager | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def __str__(self):
        return f"Ticket #{self.id} ({self.status})"


class Trip(AbstractTrip):

    def create_ticket(
            self,
            requester: IAuthorizedUser | None = None,
            owner: IBusManager | None = None,
            price: Decimal = Decimal("0"),
            status: TicketStatus | None = None,
            seats_amount: int | None = None,
    ) -> "Ticket":
        if price < 0:
            raise ValueError("Price cannot be negative")
        if seats_amount < 1:
            raise ValueError("Seats amount must be greater than 0")
        if self.available_seats < seats_amount:
            raise ValueError("Not enough available seats on that trip")

        ticket = Ticket(
            trip=self,
            seats_amount=seats_amount,
            price=price,
            requester=requester,
            owner=owner,
        )
        self._tickets.append(ticket)
        return ticket

    def request_ticket(self, ticket: "Ticket") -> None:
        if ticket.trip is not self:
            raise ValueError(f"{ticket} doesn't belong to {self}")
        if ticket.status is not TicketStatus.AVAILABLE:
            raise ValueError(f"Ticket is not available")

        ticket.status = TicketStatus.REQUESTED

    def approve_ticket(self, ticket: "Ticket") -> None:
        print(f"Approving ticket #{ticket.id}")
        ticket.status = TicketStatus.APPROVED

    def sell_ticket(self, ticket: "Ticket") -> None:
        if ticket not in self._tickets:
            raise ValueError(f"This ticket doesn't belong to {self}")

        print(f"Ticket #{ticket.id} was sold")
        ticket.status = TicketStatus.SOLD

    def refund_ticket(self, ticket: "Ticket") -> None:
        if self.departure_date < date.today():
            raise ValueError(f"You can not refund ticket on trip that has already taken place")

        print(f"Refunding ticket #{ticket.id}")
        ticket.status = TicketStatus.SOLD


class UnauthorizedUser(AbstractUser):
    def get_trips(self, trips: list["Trip"], sort_by: SortBy) -> list["Trip"]:
        def list_trips(trips_list: list):
            for trip in trips_list:
                print(trip)

        if sort_by is None:
            list_trips(trips)

        mapping = {
            SortBy.DEPARTURE: lambda t: t.departute,
            SortBy.DEPARTURE_DATE: lambda t: t.departure_date,
            SortBy.ARRIVAL: lambda t: t.arrival,
            SortBy.ARRIVAL_DATE: lambda t: t.arrival_date,
            SortBy.AVAILABLE_SEATS: lambda t: t.available_seats,
            SortBy.RATING: lambda t: t.average_rating,
        }

        list_trips(sorted(trips, key=mapping[sort_by], reverse=(sort_by == SortBy.RATING)))


class AuthorizedUser(UnauthorizedUser, IAuthorizedUser):

    def __init__(self, name: str, email: str):
        super().__init__(name, email)
        self._tickets: list["Ticket"] = []

    def request_ticket(self, ticket: "Ticket") -> None:
        ticket.trip.request_ticket(ticket)
        self._tickets.append(ticket)


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
        print(f"Updating {trip}...")

        for key, value in new_trip_data.items():
            if hasattr(trip, key):
                setattr(trip, key, value)

    def delete_trip(self, trip: "Trip") -> None:
        print(f"Deleting {trip}")
        del trip

    def approve_ticket_request(self, ticket: "Ticket") -> None:
        ticket.trip.approve_ticket(ticket)


class BusManager(AuthorizedUser, IBusManager):

    def sell_ticket(self, ticket: "Ticket") -> None:
        ticket.trip.sell_ticket(ticket)

    def refund_ticket(self, ticket: "Ticket") -> None:
        ticket.trip.refund_ticket(ticket)


class Superuser(BusManager, TripManager):
    def __str__(self):
        return f"Superuser ({self.email})"
