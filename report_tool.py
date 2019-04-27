#!/usr/bin/env python3
# -*- encoding: utf-8 -*-  # Use if python2

import psycopg2
import sys

DBNAME = "news"
USER = "vagrant"

def connect(database_name, user):
    """
        Connect to the PostgreSQL database. Returns a database connection
        Use this like so:
        db, cursor = connect(DBNAME)
    """
    try:
        db = psycopg2.connect("dbname={} user={}".format(database_name, user))
        cursor = db.cursor()
        return db, cursor
        """
            db, cursor: is a tuple.
            The first element (db) is a connectin to the database.
            The second element (cursor) is a cursor for the database.
        """
    except  (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)

def answer1():
    """Answer the first question """
    top3_articles_sql = """
        select a.title, t3.count 
        from 
            articles as a, 
            (
                select count(*), overlay(path placing '' from 1 for 9) as slug 
                from log 
                where path != '/'
                and status != '404 NOT FOUND'
                group by path 
                order by 1 desc 
                limit 3
            ) as t3 
        where a.slug = t3.slug 
        order by 2 desc;"""
    print("Question 1: What are the most popular three articles of all time?\n")
    db, cursor = connect(DBNAME, USER)
    cursor.execute(top3_articles_sql)
    top3_articles = cursor.fetchall()
    cursor.close()
    db.close()
    top3_articles_formated = "\n".join(['   "{}" - {} views'.format(x[0],x[1]) for x in top3_articles])
    print(top3_articles_formated)


def answer2():
    """Answer the second question """
    print("Question 2: Who are the most popular article authors of all time?\n")
    db, cursor = connect(DBNAME, USER)
    top_authors_sql = """
        select au.name, count(*)
        from authors as au, articles as ar, log as l
        where au.id = ar.author
        and ar.slug = overlay(l.path placing '' from 1 for 9)
        group by au.name
        order by 2 desc;"""
    cursor.execute(top_authors_sql)
    top_authors = cursor.fetchall()
    cursor.close()
    db.close()
    top_authors_formated = "\n".join(['   {} - {} views'.format(x[0],x[1]) for x in top_authors])
    print(top_authors_formated)

def answer3():
    """Answer the third question """
    error_date_sql = """
        select * 
        from 
            (
                select sc.count::float/tc.count as error_rate, sc.date 
                from 
                    (
                        select total.date, count(*) 
                        from 
                            (
                                select to_char(time, 'Mon DD, YYYY') as date 
                                from log
                            ) total 
                        group by 1
                    ) tc, 
                    (
                        select success.date, count(*) 
                        from 
                            (
                                select to_char(time, 'Mon DD, YYYY') as date, status 
                                from log 
                                where status !='200 OK'
                            ) success 
                        group by 1 
                    ) sc 
                where sc.date = tc.date
            ) e 
        where e.error_rate > 0.01;"""
    print("Question 3: On which days did more than 1% of requests lead to errors?\n")    
    db, cursor = connect(DBNAME, USER)
    cursor.execute(error_date_sql)
    error_date = cursor.fetchall()
    cursor.close()
    db.close()
    error_date_fromated = '   {} - {}% error'.format(
        error_date[0][1],
        str(round(error_date[0][0]*100, 2))
        )
    print(error_date_fromated)

def run():
    """Running report ..."""
    print("Running reporting tools...\n")
    answer1()
    print("\n")
    
    answer2()
    print("\n")
    
    answer3()
    print("\n")

if __name__ == '__main__':
    run()
else:
    print('Importing')
