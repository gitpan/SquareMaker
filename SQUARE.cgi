#!/usr/local/bin/perl -Tw

# $Header: SQUARE.cgi,v 4.2 1997/06/19 $
# 1997 Fabrizio Pivari (Pivari@geocities.com)
# "Simple Magic Square checker and gif maker" script

require "cgi-lib.pl";
# with CGI.pm you can use
#use CGI qw(:cgi-lib);
use GD;

MAIN:
{
$SQUAREfile = "/usr/local/etc/httpd/htdocs/test/SQUARE.gif";
$LINEfile = "/usr/local/etc/httpd/htdocs/test/LINE.gif";

# Read in all the variables set by the form
  &ReadParse(*input);

$separator = $input{'separator'};
if ($separator eq "") {$separator = " ";}
$square = $input{'square'};
$skipblank = $input{'skipblank'};
$table  = $input{'table'};
$gif    = $input{'gif'};
$check  = $input{'check'};
$transparent  = $input{'transparent'};
$rbg  = $input{'rbg'};
$gbg  = $input{'gbg'};
$bbg  = $input{'bbg'};
$rfg  = $input{'rfg'};
$gfg  = $input{'gfg'};
$bfg  = $input{'bfg'};

if ($separator eq "" || $separator eq " ")
   {
   if ($skipblank eq "skipblank")
      {$square =~ s/\r\s*/ /g; $square =~ s/^\s*//; $square =~ s/\s+/ /g;}
   else {$square =~ s/\r\n/ /g;}
   }
else
   {
   if ($skipblank eq "skipblank")
      {$square =~ s/\r\s*/$separator/g;$square =~ s/^\s*//; $square =~ s/\s+//g;}
   else {$square =~ s/\r\n/$separator/g;}
   }

@all = split(/$separator/,$square);
$ORD = sqrt($#all+1);
if ($ORD =~ /\d+\.\d+/)
   {
   print &PrintHeader;
   print &HtmlTop ("Error");
   print " The number of elements in every line or column is not the
         same\n";
   print &HtmlBot;
   exit 1;
   }
$i=0; $j=0;
foreach $all (@all)
   {
   $elem[$j][$i] = $all;
   $i++;
   if (($i)%$ORD == 0) {$j++; $i=0;}
   }

# $ORD = $#line+1;
$CELLGRIDSIZE = 31;
$GRIDSIZE = 8+($ORD -1)*2+$ORD*$CELLGRIDSIZE;

# Print the header
   print &PrintHeader;
   print &HtmlTop ("$ORD x $ORD Magic Square");

if ($check eq "check")
   {
# Magic constant for a Magic Square 1,2,...,n
   $sum=$ORD*($ORD*$ORD+1)/2;
   $i=0;
# Generic magic constant
   for(0..$ORD-1) { $SUM+=$elem[0][$i]; $i++;}
# Check lines and columns
   $j=0;
   for($j=0;$j<$ORD;$j++)
      {
      $i=0; $line1=0; $line2=0;
      for($i=0;$i<$ORD;$i++)
         {
         $line1+=$elem[$j][$i];
         $line2+=$elem[$i][$j];
         }
      if ($line1 != $SUM || $line2 != $SUM)
         {
         print "This isn't a magic square<p>\n";
         goto NEXT;
         }
      }

# Check diagonals and broken diagonals
   $j=0;
   for($j=0;$j<$ORD;$j++)
      {
      $i=0; $diag1=0; $diag2=0;
      for($i=0;$i<$ORD;$i++)
         {
         $diag1+=$elem[$i][($i+$j)%$ORD];
         $diag2+=$elem[$ORD-1][($i+$j)%$ORD];
         }
      if ($j == 0)
         {
         if ($diag1 != $SUM || $diag2 != $SUM)
            {
            if ($SUM == $sum)
               {
               print "This is a Semimagic Square with magic constant
                      n(n<sup>2</sup>+1)/2 = $sum<p>\n";
               goto NEXT;
               }
            else
               {
               print "This is a Semimagic Square with magic constant = $SUM<p>\n";
               goto NEXT;
               }
            }
         }
      else
         {
         if ($diag1 != $SUM || $diag2 != $SUM)
            {
            if ($SUM == $sum)
               {
               print "This is a Magic Square with magic constant
                      n(n<sup>2</sup>+1)/2 = $sum<p>\n";
               $k=1;
               $MIDDLE = ($CELLGRIDSIZE+1)/2;
               $im=new GD::Image($GRIDSIZE,$GRIDSIZE);
               $bg=$im->colorAllocate($rbg,$gbg,$bbg);
               $fg=$im->colorAllocate($rfg,$gfg,$bfg);

               # GRID
               if ($transparent eq "yes") {$im->transparent($bg);}
               $im->filledRectangle(0,0,255,255,$bg);
               $im->filledRectangle(0,0,4,$GRIDSIZE,$fg);
               $im->filledRectangle(0,0,$GRIDSIZE,4,$fg);
               $tmp = $GRIDSIZE -5;
               $im->filledRectangle($tmp,0,$GRIDSIZE,$GRIDSIZE,$fg);
               $im->filledRectangle(0,$tmp,$GRIDSIZE,$GRIDSIZE,$fg);
               $xy = 4 + $CELLGRIDSIZE;
               $xy2 = $xy +2;
               for (1..$ORD-1)
                  {
                  $im->filledRectangle($xy,0,$xy2,$GRIDSIZE,$fg);
                  $im->filledRectangle(0,$xy,$GRIDSIZE,$xy2,$fg);
                  $xy = $xy2 + $CELLGRIDSIZE;
                  $xy2 = $xy + 2;
                  }

               ANOTHER:    $j=0;
               for($j=0;$j<$ORD;$j++)
                  {
                  $i=0;
                  for($i=0;$i<$ORD;$i++)
                     {
                     if ($elem[$j][$i] == $k)
                        {
                        if ($elem[$j][$i] == 1)
                           {
                           $x1=$i*$CELLGRIDSIZE+$MIDDLE+4+$i*2;
                           $y1=$j*$CELLGRIDSIZE+$MIDDLE+4+$j*2;
                           $im->arc($x1,$y1,2,2,0,360,$fg);
                           $k++;
                           goto ANOTHER;
                           }
                        $x2=$i*$CELLGRIDSIZE+$MIDDLE+4+$i*2;
                        $y2=$j*$CELLGRIDSIZE+$MIDDLE+4+$j*2;
                        $im->line($x1,$y1,$x2,$y2,$fg);
                        $im->arc($x2,$y2,2,2,0,360,$fg);

                        $x1=$x2;
                        $y1=$y2;
                        $k++;
                        goto ANOTHER;
                        }
                     }
                  }
               open (LINE,">$LINEfile") || die "Error: $LINEfile - $!\n";
               print LINE $im -> gif;
               close (LINE);

               print qq!<img src="/test/LINE.gif"><p>\n!;

               goto NEXT;
               }
            else
               {
               print "This is a Magic Square with magic constant = $SUM<p>\n";
               goto NEXT;
               }
            }
         }
      }
      if ($SUM == $sum) { print "This is a Panmagic Square with magic constant
                                 n(n<sup>2</sup>+1)/2 = $sum<p>\n";}
      else { print "This is a Panmagic Square with magic constant = $SUM<p>\n";}
   }

NEXT: if ($gif eq "gif")
   {
   $im=new GD::Image($GRIDSIZE,$GRIDSIZE);
   $bg=$im->colorAllocate($rbg,$gbg,$bbg);
   $fg=$im->colorAllocate($rfg,$gfg,$bfg);

   # GRID
   if ($transparent eq "yes") {$im->transparent($bg);}
   $im->filledRectangle(0,0,255,255,$bg);
   $im->filledRectangle(0,0,4,$GRIDSIZE,$fg);
   $im->filledRectangle(0,0,$GRIDSIZE,4,$fg);
   $tmp = $GRIDSIZE -5;
   $im->filledRectangle($tmp,0,$GRIDSIZE,$GRIDSIZE,$fg);
   $im->filledRectangle(0,$tmp,$GRIDSIZE,$GRIDSIZE,$fg);
   $xy = 4 + $CELLGRIDSIZE;
   $xy2 = $xy +2;
   for (1..$ORD-1)
      {
      $im->filledRectangle($xy,0,$xy2,$GRIDSIZE,$fg);
      $im->filledRectangle(0,$xy,$GRIDSIZE,$xy2,$fg);
      $xy = $xy2 + $CELLGRIDSIZE;
      $xy2 = $xy + 2;
      }

   # NUMBERS
   $x1 = 4 + 8;
   $y1 = 4 + 9;
   $j=0;
   for ($j=0;$j<$ORD;$j++)
      {
      $i=0;
      for ($i=0;$i<$ORD;$i++)
         {
         # to hit the centre with numbers < -9
         if ($elem[$j][$i] < -9) { $x1 = $x1 - 3; }
         # to hit the centre with numbers between -9 and -1
         if ($elem[$j][$i] < 0 && $elem[$j][$i] > -10) { $x1 = $x1 - 2; }
         # to hit the centre with numbers between 0 and 9
         if ($elem[$j][$i] < 10 && $elem[$j][$i] >= 0) { $x1 = $x1 + 4; }
         # to hit the centre with numbers > 99
         if ($elem[$j][$i] > 99) { $x1 = $x1 - 4; }
         $im->string(gdLargeFont,$x1,$y1,"$elem[$j][$i]",$fg);
         $x1 = $x1 + $CELLGRIDSIZE + 2;
         if ($elem[$j][$i] < -9) { $x1 = $x1 + 3; }
         if ($elem[$j][$i] < 0 && $elem[$j][$i] > -10) { $x1 = $x1 + 2; }
         if ($elem[$j][$i] < 10 && $elem[$j][$i] >= 0) { $x1 = $x1 - 4; }
         if ($elem[$j][$i] > 99) { $x1 = $x1 + 4; }
         }
      $x1 = 4 + 8;
      $y1 = $y1 + $CELLGRIDSIZE + 2;
      } 

   open (SQUARE,">$SQUAREfile") || die "Error: $SQUAREfile - $!\n";
   print SQUARE $im -> gif;
   close (SQUARE);

   print qq!<img src="/test/SQUARE.gif"><p>\n!;
   }

if ($table eq "table")
   {
   print qq!<table border=3 width="2" height="2" cellpadding=1 cellspacing=1>\n!;
   $j=0;
   for $j (0..$ORD-1)
      {
      $i=0;
      print "<tr>\n";
      for $i (0..$ORD-1)
         {
         print "<td align=right><font size=+2><b>$elem[$j][$i]</b></font></td>\n";
         }
      print "</tr>\n";
      }
   print "</table><p>\n";
   }

print qq!Generated with SquareMaker-4.2 written by <a href="mailto:Pivari\@geocities.com">Fabrizio Pivari</a>\n!;

# Close the document cleanly
   print &HtmlBot;

}
