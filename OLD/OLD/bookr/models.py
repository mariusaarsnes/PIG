#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
from datetime import date, datetime

from flask import g
from flask import session

from bookr.app import query_db, get_db


def check_band(band_name, band_id):
    """
    Checks if a band of the given name already exists in the database.

    :param band_name: Name of a band
    :param band_id: ID of a band
    :return: True if the band already exists, false if not.
    """
    if not query_db('SELECT Bands.id FROM Bands WHERE Bands.band_name IS ? AND Bands.id IS NOT ?',
                    (band_name, band_id)):
        return False
    else:
        return True


def generate_cities_played():
    """
    Generates a "list" of major cities that a band has supposedly played in previously.

    :return: A comma-separated string of cities
    """
    cities = ['Oslo', 'Bergen', 'Stavanger', 'Trondheim', 'Drammen', 'Fredrikstad']
    cities_chosen = []
    city_amount = random.randint(0, 3)
    for x in range(city_amount):
        random.shuffle(cities)
        cities_chosen.append(cities.pop())
    cities_chosen.sort()
    city_string = ', '.join(cities_chosen)
    return city_string


def generate_stream_info():
    """
    Generates info that is supposed to come from streaming services, but the data is fake for the project, as the
    product owner didn't feel a need to get actual data.

    :return: Amount of albums the band has made, amount of total playbacks, and amount of albums sold.
    """
    albums = random.randint(1, 10)
    playbacks = 0
    for x in range(1, albums, 1):
        playbacks += random.randint(500, 5000) * x ^ 2
    albums_sold = playbacks / albums
    return int(albums), int(playbacks), int(albums_sold)


def generate_visitors(venue):
    """
    Generates a random amount of visitors for a concert between half and full capacity of the given venue
    :param venue: ID of a venue
    :return: The generated amount of visitors
    """
    full_capacity = query_db('SELECT Venues.capacity FROM Venues WHERE id =?', (venue,))[0][0]
    half_capacity = full_capacity / 2
    visitors = random.randint(half_capacity, full_capacity)
    return visitors


def get_available_managers():
    """
    Gets all managers from the database
    :return: List of managers
    """
    managers = query_db('SELECT Users.id, Users.username FROM Users WHERE role = "manager"')
    return managers


def get_bands():
    """
    Retrieves basic information on bands from the database
    :return: The ID and band name of every band
    """
    bands = query_db('SELECT id,band_name FROM Bands')
    return bands


def get_concerts():
    """
    Gets all information from all concerts, and then some. Joins concerts and offers together, as we have a lot of
    relevant data for concerts in the offers table to avoid duplicates.
    :return: A list of data
    """
    concerts = []
    for concert in query_db(
            'SELECT * FROM Concerts '
            'INNER JOIN Offers ON Concerts.offer=Offers.id '
            'ORDER BY Concerts.id DESC'):
        concerts.append(concert)
    return concerts


def get_concerts_mine(organizer):
    """
    Get data from concerts that is assigned to the given organizer
    :param organizer: Username of the admin or organizer that is logged in
    :return: A list of concerts, with some more fields from offers, bands and venues.
    """
    concerts = []
    for concert in query_db(
            'SELECT * FROM Concerts '
            'INNER JOIN Offers ON Concerts.offer=Offers.id '
            'INNER JOIN Bands ON Offers.band=Bands.id '
            'INNER JOIN Venues ON Offers.venue=Venues.id WHERE Concerts.organizer = ? AND Concerts.finished=0 '
            'ORDER BY id DESC',
            (organizer,)):
        concerts.append(concert)
    return concerts


def get_days_left():
    """
    Calculates number of days between today and end of semester. End of semester is hard-coded in, but considering the
    circumstances of the project, there's not much point to making a more dynamic function.

    :return: Amount of days until end of semester
    """
    now = date.today()
    end_semester_fall = date(2016, 12, 31)
    end_semester_spring = date(2017, 6, 22)
    if now > end_semester_fall:
        delta = end_semester_spring - now
    else:
        delta = end_semester_fall - now
    return delta.days


def get_days_left_scene(scene_id):
    """
    Takes the total amount of days left in the semester, minus all "taken" days, aka. those that have a concert booked.
    The function isn't super intuitively named, considering renaming.

    :param scene_id: ID of a venue
    :return: Amount of available dates for a given venue
    """
    counter = 0
    confirmed_dates = get_offers('confirmed')
    duplicate_dates = []            # duplicate_dates allows for multiple concerts on the same scene on
    for row in confirmed_dates:     # the same day without messing up statistics
        if row[2] == scene_id and not row[5] in duplicate_dates:
            duplicate_dates.append(row[5])
            counter += 1
    return get_days_left() - counter


def get_days_taken_scene(scene_id):
    """
    Gets the dates that have a booked concert on them
    :param scene_id: ID of a venue
    :return: A string of dates separated by comma
    """
    taken_dates = []
    confirmed_dates = get_offers('confirmed')
    for row in confirmed_dates:
        if row[2] == scene_id:
            if row[5] not in taken_dates:
                taken_dates.append(row[5])
    return ', '.join(taken_dates) if taken_dates else ""


def get_free_concerts():
    """
    Get data from concerts that don't have an organizer assigned to them.
    :return: A list of concerts, with some more fields from offers, bands and venues.
    """
    concerts = []
    for concert in query_db(
            'SELECT * FROM Concerts '
            'INNER JOIN Offers ON Concerts.offer=Offers.id '
            'INNER JOIN Bands ON Offers.band=Bands.id '
            'INNER JOIN Venues ON Offers.venue=Venues.id WHERE Concerts.organizer = ? AND Concerts.finished=0 '
            'ORDER BY id DESC',
            (-1,)):
        concerts.append(concert)
    return concerts


