#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Data analysis from www.car.gr

author : pmav99
email : gmail, pmav99
license : GPL3
"""

import re
import sys
import sqlite3
import logging
import argparse
import datetime
from io import StringIO
from urllib.request import urlopen
from multiprocessing.dummy import Pool as ThreadPool

from bs4 import BeautifulSoup


# create a custom logging handler handler
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
handler.setLevel(logging.DEBUG)
handler.setFormatter(
    #logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logging.Formatter('%(asctime)s ; %(levelname)10s : %(message)s')
)

# setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class Database(object):
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.curs = self.conn.cursor()
        self.create_table()

    def create_table(self):
        sql = """
        CREATE TABLE data (
            id INTEGER PRIMARY KEY NOT NULL,
            description text NOT NULL,
            distance INTEGER NOT NULL,
            price INTEGER NOT NULL,
            age DATE NOT NULL
        ) """
        with self.conn:
            self.conn.execute(sql)

    def insert_data(self, data):
        sql = " INSERT INTO data (description, distance, price, age) VALUES (?, ?, ?, ?); "
        with self.conn:
            self.conn.executemany(sql, data)

    def fetchone(self, sql):
        self.curs.execute(sql)
        return self.curs.fetchone()[0]

    def fetchall(self, sql):
        self.curs.execute(sql)
        return self.curs.fetchall()

    def get_all(self):
        return self.fetchall("SELECT * FROM data")

    def get_average_price(self):
        avg = self.fetchone(" SELECT AVG(price) FROM data ")
        return avg

    def get_average_distance(self):
        avg = self.fetchone(" SELECT AVG(distance) FROM data ")
        return avg

    def get_average_age(self):
        avg = self.fetchone(" SELECT AVG(strftime('%Y', age)) AS YEAR FROM data ")
        return avg

    def _get_aggregate_per_year(self, aggregate, quantity, verbose=True):
        sql = """
        SELECT strftime('%Y', age) AS year, COUNT(id) AS cnt, {aggregate}({quantity})
        FROM data
        GROUP BY year
        ORDER BY year """.format(aggregate=aggregate, quantity=quantity)
        return self.fetchall(sql)

    def analyze(self):

        output = StringIO()

        output.write(
            "\n\nAnalysis\n========\n\n" +
            "General data\n" +
            "------------\n\n" +
            "The average price is: %.0f €.\n" % self.get_average_price() +
            "The average distance is: %.0f km.\n" % self.get_average_distance() +
            "The average manufacturing date is: %.0f.\n\n\n" % self.get_average_age()
        )

        avg_prices = self._get_aggregate_per_year("AVG", "price")
        min_prices = self._get_aggregate_per_year("MIN", "price")
        avg_distances = self._get_aggregate_per_year("AVG", "distance")
        min_distances = self._get_aggregate_per_year("MIN", "distance")

        rows = []
        text_row = "{year} | {cnt:5}     | {avg_price:7.0f} | {min_price:7.0f} | {avg_distance:7.0f} | {min_distance:7.0f}"
        for avg_price, min_price, avg_distance, min_distance in zip(avg_prices, min_prices, avg_distances, min_distances):
            rows.append(
                text_row.format(
                    year=avg_price[0], cnt=avg_price[1],
                    avg_price=avg_price[-1], min_price=min_price[-1],
                    avg_distance=avg_distance[-1], min_distance=min_distance[-1]
                )
            )

        output.write(
            "Yearly data\n\n" +
            "-----------\n" +
            "Year | # Records |     Price (€)     |   Distance (km)\n" +
            "     |           |   AVG   |   MIN   |   AVG   |   MIN    \n" +
            "--------------------------------------------------------\n" +
            "\n".join(rows)
        )

        text = output.getvalue()
        output.close()
        print(text)
        return text


def normalize_url(url):
    new_url = re.sub(r"(.*)&pg=[0-9]+(.*)", r"\1\2", url)
    new_url += "&pg={page}"
    if "&price-with=>" not in new_url:
        new_url += "&price-with=>1"
    return new_url


def get_soup(url, page_index=1):
    try:
        with urlopen(url) as response:
            logger.info("Retrieved page: %d", page_index)
            soup = BeautifulSoup(response.read())
            logger.info("Parsed page: %d", page_index)
            return soup
    except ValueError:
        logger.error("Are you sure this is a valid url? < %r > ", url)
        sys.exit(1)


def get_page_bikes(soup):
    bikes = []
    for i, ad in enumerate(soup.find_all("div", class_="clsfd_list_row_group")):
        text = [line.strip() for line in ad.text.splitlines() if line.strip()]
        # Not sure why javascript appears in text...
        if "googletag" in text[-1]:
            text.pop()
        description, distance, price, date = text[0], text[-2], text[-3], text[-5]
        # normalize data
        distance = int(float(distance[:-3]) * 1000) if "." in distance else int(distance[:-3])
        price = int(float(price[2:]) * 1000) if "." in price else int(price[2:])
        month, year = map(int, date.split("/"))
        year += 2000 if year < 20 else 1990
        if year > datetime.date.today().year:
            log.debug("Date in the future, skipping listing")
        date = datetime.date(year, month, 1)
        bikes.append((description, distance, price, date))
    return bikes


def get_last_page_number(soup):
    try:
        return int(soup.find("ul", class_="pagination pull-right").text.splitlines()[-2])
    except ValueError:
        return 2


def get_data(url):
    # We want to determine the urls of all the available pages.
    # In order to do so, we need to first parse the initial page.
    logger.info("Initial page retrieval")
    url = normalize_url(url)
    first_page_url = url.format(page=1)
    soups = [get_soup(first_page_url)]
    last_page = get_last_page_number(soups[0]) + 1
    urls = [url.format(page=i) for i in range(2, last_page)]
    indexes = [i for i in range(2, 2 + len(urls))]
    logger.info("There are %d pages available", len(urls) + 1)

    # Download and parse the rest of the pages
    # Since this is an I/O bound task we use threads
    pool = ThreadPool(options.threads)
    pool = ThreadPool(10)
    soups.extend(
        pool.starmap(get_soup, zip(urls, indexes))
    )
    pool.close()
    pool.join()

    # extract data
    # No real reason to do this one asynchronously too!
    data = []
    for soup in soups:
        data.extend(get_page_bikes(soup))
    return data


def parse_arguments():
    parser = argparse.ArgumentParser(
        description=__doc__.splitlines()[1],
        prog="car.gr analyzer",
        epilog="")

    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s ' + "0.1.0"
    )

    parser.add_argument(
        'url',
        action='store',
        help="A url from www.car.gr"
    )

    parser.add_argument(
        "-j", "--threads",
        dest="threads",
        action="store",
        type=int,
        default=4,
        help="number of threads to use when downloading pages. Defaults to 4",
    )

    options = parser.parse_args()
    return options


def main(options):
    data = get_data(options.url)
    db = Database()
    db.insert_data(data)
    db.analyze()

    # import pickle
    # # with open("data.pickle", "wb") as f:
    # #     pickle.dump(data, f)
    # with open("data.pickle", "rb") as f:
    #     data = pickle.load(f)

if __name__ == "__main__":
    options = parse_arguments()
    main(options)
