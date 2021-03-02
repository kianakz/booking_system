const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');

const app = express();
app.use(bodyParser.json()); // for parsing application/json

const bookings = JSON.parse(fs.readFileSync('./server/bookings.json'))
  .map((bookingRecord) => ({
    id: bookingRecord.id,
    time: Date.parse(bookingRecord.time),
    duration: bookingRecord.duration * 60 * 1000, // mins into ms
    userId: bookingRecord.user_id,
  }));

const nextBookingId = bookings.reduce((id, booking) => Math.max(booking.id, id), 0) + 1;

const users = JSON.parse(fs.readFileSync('./server/users.json'))
  .map((userRecord) => ({
    id: userRecord.id,
    name: userRecord.name,
  }));

app.get('/bookings', (_, res) => {
  res.json(bookings);
});

app.get('/users', (_, res) => {
  res.json(users);
});

app.post('/bookings', (req, res) => {
  if (!users.some((user) => user.id === req.body.user_id)) {
    res.status(400);
    return res.json({ message: 'No user with this ID found' });
  }
  const newBooking = { id: nextBookingId, time: req.body.time, duration: req.body.duration, userId: req.body.user_id };
  bookings.push(newBooking);
  res.json(newBooking);
});

app.listen(3001);
