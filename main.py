import booker

client = booker.connect()

users = client.users

assert users[0].id == 1
assert users[0].name == "Mel"
assert len(users[0].bookings) == 3
assert len(users) == 3

bookings = client.bookings
assert bookings[0].id == 1
assert bookings[0].time == 1519866000000
assert bookings[0].duration == 10800000
assert bookings[0].user.id == 1
assert bookings[0].user.name == "Mel"
assert len(bookings) == 5

newBooking1 = users[1].addBooking(1520056800000, 3600000) # doesn't overlap
newBooking2 = users[1].addBooking(1520042400000, 3600000) # overlaps

assert newBooking1.id == 6
assert newBooking1.time == 1520056800000
assert newBooking1.duration == 3600000
assert newBooking1.user.id == 2
assert newBooking1.user.name == "Ash"
assert newBooking2 == False # overlaps with existing booking
assert len(users[0].bookings) == 3
assert len(client.bookings) == 6

print('Booker SDK successfully implemented!')