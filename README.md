# Booking SDK

A Python SDK for interfacing with a booking server. 

## Existing code

### Overview

ExpressJS server with the following endpoints:
- `GET` `/bookings`
- `GET` `/users`
- `POST` `/bookings` (JSON body: `{ "time": 1534722030718, "duration": 3600000, "user_id": 1 }`)

### Instructions for use

- To install dependencies: `yarn install`
- To run the ExpressJS server: `yarn run server` (the server will be available at `http://localhost:3001`)

## Additional required features

Implement a Python wrapper for this server API called `booker` that behaves in the manner presented in `main.py`.

That is:
- `booker.connect()` fetches the users and bookings from the server and makes them available as member variables of a `client` object
- each booking object has the associated user object available as a member variable
- each user object has the associated list of booking objects available as a member variable
- bookings can be created for a user via a method on the user object
- bookings that overlap with any existing bookings (from any user) can not be created

Test your implementation by running `python main.py`. 

If you're having trouble starting, the [`requests`](http://docs.python-requests.org/en/master/) library is useful for making HTTP requests to the server. If you need a bit more help with any part, please send us an email and we'll give you a pointer. 