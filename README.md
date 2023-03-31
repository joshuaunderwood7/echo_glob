# echo_glob
Monitor directories for log files and echo them to STDOUT

Have you ever needed to monitor a directory that has rotating log files, 
changing filenames, or otherwise just want to `tail -f *` and 
have the system know when new files showed up?  Then `echo_glob.py` 
is the tool that you need.  

It does this one thing, where it montors a file glob.glob and if a new 
file shows up, it includes it in the output.  If a file goes away, it 
doesn't care.

I hope this helps someone out there do whatever it is they want it to do.
