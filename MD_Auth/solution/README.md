# Solution

The solution consists in exploiting a weak secret in the signature scheme, combined with a wrong argument in the md5 call() and a blind SQLite injection.

## Signature scheme

All the md5() calls in the code are coupled with the use of a secret, `APP_SALT`. The code indicates that this secret is only 7-digit long, therefore it can be bruteforced.
It is possible to trigger the account lock, to ensure that the cookie is `md5(APP_SALT + '5')`, and then bruteforce the secret.


## MD5 wrong argument

The md5() call on the password is called after the `escapeString` call, and uses `true` as a second argument. This argument causes the output to be as a binary contrary to the standard hexadecimal output. Therefore, this output may contains single quotes that will circumvent the sql injection protections.
While it would be very difficult to force the binary output to contain a fully functional sql injection, it is possible to begin a comment within the password, and close it in the login to begin the injection.
This equals to a bruteforce on salted md5 to have `'/*` in the password hash (with no previous quote).


## (Blind) SQL Injection

Last part is trivial, and consists in exploiting an SQL injection in the login/password fields. Using the `sqlite_master` table, we can retrieve the schema of the `users` table, then the `flag_field` field in this table to retrieve the flag.
