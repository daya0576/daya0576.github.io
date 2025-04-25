---
layout: post
title: "Henry's Awesome Summary of Perl"
date: 2016-09-20 09:52:18
comments: true
tags: [unsw]
---

My summary of Perl in semester 16s2 of (COMP2041|COMP9041) in UNSW.    

<!--more-->
   

> My note of lectures, it was a mess and not well organized.    
So I decided to write this blog to make things clear(I need time to modify).       
<img style="max-height:350px" src="/images/blog/160920_perl/note.JPG"> 


>Perl = **P**ractical **E**xtraction and **R**eport **L**anguage    


# Running Perl code in the command line     
`perl -e ’print "Hello, world\n"; `



# #!/usr/bin/perl -w
Adding this line at the beginning of the file, which will let the operating system know that this file is Perl program so that it can be executed in this way:    
`chmod 755 PerlCodeFile;./PerlCodeFile.pl`   
`-w` means warnings.    



# Arithmetic & Logical Operators   
Numeric: `== != < <= > >= <=>`   
String: `eq ne lt le gt ge cmp`   



# Input/Output
Andrew always gives us advice to make our life easier, and one thing is always remembering to check the file is correctly opened.      
**Elegant usage of die:**       
```pl
# $0 is the perl filename, and $! is the error msg.     
open BOOK, "hp1.txt" or die "$0: open '$file' failed: $!" 
```
**Sample implementation of `cat`**     
```pl
while ($line = <STDIN>){
    print $line;
}
```
**read,  write and append**   
```pl
open(DATA, "<< data"); # read from file "data"

open(RES, ">> results"); # write to file "results"
print RES @array;

open(XTRA, ">>> stuff"); # append to file "stuff"
```
**Read content of web page through url:**   
```pl
open F, "wget -q -O- $url|" or die;
while ($line = <F>) {}
```
**Saving lines of file content to array**   
```pl
@lines = <STDIN>;
```



# Control Structures
**For loop**
```pl
foreach $arg (@ARGV){}

foreach $num (1..10){}

print "$_\n" foreach @list; 

foreach $file (glob *.txt){};
```
**If**     
Testing the line's content, `=~` is so useful in perl.     
```pl
if ($line =~ /($course_prefix[0-9]{4})<\/a>/){
    # print $line;
    print "$1\n";
}

# checking ctrl - D
last if (! $line)

```



# Data structure 
**String:**    
```pl
# "Henry\n" --> "Henry"
chmod $line;

$len = length $line;

$name.$no == "$name$no"
```
**split a string**:    
```pl
@field = split /,/, $line;
@words = split /\s+/, $line;
```
**Array**
```pl
$a[4] = 42;  # @a = (,,,,42)

# print array:
# @array = ("Henry", "is", "so", "cool");
@array = qw/Henry is so cool/;
print @array; # Henryissocool
print "@array"; # Henry is so cool

join(",", @array)

push <--> pop
shift  <--> unshift

# shift(only one word) can be used to shift element in ARGV.
shift;
$opt = shift @ARGV;

# get the length of the array 
len = @array
```
**Hash**    
Here is a useful example from my lab code:    
we can also see how sed work in perl:     
```pl
foreach $input (sort keys %total_p_of){
    # %poem_e = $total_p_of{$input};
    @poem_e_sort = sort { $total_p_of{$input}{$a} <=> $total_p_of{$input}{$b} } keys %{$total_p_of{$input}\};

    $p_e = $poem_e_sort[-1];
    $p_e =~ s|poems/||;
    $p_e =~ s/.txt//;
    $p_e =~ s/_/ /g;

    $p_sum = $total_p_of{$input}{$poem_e_sort[-1]};

    print sprintf("%s most resembles the work of %s (log-probability=%0.1f)\n",
                  $input, $p_e, $p_sum);
}
```



# SHELL Command in Perl
Perl is shell-like in the ease of invoking other commands/programs.
Several ways of interacting with external commands/programs:    
```pl
`cmd`; # capture entire output of cmd as single string
system("cmd"); # execute cmd and capture its exit status only
open(F,"cmd|");  # collect cmd output by reading from a stream
```



# Reference
This exaple explains this concept so well:
```pl
$henry = 42;
$fred = "henry";
$c = $$fred;  # => 42
```



# Math
**Square root**: `sqrt $x*$x + $y*$y`   
**Calculation of string**:     
```pl
$string = "1+2+3+4+5";
$result = eval $string;
```


