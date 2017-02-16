# coding=utf-8
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from bookr.app import app, query_db, get_db
from bookr.models import get_genres, generate_cities_played, generate_stream_info, get_offers, get_manager_bands, \
    get_venues, get_bands, check_band


@app.route('/add_technicians', methods=['POST'])
def add_technicians():
    """
    Updates the concerts with technicians as set by the organizer (or admin)
    :return: Re-renders the "my concerts" page
    """
    technicians = request.form['users']
    concert_id = request.form['concert_id']
    get_db().execute("UPDATE Concerts SET technicians=? WHERE id=?", (technicians, concert_id))
    g._database.commit()
    return redirect(url_for('concerts_mine'))


@app.route('/band_filter', methods=['POST'])
def band_filter():
    """
    Retrieves the information for the given band, and concerts they've played previously.

    A lot of duplicate code from the band_info page. Band_search is basically a mirror, except it has the functionality
    to choose which band you want to see the info of. Could be handled more elegantly, but discussions with the product
    owner led to this being the implementation.

    :return: Re-renders the "search for bands" page with the info of the given band
    """

    band_id = request.form['band_dropdown']

    band_info = query_db(
        'SELECT Bands.id, Bands.band_name, Bands.genre, Bands.price, Bands.email, Bands.tlf, Bands.requirements, '
        'Users.username, Bands.albums, Bands.albums_sold, Bands.playbacks, Bands.cities_played '
        'FROM Bands '
        'INNER JOIN Users ON Bands.manager=Users.id '
        'WHERE Bands.id = ?', (band_id,))[0]

    concerts = []
    for concert in query_db('SELECT Venues.venue_name, Offers.start_date, Offers.start_time, Offers.end_time, '
                            'Concerts.tickets_sold '
                            'FROM Concerts INNER JOIN Offers ON Concerts.offer=Offers.id '
                            'INNER JOIN Venues ON Offers.venue=Venues.id '
                            'WHERE Offers.band = ? AND Concerts.finished=1 ORDER BY Concerts.id DESC', (band_id,)):
        concerts.append(concert)

    return render_template("band_search.html", band_info=band_info, rows=concerts, bands=get_bands(),
                           retrieved=True)


@app.route('/band_handler', methods=['POST'])
def band_handler():
    """
    Registers a band and generates "data" from streaming services and the cities the band has played in. If a manager is
    registering the band, they get assigned as the manager for the band. An admin or booker gets to pick the manager.
    :return: Redirects to the main menu when finished.
    """
    error = None
    bandname = request.form['bandname'].title()
    genre = request.form['genre']
    requirements = request.form['reqs']
    tlf = request.form['tlf']
    price = request.form['price']
    mail = request.form['email']
    albums, playbacks, albums_sold = generate_stream_info()
    cities = generate_cities_played()
    if query_db('SELECT band_name FROM Bands WHERE band_name = ?', (bandname,)):
        error = "Bandet finnes allerede i databasen. Tenk kreativt!"
        return render_template("band_create.html", error=error, role=session.get('session_role'))
    role = session.get('session_role')
    if role in ('booker', 'admin'):
        manager = request.form['manager']
        get_db().execute('INSERT INTO Bands (band_name,genre,price,email,tlf,requirements,manager,albums,playbacks,'
                         'albums_sold,cities_played) '
                         'VALUES (?,?,?,?,?,?,?,?,?,?,?)', (bandname, genre, price, mail, tlf, requirements, manager,
                                                            albums, playbacks, albums_sold, cities))
        g._database.commit()
        return redirect(url_for('index'))
    if role == 'manager':
        username = session.get('session_username')
        username_id = query_db('SELECT Users.id FROM Users WHERE username=?', (username,))[0][0]
        get_db().execute(
            'INSERT INTO Bands (band_name,genre,price,email,tlf,requirements,manager,albums,playbacks,albums_sold,'
            'cities_played) '
            'VALUES (?,?,?,?,?,?,?,?,?,?,?)',
            (bandname, genre, price, mail, tlf, requirements, username_id, albums, playbacks, albums_sold, cities))
        g._database.commit()
        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.route('/confirm_offer', methods=['POST'])
def confirm_offer():
    """
    A manager confirms that the bands want to play on the concert as offered.
    :return: Updates database, re-renders page.
    """
    status = request.form['status']
    offer_id = request.form['id']

    if status == "confirmed":
        get_db().execute("INSERT INTO Concerts (offer) VALUES (?)", (offer_id,))
        ticket_price = query_db('SELECT Offers.message FROM Offers WHERE id=?', (offer_id,))[0][0]  # the hack is unreal
        get_db().execute("UPDATE Concerts SET ticket_price=? WHERE offer=?", (int(ticket_price), offer_id,))
        g._database.commit()

    get_db().execute("UPDATE Offers SET status=? WHERE id=?", (status, offer_id))
    g._database.commit()

    return redirect(url_for('offer_confirm'))


