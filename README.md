This project adds blog posts to a database.

DEPLOYMENT

This project runs on Linux, and requires python 3 and sqlite3:

	Ubuntu:  sudo apt-get install python3 sqlite3

Get the archive from the github repository:

	https://github.com/maharvey/blogpostapi

While it is possible to run this project directly from the github
repository, it is intended to create a tarball that can be copied
to any machine and extracted there. The blog.db database is an optional
component; if not distributed, the server will create an empty database
when it is run.

To create a tarball of only the server,

	mkdir blogserver
	cp server.py blogserver
	cp README.* blogserver
	cp *.db blogserver # optional
	tar zcf blogserver.tgz blogserver

To deploy, copy blogserver.tgz to a machine that has the python3 and
sqlite3 packages installed, and extract:

	tar zxf blogserver.tgz

To run the server,

	cd blogserver
	python3 server.py >blogserver.log


KNOWN BUGS AND LIMITATIONS

The blog server only runs on localhost, port 80.


TESTING

While the API can be tested using curl, a cli component is included for
testing purposes. This makes use of standard libraries and can find things
that are not obvious using curl, and can serve as a starting point for
implementing unit/regression tests.

The cli relies on the requests library.

	https://github.com/requests/requests
	http://docs.python-requests.org/en/master/user/install/