def get_genres():
    """
    In theory, this function returns a list of the database-recognized genres, but the actual function just gets all
    distinct genres from the bands we have in the database. So, someone could add a new genre by just modifying the
    database. The site doesn't let you put in anything other than the genres in the <select> from the HTML though.
    It's kind of a hack.

    :return: A list of genres
    """
    genres = query_db('SELECT DISTINCT Bands.genre FROM Bands')
    return genres


def get_manager_bands():
    """
    Admin is "assigned" to all bands. This is becayse this function is used to get a list of bands that the user can
    choose to edit the information of. So, it makes sense that managers only edit their own bands, and admins edit all.
    :return: A list of bands that the manager or admin is assigned to.
    """
    manager_name = session.get('session_username')
    if session.get('session_role') == 'admin':
        manager_band = query_db('SELECT Bands.id,Bands.band_name FROM Users '
                                'INNER JOIN Bands ON Bands.manager = Users.id')
        return manager_band
    else:
        manager_band = query_db('SELECT Bands.id,Bands.band_name FROM Users '
                                'INNER JOIN Bands ON Bands.manager = Users.id '
                                'WHERE Users.username = ?', (manager_name,))
        return manager_band


def get_offers(status):
    """
    Gets offers from the database depending on the value of status

    Ideally we wouldn't use SELECT * at all, but we learned that late in the project.
    Also, changing this specific function would be a living nightmare considering how much depends on it.

    :param status: A filtering value, to decide which offers we want to get.
    :return: A list of offers that correspond to the filter
    """
    offers = []
    if status == "all":
        for offer in query_db(
                'SELECT * FROM Offers '
                'INNER JOIN Bands ON Offers.band=Bands.id '
                'INNER JOIN Venues ON Offers.venue=Venues.id ORDER BY id DESC'):
            offers.append(offer)
    else:
        for offer in query_db(
                                'SELECT * FROM Offers '
                                'INNER JOIN Bands ON Offers.band=Bands.id '
                                'INNER JOIN Venues ON Offers.venue=Venues.id '
                                'WHERE Offers.status="' + status + '" ORDER BY id DESC'):
            offers.append(offer)
    return offers


def get_technicians():
    """
    Gets the names (usernames) of all technicians in the database
    :return: List of technician usernames
    """
    techs = []
    for tech in query_db('SELECT * FROM Users WHERE role="technician" ORDER BY username DESC'):
        techs.append(tech)
    return techs


def get_user_technician():
    """
    Retrieves every concert in the database, then filters down to concerts that the technician is assigned to
    :return: A list of concerts the tecnician is assigned to
    """
    technician_user = session['session_username']
    my_concerts = []
    for concert in query_db('SELECT id, technicians FROM Concerts'):
        current = concert[1].split(',')
        try:
            if technician_user in current:
                my_concerts.append(concert[0])
        except TypeError:
            pass

    if my_concerts:
        concerts_sql = ""
        for concert in my_concerts:
            concerts_sql += "Concerts.id=" + str(concert) + " OR "
        concerts_sql = concerts_sql[:-3]
        concerts = []
        for concert in query_db('SELECT * FROM Concerts '
                                'INNER JOIN Offers ON Concerts.offer=Offers.id '
                                'INNER JOIN Bands ON Offers.band=Bands.id '
                                'INNER JOIN Venues ON Offers.venue=Venues.id '
                                'WHERE ' + concerts_sql + ' AND Concerts.finished=0 ORDER BY id DESC'):
            concerts.append(concert)
        return concerts
    else:
        return []


def get_venues():
    """
    Gets all the data from all venues in the database
    :return: A list of venue data
    """
    venues = []
    for venue in query_db('SELECT * FROM Venues'):
        venues.append(venue)
    return venues


def process_concerts():
    """
    This is a weird one.
    First of all, it sets all offers that are past the start-date of the booking to be declines.
    Second, it updates concerts that were prior to today to be finished and fills in the tickets that were sold.
    Third, it goes through all future concerts and reassures that they are not finished, and have no tickets sold yet.

    The function is called very irregularly, and really the whole thing should be rewritten.

    :return: Doesn't return a whole lot of anything.
    """
    status = "0"
    today = datetime.today().date()
    all_start_dates = query_db('SELECT Concerts.id,Offers.start_date,Offers.venue FROM Concerts '
                               'INNER JOIN Offers ON Concerts.offer = Offers.id '
                               'WHERE Concerts.finished =?', status)
    all_expired_offers = query_db('SELECT Offers.start_date,Offers.id FROM Offers WHERE Offers.status ="pending"')
    for offer in all_expired_offers:
        date_of_offer = offer[0]
        date_of_offer_date_object = datetime.strptime(date_of_offer, "%Y-%m-%d").date()
        if date_of_offer_date_object < today:
            get_db().execute("UPDATE Offers SET status=? WHERE id=?", ("declined", offer[1]))
            g._database.commit()
        else:
            pass
    for concert in all_start_dates:
        status = "1"
        date_of_concert = concert[1]
        date_of_concert_date_object = datetime.strptime(date_of_concert, "%Y-%m-%d").date()
        if date_of_concert_date_object < today:
            visitors = generate_visitors(concert[2])
            get_db().execute("UPDATE Concerts SET finished=?,tickets_sold =? WHERE id=?",
                             (status, visitors, concert[0],))
            g._database.commit()
        if date_of_concert_date_object > today:
            status = "0"
            tickets = "0"
            get_db().execute("UPDATE Concerts SET finished=?,tickets_sold =? WHERE id=?",
                             (status, tickets, concert[0],))
            g._database.commit()
        else:
            pass