@app.route('/get_bands_by_parameter', methods=['POST'])
def get_bands_by_parameter():
    """
    Gets bands that have played a concert on a given venue
    :return: The "bands by venue" page, with more data
    """
    list_of_bands = []
    parameter = request.form['parameter']
    for band in query_db("SELECT Bands.id, Bands.band_name, Concerts.ticket_price, "
                         "Concerts.tickets_sold, Offers.start_time, Offers.start_date "
                         "FROM Concerts "
                         "INNER JOIN Offers ON Offers.id = Concerts.offer "
                         "INNER JOIN Bands ON Offers.band = Bands.id "
                         "WHERE Concerts.finished = ? AND Offers.venue = ?", (1, parameter)):
        list_of_bands.append(band)

    entries = get_venues()
    for entry in entries:
        if entry[0] is int(parameter):
            venue = entry[1]
    return render_template("bands_by_venue.html",
                           entries=entries, bands_by_venue=list_of_bands, venue=venue, retrieved=True)


@app.route('/get_concert_by_parameter', methods=['POST'])
def get_concert_by_parameter():
    """
    Gets finished and unfinished concerts of a given genre (genre is actually tied to the band that played though).
    :return: Re-renders the "concerts by genre" page with two lists of concerts
    """
    parameter = request.form['parameter']
    genres = get_genres()
    status = "1"
    status2 = "0"
    for tup in genres:
        if tup[0] == parameter:
            concert_finished = query_db('SELECT Venues.venue_name, Venues.capacity,Bands.band_name,Bands.price,'
                                        'Offers.start_time, Offers.end_time,Offers.start_date, '
                                        'Concerts.ticket_price,Concerts.tickets_sold '
                                        'FROM Concerts '
                                        'INNER JOIN Offers ON Concerts.offer = Offers.id '
                                        'INNER JOIN Bands ON Bands.id = Offers.band '
                                        'INNER JOIN Venues ON Venues.id = Offers.venue '
                                        'WHERE Bands.genre =? AND Concerts.finished =?', (parameter, status,))
            concert_unfinished = query_db('SELECT Venues.venue_name, Venues.capacity, Bands.band_name, '
                                          'Bands.price, Offers.start_time, Offers.end_time, Offers.start_date, '
                                          'Concerts.ticket_price, Concerts.tickets_sold '
                                          'FROM Concerts '
                                          'INNER JOIN Offers ON Concerts.offer = Offers.id '
                                          'INNER JOIN Bands ON Bands.id = Offers.band '
                                          'INNER JOIN Venues ON Venues.id = Offers.venue '
                                          'WHERE Bands.genre = ? AND Concerts.finished = ?', (parameter, status2,))
            return render_template("concerts_by_genre.html", genres=get_genres(), concert_finished=concert_finished,
                                   concert_unfinished=concert_unfinished, retrieved=True)


@app.route('/get_concerts_venue_filtered', methods=['POST'])
def get_concerts_venue_filtered():
    """
    Gets concerts that were played on a given venue
    :return: Redirects to "concerts by venue", with a list of finished concerts.
    """
    concerts = []
    venue = request.form['venues']
    for concert in query_db(
            'SELECT Concerts.id, Bands.band_name, Bands.genre, Venues.venue_name, Bands.price, '
            'Concerts.tickets_sold, Concerts.ticket_price '
            'FROM Concerts '
            'INNER JOIN Offers ON Concerts.offer=Offers.id '
            'INNER JOIN Bands ON Offers.band=Bands.id '
            'INNER JOIN Venues ON Offers.venue=Venues.id '
            'WHERE Concerts.finished = ? AND Venues.venue_name = ?', (1, venue)):
        concerts.append(concert)
    return render_template("concerts_by_venue.html", entries=get_venues(), concerts=concerts, retrieved=True)


@app.route('/pick_band', methods=['POST'])
def pick_band():
    """
    Gets the data of the band that the manager or admin chose
    :return: Re-renders the "edit band" page with the data of the chosen band
    """

    if request.method == "POST":
        band_id = request.form['band_id']
        manager_band = query_db('SELECT Bands.id, Bands.band_name, Bands.genre, Bands.requirements, Bands.price, '
                                'Bands.email, Bands.tlf '
                                'FROM Users '
                                'INNER JOIN Bands ON Bands.manager = Users.id '
                                'WHERE Bands.id = ?', (band_id,))[0]
        return render_template("band_edit.html", bands=get_manager_bands(), manager_band=manager_band)
    else:
        return render_template("band_edit.html", bands=get_manager_bands())


