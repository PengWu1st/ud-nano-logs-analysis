import psycopg2

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

top4_authors_sql = """
    select au.name, count(*)
    from authors as au, articles as ar, log as l
    where au.id = ar.author
    and ar.slug = overlay(l.path placing '' from 1 for 9)
    group by au.name
    order by 2 desc;"""

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

conn = psycopg2.connect("dbname=news user=vagrant")
cur = conn.cursor()
cur.execute(top3_articles_sql)
top3_articles = cur.fetchall()
cur.execute(top4_authors_sql)
top4_authors = cur.fetchall()
cur.execute(error_date_sql)
error_date = cur.fetchall()
cur.close()
conn.close()

top3_articles_formated = "\n    ".join(['"{}" - {} views'.format(x[0],x[1]) for x in top3_articles])

top4_authors_formated = "\n    ".join(['{} - {} views'.format(x[0],x[1]) for x in top4_authors])

error_date_fromated = '{} - {}% error'.format(
    error_date[0][1],
    str(round(error_date[0][0]*100, 2))
    )

print(
    """
most popular three articles of all time:
    {}

most popular authors of all time:
    {}

more than 1 percent of requests lead to errors:
    {}

    """.format(top3_articles_formated,top4_authors_formated,error_date_fromated)
)
