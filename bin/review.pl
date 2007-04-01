#!/usr/bin/perl

use strict;
use warnings;

use DBI;

my $db_name = "lca2007";
my $data_source = "dbi:Pg:dbname=$db_name";

my ($dbh);
$dbh = DBI->connect($data_source);


my (%familiarity, %technical, %experience, %coolness);
my (%proposal);
my (@reviewers);

get_proposals();
get_reviews();
get_reviewer_handles();


open REVIEWS, ">reviews.csv" or die "Couldn't open reviews: $!\n";

my $reviewers = join ",", @reviewers;
my $num_reviewers = @reviewers;
print REVIEWS ",,,,";
print REVIEWS "Familiarity" . ',' x $num_reviewers;
print REVIEWS "Technical" . ',' x $num_reviewers;
print REVIEWS "Experience" . ',' x $num_reviewers;
print REVIEWS "Coolness" . ',' x $num_reviewers;
print REVIEWS "\n";
print REVIEWS "\"ID\", \"Title\", \"Type\", \"Assistance\",$reviewers,$reviewers,$reviewers,$reviewers\n";

foreach my $proposal_id (keys %technical) {
    print REVIEWS "$proposal_id,\"$proposal{$proposal_id}{'title'}\",\"$proposal{$proposal_id}{'type'}\",$proposal{$proposal_id}{'assistance'}";

    foreach my $thingy ( (\%familiarity, \%technical, \%experience, \%coolness)) {
	my @results = ();
	foreach my $handle (@reviewers) {
	    if (!exists $thingy->{$proposal_id}->{$handle}) {
		push @results, "NA";
	    }
	    else {
		push @results, $thingy->{$proposal_id}->{$handle}
	    }
	}
	print REVIEWS ",";
	print REVIEWS join ",", @results;
    }
    print REVIEWS "\n";
}

close REVIEWS;

open PROPOSALS, ">proposals.csv" or die "Couldn't open proposals: $!\n";
print PROPOSALS "id,title,type,name,email\n";
foreach my $proposal_id (keys %technical) {
    print PROPOSALS "$proposal_id,\"$proposal{$proposal_id}{'title'}\",\"$proposal{$proposal_id}{'type'}\",";
    print PROPOSALS "\"$proposal{$proposal_id}{'name'}\",\"$proposal{$proposal_id}{'email'}\"\n";
}
close PROPOSALS;

    

$dbh->disconnect;


sub get_reviewer_handles {


    my %seen = ();
    foreach my $proposal_id (keys %technical) {
	foreach my $handle (keys %{ $technical{$proposal_id} }) {
	    push @reviewers, $handle if !$seen{$handle}++;
	}
    }
}

sub get_reviews {

    my $sth = $dbh->prepare("
    SELECT
	proposal_id, handle, familiarity, technical, experience, coolness, stream_id
    FROM
	review, person
    WHERE
	review.reviewer_id = person.id
    ");

    $sth->execute();
    my ($proposal_id, $handle, $familiarity, $technical, $experience, $coolness, $stream_id);

    $sth->bind_columns(\$proposal_id, \$handle, \$familiarity, \$technical, \$experience, \$coolness, \$stream_id);

    while($sth->fetch()) {
	$familiarity{$proposal_id}{$handle} = $familiarity;
	$technical{$proposal_id}{$handle} = $technical;
	$experience{$proposal_id}{$handle} = $experience;
	$coolness{$proposal_id}{$handle} = $coolness;
    }
}


sub get_proposals {

    my $sth = $dbh->prepare("
    SELECT
	proposal.id, title, proposal_type.name, assistance, firstname, lastname, email_address, handle
    FROM
	proposal, proposal_type, person_proposal_map, person, account
    WHERE
	proposal.proposal_type_id = proposal_type.id
	AND
	person_proposal_map.proposal_id = proposal.id
	AND
	person_proposal_map.person_id = person.id
	AND
	person.account_id = account.id
    ORDER BY
    	proposal.id
    ");

    $sth->execute();
    my ($proposal_id, $title, $type, $assistance, $firstname, $lastname, $email, $handle);

    $sth->bind_columns(\$proposal_id, \$title, \$type, \$assistance, \$firstname, \$lastname, \$email, \$handle);

    while($sth->fetch()) {

	if (!defined $firstname) {
	    $firstname = 'No';
	}
	if (!defined $lastname) {
	    $lastname = 'Name';
	}
	if (!defined $handle) {
	    $handle = 'nohandle';
	}
	my $name = "$firstname $lastname";
	if (exists $proposal{$proposal_id}) {
	    $proposal{$proposal_id}{'name'} .= ",$name";
	    $proposal{$proposal_id}{'handle'} .= ",$handle";
	    $proposal{$proposal_id}{'email'} .= ",$email";
	    next;
	}
	$proposal{$proposal_id}{'title'} = $title;
	if(!defined $assistance) {
	    $assistance = 'Unknown';
	}
	elsif ($assistance) {
	    $assistance = 'True';
	}
	else {
	    $assistance = 'False';
	}
	$proposal{$proposal_id}{'type'} = $type;
	$proposal{$proposal_id}{'assistance'} = $assistance;
	$proposal{$proposal_id}{'name'} = $name;
	$proposal{$proposal_id}{'handle'} = $handle;
	$proposal{$proposal_id}{'email'} = $email;


#warn "$proposal_id, $title, $type, $assistance\n";
    }
}


