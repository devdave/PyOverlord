Project: PyOverlord
Alt. names

* overlord of python
* Lord python over
* Python Overlord of python
* Python Overlord

Short name
   PyOV

Description:
   Currently in the prototyping phase, PyOv acts as a dedicated or dynamic proxt between a remote host and the client.

Initial uses:
   Given a project website that requires a host-name to function, it would be either impossible or tedious
   to get a client to properly configure their host name.  Worse still, lets say 10 developers in an office all
   have their own running instance, to be able to reach each host would require constant mucking around with hosts files
   or a dedicated internal DNS.
   
Does it work? Kind of 2010-06-18
   
   
Changelog:
20100618
   Took another crack at what I mistakingly percieved as a character encoding issue but turned out to be a transport
   encoding issue.  Once I noticed content-encoding and setup the correct de-compression mechanism, everything
   was happpy.

20100618
   Starting to cleanup the whole mess and get it into a cleaner foundation to build on.
   
Roadmap:
   * Cleanup the codebase a bit more, add a static path for content ( Javascript, css, etc )
   * Database capturing of the dialog focusing on text/* content ( waste of space to store images/binaries )
   * During the above, add in instrumentation to review DB content
   * Add ability to store in DB or some other store host names
   * Mid-point optimization, cleanup & refactor as necessary for speed/memory concerns
   * Feasibility study of integrating JS or some other scripting language for TRX processing
   * Feasibility study of using JS or pure Python for applying tests ( ex has etags, caching, etc )
   * Add payload injects for on page comments and tools
   * Also, at the end there will be cake.
