## About

Pytt (Python Torrent Tracker, pronounced as 'pity') is a BitTorrent Tracker written in Python using non-blocking Tornado Web Server. It also features a nice and clean UI for showing Tracker statistics.

__Work In Progress__: _May not work as a fully functioning Torrent Tracker_.

## Installing Pytt

To install Pytt, run

	sudo python setup.py install

## Configuring Pytt

Edit `~/.pytt/config/pytt.conf` and change the values to your choice. The following options are available.

- `port`: Pytt will listen to this port
- `interval`: Interval in seconds that the client should wait between sending regular requests to the tracker.
- `min_interval`: Minimum announce interval. If present clients must not re-announce more frequently than this.

## Running Pytt

To run Pytt, do

	python tracker.py -b

or

	pytt -d

- `-p` or `--port` (optional): To specify port
- `-d` or `--debug` (optional): Enable debug mode
- `-b` or `--background` (optional): Run as a daemon process

## License

MIT License. Refer COPYING for more info.
