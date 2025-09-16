import uuid
from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from enum import Enum


class AbstractUser(ABC):
    """
    Basic interface for a user that can be superclass for
    all type of users (Trip Manager, Superuser, etc.)
    """

    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

        self.id = str(uuid.uuid4())

    @abstractmethod
    def get_trips(self, trips: list["Trip"], sort_by: Enum) -> list["Trip"]:
        """
        This method should return list of available trips and provide opportunity to sort by:
        - amount of available seats
        - departure
        - departure date
        - arrival
        - arrival date
        - rating

        Any user (Unauthorized, Authorized, Superuser, etc.) can access this method.

        :param trips: List of trips
        :param sort_by: Parameter for sorting
        :return:
        """
        pass

    def __str__(self):
        return f"Unauthorized user ({self.email})"


class IAuthorizedUser(ABC):
    """
    Interface for authorized users.
    Additional functionality: can request a ticket.
    """

    @abstractmethod
    def request_ticket(self, ticket: "Ticket") -> None:
        """
        User can trigger this method to request a ticket with specified ticket id.
        Trip manger should approve that request.

        :param ticket: A ticket
        :return: None
        """
        pass

    def __str__(self):
        return f"Authorized user ({self.email})"


class ITripManager(ABC):
    """
    Interface for trip manager.
    Additional functionality: can approve tickets, can CRUD tickets
    """

    @abstractmethod
    def create_trip(
            self,
            price: Decimal,
            departure: str,
            departure_date: date,
            arrival: str,
            arrival_date: date,
            total_seats: int,
    ) -> "Trip":
        pass

    @abstractmethod
    def update_trip(self,trip: "Trip", new_trip_data: dict) -> None:
        """
        This method should search for a trip with specified ID and update its data.

        :param trip: A trip
        :param new_trip_data: Dict with patrial or full data update
        :return: None
        """
        pass

    @abstractmethod
    def delete_trip(self, trip: "Trip") -> None:
        pass

    @abstractmethod
    def approve_ticket_request(self, ticket: "Ticket") -> None:
        """
        Approve a ticket request.

        :param ticket: Requested ticket.
        :return: None
        """
        pass

    def __str__(self):
        return f"Trip Manager ({self.email})"


class IBusManager(ABC):
    """
    Interface for bus manager.
    Additional functionality: can sell tickets, refund tickets.
    """

    @abstractmethod
    def sell_ticket(self, ticket: "Ticket") -> bool:
        """
        Sell this ticket if it was approved and seats amount is enough.

        :param ticket: Requested ticket.
        :return: bool
        """
        pass

    @abstractmethod
    def refund_ticket(self, ticket: "Ticket") -> bool:
        """
        Refund is only possible if ticket has actual date, amount of sold seats is greater than 0.

        :param ticket: Requested ticket.
        :return: bool
        """
        pass

    def __str__(self):
        return f"Bus Manager ({self.email})"


class AbstractTrip(ABC):
    """
    Interface of a trip.
    """

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
        self._ratings : list[float]= []
        self._tickets: list["Ticket"] = []

    @property
    def available_seats(self) -> int:
        """
        Return amount of available seats.

        :return: int
        """
        return self.total_seats - self.sold_seats

    def add_rating(self, user: "User", rating: float) -> None:
        """
        Add rating from a user to ratings list.

        :param user: A user that leave a rating.
        :param rating: Score of rating.
        :return: None
        """
        print(f"User {user.id} has added rating with score {rating}")
        self._ratings.append(rating)

    @property
    def average_rating(self) -> float:
        """
        Calculate average rating of a trip.

        :return: float
        """
        return sum(self._ratings) / len(self._ratings)

    @abstractmethod
    def create_ticket(
            self,
            requester: IAuthorizedUser,
            owner: IBusManager,
            price: Decimal = Decimal("0"),
            status: "TicketStatus | None" = None,
            seats_amount: int | None = None,
    ) -> "Ticket":
        pass

    @abstractmethod
    def request_ticket(self, ticket: "Ticket") -> None:
        pass

    @abstractmethod
    def approve_ticket(self, ticket: "Ticket") -> None:
        pass

    @abstractmethod
    def sell_ticket(self, ticket: "Ticket") -> None:
        pass

    @abstractmethod
    def refund_ticket(self, ticket: "Ticket") -> None:
        pass

    def __str__(self):
        return f"Trip {self.departure} -> {self.arrival} [{self.departure_date}]"
