#!/usr/bin/env python2.7.12
import sys
import psycopg2


# join table-articles with table-log by (articles.slug, log.path)
# goup the new table by articles.id
# get the three articles with most page views
query1 = """
select articles.title, count(log.id) as num
from articles left join log
on log.path = concat('/article/',articles.slug)
group by articles.id
order by num desc
limit 3
"""


# join table-articles with table-log by (articles.slug, log.path) as table1
# join table-authors with table 1 by (authors.id, articles.author)
# group the new table by authors.id
# get the author with most page views
query2 = """
select authors.name, count(table1.id) as num
from authors left join

(select articles.author, log.id
from articles left join log
on log.path = concat('/article/',articles.slug))
as table1

on authors.id = table1.author
group by authors.id
order by num desc
limit 3
"""


# 1.group table-log by date
#    select (date, count(*) as num1) as table1
# 2.group table-log by date,status
#    select (date, status, count(*) as num2) as table2
# 3.join table1 and table2
#    select( table2.date, table2.status, table2.num2,table1.num1) as table3
# 4.select date and percentage(num2/num1)
#    from table3 where (status = '404' and percentage> 1%)
query3 = """
select date, round((table3.num2::decimal/table3.num1)*100,3) as percent
from

(select table2.date, table2.status, table2.num2, table1.num1
from

(select date(log.time) as date, count(*) as num1
from log
group by date(time)) as table1

right join

(select date(time) as date, status, count(*) as num2
from log
group by date(time), status) as table2

on table1.date = table2.date) as table3

where table3.num2::decimal/table3.num1>0.01 and table3.status ='404 NOT FOUND'
"""


def connect(db_name="news"):
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname={}".format(db_name))
        c = db.cursor()
        return db, c

    except psycopg2.Error as e:
        print "Unable to connect to database"
        # THEN exit the program
        sys.exit(1)


def fetch_query(query):
    """Connect to the database, query, fetch results, close, return results."""
    db, c = connect()
    c.execute(query)
    rows = c.fetchall()
    db.close()
    return rows


def print_top_articles(query):
    """
    Fetch top articles using helper function, print results.
    """
    rows = fetch_query(query)
    print "Problem 1 Answer:", "\n"
    for row in rows:
        print row[0] + " - " + str(row[1]) + " views"
    print "\n"


def print_top_authors(query):
    """
    Fetch top authors using helper function, print results.
    """
    rows = fetch_query(query)
    print "Problem 2 Answer:", "\n"
    for row in rows:
        print row[0] + " - " + str(row[1]) + " views"
    print "\n"


def print_top_error_days(query):
    """
    Fetch top error days using helper function, print results.
    """
    rows = fetch_query(query)
    print "Problem 3 Answer:", "\n"
    for row in rows:
        print str(row[0]) + " - " + str(row[1]) + "%" + " errors"
    print "\n"


if __name__ == '__main__':
    print_top_articles(query1)
    print_top_authors(query2)
    print_top_error_days(query3)

