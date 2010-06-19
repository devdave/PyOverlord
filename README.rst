Project: PyOverlord
Alt. names:
*overlord of python
* Lord python over
* Python Overlord of python
* Python Overlord

Short name
   PyOV

Description:
   Currently in the prototyping phase, PyOv acts as a dedicated or dynamic proxt between a remote host
and the client.

Initial uses:
   Given a project website that requires a host-name to function, it would be either impossible or tedious
   to get a client to properly configure their host name.  Worse still, lets say 10 developers in an office all
   have their own running instance, to be able to reach each host would require constant mucking around with hosts files
   or a dedicated internal DNS.
   
Does it work? Kind of 2010-06-18

Why
   Most of the intermediate URL logic functions as expected EXCEPT in the case of 3xx redirects.  To fix this will require
   a custom urlhandler for urllib2.
   
   
Changelog:
20090618
   Took another crack at what I mistakingly percieved as a character encoding issue.   