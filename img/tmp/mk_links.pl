#!/usr/bin/env perl
use strict; use warnings; use utf8; use 5.10.0;
use Path::Tiny qw/path/;

my $template = '    - <img src="img/xx" alt="" width="80%"/>';
my $res = '';
foreach my $f (split "\n", `ls *.png`) {
    my $str = $template;
    $str =~ s/xx/$f/;
    $res .= $str."\n";
}

spew_and_say($res,'/tmp/mk_links.txt');

sub spew_and_say {
    my ($res,$tmp) = @_;
    path($tmp)->spew($res);
    system("cat $tmp | xclip -i -selection clipboard");
    say $res;
}

# Iterate over all filenames and generate

