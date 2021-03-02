import requests


bookings = []  # A global variable that represents all the bookings for all the users

class APIError(Exception):
    # API exception handling
    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)


class booking:

    booking_id = 0  # static variable

    def __init__(self, time, duration, user):
        """
        :param time: int, unix time stamp
        :param duration: int
        :param user: user object
        """
        booking.booking_id += 1  # gets incremented by one each time a new booking is generated
        self.id = booking.booking_id
        self.time = time
        self.duration = duration
        self.user = user
        booking_json = {"id": self.id, "time": self.time, "duration": self.duration, "user_id": self.user.id}
        requests.post('http://localhost:3001/bookings/', json=booking_json)  # post to the server


class user:
    user_id = 0
    times = []
    durations = []

    def __init__(self, name):
        """
        :param name: string
        """
        user.user_id += 1  # static variable
        self.id = user.user_id
        self.name = name
        self.bookings = []

    def addBooking(self, time, duration):
        """
        :param time: int, unix time stamp
        :param duration: int
        :return: a booking instance
        """
        durations = user.durations
        start_time = time
        end_time = time + duration
        for i in range(len(bookings)):  # Go through all the existing bookings and check if the current booking overlaps
            start_time_exist = bookings[i].time
            end_time_exist = bookings[i].time + durations[i]
            if start_time_exist < end_time <= end_time_exist:  # Overlap case 1
                return False
            elif start_time_exist <= start_time < end_time_exist:  # Overlap case 2
                return False
            if start_time <= start_time_exist and end_time >= end_time_exist:  # Overlap case 3
                return False

        # Booking doesn't overlap, generate the booking object
        self.times.append(time)
        self.durations.append(duration)
        new_booking = booking(time, duration, self)  # Instantiate a booking object

        self.bookings.append(new_booking)
        bookings.append(new_booking)  # Add the booking to the global variable
        return new_booking


class client:

    def __init__(self, users):
        """
        :param users: a list of user objects
        """
        self.users = users
        self.bookings = bookings  # bookings is a global variable. The reason is that the "main.py" doesn't use getter
        # functions to recalculate all the bookings. The bookings are created when a client object is instantiated
        # (when main.py calls booker.connect()), and they won't be updated when main.py adds bookings.
        # Thus, I created a global variable for bookings to always keep track of all the bookings


def connect():
    """
    :return: a client object
    """
    # get users and bookings data
    resp_users = requests.get('http://localhost:3001/users')  # Get users json
    if resp_users.status_code != 200:  # If the connection wasn't successful
        raise APIError(resp_users)  # Throw error

    resp_bookings = requests.get('http://localhost:3001/bookings/')  # Get bookings json
    if resp_bookings.status_code != 200:  # If the connection wasn't successful
        raise APIError('GET /tasks/ {}'.format(resp_bookings.status_code))  # Throw error

    # Instantiate user objects
    users = []
    for user_js in resp_users.json():  # Go through each json item  and instantiate a user object
        user_name = user_js['name']  # Extract the user name
        new_user = user(user_name)  # Create user object
        users.append(new_user)

    # Add each booking to its corresponding user
    for booking_js in resp_bookings.json():
        user_id = booking_js['userId'] - 1  # Extract user id of booking_js
        booking_time = booking_js['time']  # Extract booking time
        bookings_duration = booking_js['duration']  # Extract booking duration
        users[user_id].addBooking(booking_time, bookings_duration)  # Add booking

    return client(users)  # Create a client object and return