@app.route('/post_handler', methods=['POST'])
def post_handler():
    """
    Creates an offer in the database. Poorly named function in retrospect, considering the amount of "post handlers"
    we have in our code now.

    :return: Redirects to main menu when done
    """
    name = request.form['name']
    venue = request.form['venues']
    start = request.form['start_booking']
    end = request.form['end_booking']
    start_date = request.form['start_date']
    message = request.form['comment']
    get_db().execute(
        "INSERT INTO Offers (band, venue, start_time, end_time, message, start_date) VALUES (?,?,?,?,?,?)",
        (name, venue, start, end, message, start_date))
    g._database.commit()
    return redirect(url_for('index'))


@app.route('/review_offer', methods=['POST'])
def review_offer():
    """
    This one is really messy, but basically what's going on is that we're checking if the offer that the chief or admin
    accepted collides with another one that is already in the database. If so, we return an error. If all is good, the
    offer is accepted in the database and sent back to the booker, to be sent to the manager of the band.

    :return: Re-renders the "offer review" page, with an error if appropriate.
    """
    status = request.form['status']
    offer_id = request.form['id']
    ticket_price = request.form['ticket_price']
    # Assume no error (time conflict)
    error = ""

    if status == 'approved':
        c = query_db('SELECT * FROM Offers WHERE id=?', (offer_id,))[0]
        c_start = int(c[3][0:2])
        c_end = int(c[4][0:2]) if not int(c[4][0:2]) < c_start else int(c[4][0:2]) + 24
        # CHECK IF SCENE IS FREE AT THIS TIME
        concerts = []
        for concert in query_db(
                'SELECT * FROM Concerts '
                'INNER JOIN Offers ON Concerts.offer=Offers.id '
                'WHERE Offers.start_date = ? AND Offers.venue = ? AND Offers.id != ? ORDER BY id DESC',
                (c[5], c[2], offer_id)):
            concerts.append(concert)
        for concert in concerts:
            start = int(concert[12][0:2])
            end = int(concert[13][0:2]) if not int(concert[13][0:2]) < start else int(concert[13][0:2]) + 24
            if c_start in range(start, end):
                if not c[3] == concert[12] or int(c[3][3:5]) >= int(concert[11][3:5]):
                    error = "Det pågår en konsert på dette tidspunktet first"
            elif c_end in range(start, end):
                if not c[4] == concert[11] or int(c[4][3:5]) <= int(concert[11][3:5]):
                    error = "Det pågår en konsert på dette tidspunktet second"

        # SHOW ERROR IF TIME COLLISION - ACCEPT OFFER IF NOT
        if error:
            return render_template("offer_review.html", rows=get_offers("pending"), error=error)
        else:
            get_db().execute("UPDATE Offers SET status=? WHERE id=?", (status, offer_id))
            get_db().execute("UPDATE Offers SET message=? WHERE id=?", (ticket_price, offer_id))  # sorry for the hack.
            g._database.commit()
            return render_template("offer_review.html", rows=get_offers("pending"))
    else:
        get_db().execute("UPDATE Offers SET status=? WHERE id=?", (status, offer_id))
        g._database.commit()
        return render_template("offer_review.html", rows=get_offers("pending"))


@app.route('/send_offer', methods=['POST'])
def send_offer():
    """
    Sends an offer that has been approved by the chief to a bandmanager
    :return: Re-renders the "sent offers" page
    """
    status = request.form['status']
    offer_id = request.form['id']
    get_db().execute("UPDATE Offers SET status=? WHERE id=?", (status, offer_id))
    g._database.commit()
    return render_template("offer_sent.html", rows=get_offers("all"))


@app.route('/take_concert', methods=['POST'])
def take_concert():
    """
    Allows organizers to assign themselves to an available concert of their choice.
    :return: Sends the organizer or admin to the "my concerts" page.
    """
    concert_id = request.form['concert_id']
    username = session.get('session_username')
    get_db().execute("UPDATE Concerts SET organizer=? WHERE id=?", (username, concert_id))
    g._database.commit()
    return redirect(url_for('concerts_mine'))


@app.route('/update_band', methods=['POST'])
def update_band():
    """
    Form used for the "edit band" page. Updates the band with the new data, if it doesn't conflict with other bands.
    :return: Redirects to the main menu when done.
    """
    error = None
    band_id = request.form['band_id']
    new_band_name = request.form['bandname']
    new_band_name = new_band_name.title()
    if check_band(new_band_name, band_id):
        error = "Det finnes allerede ett band med det navnet. Tenk kreativt!"
        return render_template("band_edit.html", bands=get_manager_bands(), error=error)
    requirements = request.form['requirements']
    genre = request.form['genre']
    price = request.form['price']
    tlf = request.form['tlf']
    mail = request.form['mail']
    get_db().execute('UPDATE Bands SET band_name =?, requirements =?, genre =?,price =?,tlf =?,email=? WHERE id =?',
                     (new_band_name, requirements, genre, price, tlf, mail, band_id,))
    g._database.commit()
    return redirect(url_for('index'))
