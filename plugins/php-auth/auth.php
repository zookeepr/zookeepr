#!/usr/bin/php5
<?php
// Example showing how to authenticate a given user against the zookeepr database
//
// Requirements:
//   - php5-pgsql

$DBHOST = 'localhost';
$DBNAME = 'zk';
$DBUSER = 'zookeepr';
$DBPASS = 'zookeepr';

$ZKSALT = 'changeme';
$ZKITERATIONS = 400000;

$USEREMAIL = 'admin@zookeepr.org';
$USERPASS = 'password';

function check_password($email, $password) {
    global $DBHOST, $DBNAME, $DBUSER, $DBPASS;
    global $ZKSALT, $ZKITERATIONS;

    $dbconn = pg_connect("host=$DBHOST dbname=$DBNAME user=$DBUSER password=$DBPASS")
        or die('Could not connect: ' . pg_last_error());

    pg_prepare($dbconn, "pwcheck", 'SELECT password_hash, password_salt FROM person WHERE email_address = $1');
    $result = pg_execute($dbconn, "pwcheck", array($email));
    $expectedhash = pg_fetch_result($result, 0, 'password_hash');
    $usersalt = pg_fetch_result($result, 0, 'password_salt');
    pg_free_result($result);
    pg_close($dbconn);
    print "\t ZK:\t" . $expectedhash . "\n";

    $salt = $ZKSALT . $usersalt;
    // FIXME: switch back to PBKDF2 once Python 2.7.8 is in Ubuntu LTS (16.04)
    //$computedhash = hash_pbkdf2('sha256', $password, $salt, $ZKITERATIONS);
    $computedhash = hash('sha256', $password . $salt);
    print "\t PHP:\t" . $computedhash . "\n";

    return $expectedhash === $computedhash;
}

print "$USEREMAIL:\n";
if (check_password($USEREMAIL, $USERPASS)) {
    print "Correct password\n";
} else {
    print "Incorrect password\n";
}
