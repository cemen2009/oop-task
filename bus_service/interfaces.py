from abc import ABC, abstractmethod
from datetime import date
from decimal import Decimal
from enum import Enum

from bus_service.bus_service import Trip


class IUser(ABC):
    """
    Basic interface for a user that can be superclass for
    all type of users (Trip Manager, Superuser, etc.)
    """

    @abstractmethod
    def get_trips(self, trips: list["Trip"], sort_by: Enum) -> list["Trip"]:
        """
        This method should return list of available trips and provide opportunity to sort by:
        - destination
        - amount of available seats
        - departure
        - arrival date
        - rating

        Any user (Unauthorized, Authorized, Superuser, etc.) can access this method.

        :param trips: list of trips
        :return:
        """
        pass

class IAuthorized(ABC):
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
    def approve_ticket_request(self, user: "User", ticket: "Ticket") -> None:
        """
        Approve a ticket request.

        :param user: A user that has requested a ticket.
        :param ticket: Requested ticket.
        :return: None
        """
        pass


class IBusManager(ABC):
    """
    Interface for bus manager.
    Additional functionality: can sell tickets, refund tickets.
    """

    @abstractmethod
    def sell_ticket(self, user: "User", ticket: "Ticket") -> bool:
        """
        Sell this ticket if it was approved and seats amount is enough.

        :param user: A user that has requested a ticket.
        :param ticket: Requested ticket.
        :return: bool
        """
        pass

    @abstractmethod
    def refund_ticket(self, user: "User", ticket: "Ticket") -> bool:
        """
        Refund is only possible if ticket has actual date, amount of sold seats is greater than 0.

        :param user: A user that has requested a refund.
        :param ticket: Requested ticket.
        :return: bool
        """
        pass


class ITrip(ABC):
    """
    Interface of a trip.
    """

    @abstractmethod
    def available_seats(self) -> int:
        """
        Return amount of available seats.

        :return: int
        """
        pass

    @abstractmethod
    def add_rating(self, user: "User", rating: float) -> None:
        """
        Add rating from a user to ratings list.

        :param user: A user that leave a rating.
        :param rating: Score of rating.
        :return: None
        """

    @abstractmethod
    def average_rating(self) -> float:
        """
        Calculate average rating of a trip.

        :return: float
        """
        pass
    
