# House Crew Coffee Control

## About
Really simple web application to manage who wants coffee in my household.
Roommates names hard-coded in as are IDs and event names... nothing fancy!
All clients connected should have synchronized checkbox states.

Make sure you hit the "I made a new pot" button after brewing a batch.
This resets the timer and notifies all other connected clients.

## Development
- must have `virtualenv` and `virtualenvwrapper` installed.
- must have `foreman` installed

- `pip install -r requirements.txt`
- `foreman start`

Uses flask as a webserver and socket.io for real time b/w server and clients.
