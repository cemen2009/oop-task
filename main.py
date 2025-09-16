import datetime
from decimal import Decimal

from bus_service import (
    UnauthorizedUser,
    AuthorizedUser,
    TripManager,
    BusManager,
    Superuser,
    Ticket,
)
from bus_service.bus_service import SortBy


def main():
    trips = []
    tickets = []

    guest = UnauthorizedUser("John", "john.cena@user.com")
    print(guest)

    user = AuthorizedUser("Dwayne", "dwayne.howard@user.com")
    print(user)

    trip_manager = TripManager("Immanuel", "immanuel.kant@user.com")
    print(trip_manager)

    bus_manager = BusManager("Mario", "mario.ballotelli@user.com")
    print(bus_manager)

    admin = Superuser("Anthony", "anthony.joshua@user.com")
    print(admin)

    kyiv_poltava_trip = trip_manager.create_trip(
        Decimal(148.8),
        "Kyiv",
        datetime.date(2026, 6, 7),
        "Poltava",
        datetime.date(2026, 6, 8),
        15
    )
    lviv_ternopil_trip = trip_manager.create_trip(
        Decimal(67),
        "Lviv",
        datetime.date(2025, 10, 21),
        "Ternopil",
        datetime.date(2025, 10, 21),
        32
    )

    trips += [kyiv_poltava_trip, lviv_ternopil_trip]

    print("\n=========================================\nList of trips for unauthorized user:")
    guest.get_trips(trips, sort_by=SortBy.ARRIVAL_DATE)
    print("=========================================\n")

    # selling ticket
    print("=========================================\nTicket example 0")
    new_ticket_00 = kyiv_poltava_trip.create_ticket(seats_amount=1)
    user.request_ticket(new_ticket_00)

    trip_manager.approve_ticket_request(new_ticket_00)

    bus_manager.sell_ticket(new_ticket_00)

    bus_manager.refund_ticket(new_ticket_00)

    print(new_ticket_00)
    print("\n\nTicket example 1")

    new_ticket_01 = lviv_ternopil_trip.create_ticket(seats_amount=5)

    user.request_ticket(new_ticket_01)

    admin.approve_ticket_request(new_ticket_01)
    admin.sell_ticket(new_ticket_01)
    admin.refund_ticket(new_ticket_01)

    print(new_ticket_01)
    print("\n=========================================\nsorting example\n")

    new_trip = admin.create_trip(
        Decimal(101),
        "Odesa",
        datetime.date(2024, 11, 19),
        "Uman",
        datetime.date(2024, 11, 19),
        32
    )
    trips.append(new_trip)

    print("without sorting:")
    user.get_trips(trips, sort_by=SortBy.DEPARTURE_DATE)
    print("\nwith arrival date sorting:")
    user.get_trips(trips, sort_by=SortBy.ARRIVAL_DATE)

    print("\n=========================================\nratings example\n")

    new_trip.add_rating(user, 4.3)
    new_trip.add_rating(guest, 4.9)

    kyiv_poltava_trip.add_rating(user, 4.9)
    kyiv_poltava_trip.add_rating(guest, 4.1)

    lviv_ternopil_trip.add_rating(user, 4.5)
    lviv_ternopil_trip.add_rating(guest, 2.8)

    user.get_trips(trips, sort_by=SortBy.RATING)


if __name__ == "__main__":
    main()
