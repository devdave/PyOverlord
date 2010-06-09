Project: PyOverlord
Alt. name: overlord of python
Alt. name: Lord python over
Alt. name: Python Overlord of python
Alt. name: Python Overlord
Short name: PyOV

Description:
   Currently in the prototyping phase, PyOv acts as a dedicated or dynamic proxt between a remote host
and the client.

Initial uses:
   Given a project website that requires a host-name to function, it would be either impossible or tedious
   to get a client to properly configure their host name.  Worse still, lets say 10 developers in an office all
   have their own running instance, to be able to reach each host would require constant mucking around with hosts files
   or a dedicated internal DNS.
   
Does it work? NO

Why
   Most of the intermediate URL logic functions as expected EXCEPT in the case of 3xx redirects.  To fix this will require
   a custom urlhandler for urllib2.