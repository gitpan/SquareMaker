This simple tool is compose of 4 files

SQUARE.cgi		the perl script
squaremaker.html	the form
cgi-lib.pl		The cgi-lib.pl library has become the de facto standard
			library for creating Common Gateway Interface (CGI)
			scripts in the Perl language
separator_skip.html	a file to explain the field separator and the checkbox
			Skip blanks


1) Check if you have PERL. You can find it at http://www.perl.com

2) Control the path of your perl installation. The default in SQUARE.cgi is
   #!/usr/local/bin/perl -Tw

3) Check if you have GD.pm (A graphics library for fast GIF creation in perl).
   You can find it at http://www-genome.wi.mit.edu/ftp/pub/software/WWW/GD.html

4) Move SQUARE.cgi in /cgi-bin/ directory of your Web
   [Usually default is /usr/local/etc/httpd/cgi-bin]
   you have to modify the variables
   $SQUAREfile = "/usr/local/etc/httpd/htdocs/test/SQUARE.gif"; and the relative links
   print "<img src=\"/test/SQUARE.gif\"><p>\n";
   $LINEfile = "/usr/local/etc/httpd/htdocs/test/LINE.gif"; and the relative links
   print "<img src=\"/test/LINE.gif\"><p>\n";

5) Move cgi-lib.pl in the default directory of lib PERL
   [Usually /usr/local/lib/perl5]
   You can find the last version of cgi-lib.pl and documentation at
   http://www.bio.cam.ac.uk/cgi-lib/

I don't test this simple tool with PERL version 4. I hope it works.
