from datetime import datetime, date

from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from bookr.app import app, query_db
from bookr.models import get_genres, get_offers, get_manager_bands, get_venues, get_free_concerts, get_technicians, \
    get_concerts_mine, get_days_left_scene, get_days_taken_scene, get_days_left, get_bands, get_user_technician, \
    process_concerts, get_available_managers
from bookr.validation import get_session, check_role, get_sites


@app.errorhandler(405)
def method_not_allowed(e):
    """
    This is to prevent people from manually navigating to our form actions. When they try to GET a route that only takes
    POST methods, they get sent to this error handler. If they did it while logged in, they get thrown back to the
    main menu, if not, they get thrown to the login page.

    Should maybe be in a different file.

    :param e: Exception/error. We don't use it, but Flask is very displeased if we don't include it as an argument.
    :return: Redirect to main menu or login page.
    """
    if get_session():
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))


@app.route('/')
def index():
    """
    This is the view for the main menu, given that you're logged in.
    :return: Main menu
    """
    if get_session():
        sites = get_sites(session.get('session_role'))
        return render_template('menu.html', sites=sites)
    else:
        return redirect(url_for('login'))


@app.route('/band_create')
def band_create():
    """
    We check role here because the create band page adapts to whether or not you're a manager.
    :return: Create band page
    """
    if check_role('manager') or check_role('booker'):
        role = session.get('session_role')
        return render_template("band_create.html", role=role, managers=get_available_managers())
    else:
        return redirect(url_for('login'))


@app.route('/band_edit')
def band_edit():
    if check_role('manager'):
        return render_template("band_edit.html", bands=get_manager_bands())
    else:
        return redirect(url_for('login'))


@app.route('/band_info')
def band_info():
    """
    Retrieves the information for the given band, and concerts they've played previously.
    Only have docstring here because there's some data-retrieval here that really should've been handled elsewhere.

    :return: Band info page
    """
    if check_role('booker'):

        band_id = request.args.get('band')
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
                                'WHERE Offers.band = ? AND Concerts.finished=1 ORDER BY Concerts.id DESC',
                                (band_id,)):
            concerts.append(concert)

        return render_template("band_info.html", band_info=band_info, rows=concerts)
    else:
        return redirect(url_for('login'))


@app.route('/band_search')
def band_search():
    if check_role('booker'):
        return render_template("band_search.html", bands=get_bands())
    else:
        return redirect(url_for('login'))


@app.route('/bands_by_venue')
def bands_by_venue():
    if check_role('booker'):
        return render_template("bands_by_venue.html", entries=get_venues())
    else:
        return redirect(url_for('login'))


@app.route('/booking_stats')
def booking_stats():
    """
    This one is kinda hacky. Gets data for every venue, one by one.
    :return: The page for booking stats, along with a lot of stats.
    """
    if check_role('chief'):
        return render_template("booking_stats.html", rows_accepted=get_offers("confirmed"),
                               entries=get_offers("all"), days_left=get_days_left(),
                               strossa=get_days_left_scene(1), storsalen=get_days_left_scene(2),
                               selskapssiden=get_days_left_scene(3),
                               rundhallen=get_days_left_scene(4),
                               lyche=get_days_left_scene(5), knaus=get_days_left_scene(6),
                               klubben=get_days_left_scene(7), edgar=get_days_left_scene(8),
                               daglighallen=get_days_left_scene(9),
                               bodegaen=get_days_left_scene(10),
                               strossa_taken=get_days_taken_scene(1),
                               storsalen_taken=get_days_taken_scene(2),
                               selskapssiden_taken=get_days_taken_scene(3),
                               rundhallen_taken=get_days_taken_scene(4),
                               lyche_taken=get_days_taken_scene(5), knaus_taken=get_days_taken_scene(6),
                               klubben_taken=get_days_taken_scene(7), edgar_taken=get_days_taken_scene(8),
                               daglighallen_taken=get_days_taken_scene(9),
                               bodegaen_taken=get_days_taken_scene(10))
    else:
        return redirect(url_for('login'))


@app.route('/concerts_available')
def concerts_available():
    if check_role('organizer'):
        username = session.get('session_username')
        return render_template("concerts_available.html", entries=get_free_concerts(), technicians=get_technicians(),
                               organizer=username)
    else:
        return redirect(url_for('login'))


@app.route('/concerts_by_genre')
def concerts_by_genre():
    if check_role('booker'):
        process_concerts()
        return render_template("concerts_by_genre.html", genres=get_genres())
    else:
        return redirect(url_for('login'))


@app.route('/concerts_by_venue')
def concerts_by_venue():
    if check_role('chief'):
        process_concerts()
        return render_template("concerts_by_venue.html", entries=get_venues())
    else:
        return redirect(url_for('login'))


@app.route('/concerts_mine')
def concerts_mine():
    if check_role('organizer'):
        username = session.get('session_username')
        return render_template("concerts_mine.html", entries=get_concerts_mine(username), technicians=get_technicians(),
                               organizer=username)
    else:
        return redirect(url_for('login'))


@app.route('/offer_confirm')
def offer_confirm():
    """
    Some logic here that probably doesn't belong in the view itself. Gets the offers that have been sent from the
    booker/chief, limited only to the offers sent to the bands the manager is assigned to.

    Admin can see all offers, no matter the manager.

    :return: A manager page along with all new offers for the manager to accept
    """
    if check_role('manager'):
        manager_id = session.get('session_username')
        offers = []
        if check_role('admin'):
            for offer in query_db(
                    'SELECT * FROM Offers '
                    'INNER JOIN Bands ON Offers.band=Bands.id '
                    'INNER JOIN Users ON Bands.manager=Users.id '
                    'INNER JOIN Venues ON Offers.venue=Venues.id WHERE Offers.status="accepted" '
                    'ORDER BY id DESC'):
                offers.append(offer)
        else:
            for offer in query_db(
                    'SELECT * FROM Offers '
                    'INNER JOIN Bands ON Offers.band=Bands.id '
                    'INNER JOIN Users ON Bands.manager=Users.id '
                    'INNER JOIN Venues ON Offers.venue=Venues.id WHERE Offers.status="accepted" '
                    'AND Users.username=? ORDER BY id DESC', (manager_id,)):
                offers.append(offer)
        for offer in offers:
            if datetime.strptime(offer[5], "%Y-%m-%d").date() < datetime.today().date():
                offers.remove(offer)
        print(offers)
        return render_template("offer_confirm.html", rows=offers)
    else:
        return redirect(url_for('login'))


@app.route('/offer_create')
def offer_create():
    if check_role('booker'):
        return render_template("offer_create.html", entries=get_venues(), bands=get_bands(),
                               today=date.today())
    else:
        return redirect(url_for('login'))


@app.route('/offer_history')
def offer_history():
    if check_role('chief'):
        return render_template("offer_history.html", rows=get_offers("all"))
    else:
        return redirect(url_for('login'))


@app.route('/offer_review')
def offer_review():
    if check_role('chief'):
        return render_template("offer_review.html", rows=get_offers("pending"))
    else:
        return redirect(url_for('login'))


@app.route('/offer_sent')
def offer_sent():
    if check_role('booker'):
        return render_template("offer_sent.html", rows=get_offers("all"))
    else:
        return redirect(url_for('login'))


@app.route('/technician')
def technician():
    if check_role('technician'):
        return render_template("technician.html", concerts=get_user_technician())
    else:
        return redirect(url_for('login'))
