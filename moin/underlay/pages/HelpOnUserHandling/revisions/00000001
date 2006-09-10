##master-page:HelpTemplate
##master-date:Unknown-Date
#format wiki
#language en

[[TableOfContents]]

= How to maintain your user data =

User data is stored in directory data/user in files that have the user id as filename. The files with the appendix .trail contain a history of what pages the user visited last.

To speed up processing, MoinMoin may also generate some data structures that get saved to disk as *.pickle file - these are internal data structures and you must not edit those files. If you are in doubt whether such a *.pickle file is correct or up-to-date, then just delete it and it will be re-generated automatically by moin. If you run a persistent (non-cgi) moin, maybe better restart MoinMoin after deleting the pickle.

== Disable a user account ==

You can disable a user account if you are logged in as a superuser (see HelpOnSuperUser) and choose to login to the account of the user via the superuser preferences (so than you will be the user to be deleted) and choose "Disable this account forever" in the preferences. After that you should logoff.

== Removing a user account ==
You can remove a user by deleting his user file (and other files that are named with that userid prefix).

Be aware that if you do that, you will destroy the edit history of that user. Moin won't be able to show this user in page history, because this user id will then be unknown. So better disable an account rather than removing it. After user data is deleted, MoinMoin may still think the user exists due to the user cache in data/cache/user/name2id.  Deleting this file purges the cache and should fix this problem.

== One wiki for user home pages ==

Yyou can set the value {{{user_homewiki}}} to have one wiki where all the user home pages are stored. Useful if you have many users. You could even link to nonwiki "user pages" if the wiki username is in the target URL.

== Merging userbases ==

You can merge two different wiki user bases to one. You can copy all those user files from one wiki to the other, but you should make sure that no user exists twice. The username can be found at "name=" in a user file.
