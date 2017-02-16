# coding=utf-8
from collections import OrderedDict

from flask import session


def get_session():
    """
    Checks if the user in the session is logged in, has a username, and a role.
    :return: True if all is good, False if not.
    """
    if session.get('logged_in') is True:
        if session.get('session_username') is not None:
            if session.get('session_role') is not None:
                return True
    else:
        return False


def check_role(role):
    """
    Primarily used to gate access to views. Checks if a user is logged in, has a username, and role. Then checks if the
    role aligns to the ones who have access to the given view (admin or the role from the parameter).
    :param role: String-name of a role
    :return: Boolean depending on if it passed the check or not
    """
    return get_session() and session.get('session_role') in ('admin', role)


def get_sites(role):
    """
    This function is used for the main menu. The '/' index view calls this function to get the sites that the given user
    has access to. There's one big ordered dictionary, with keys that correspond to roles, and values that are also
    ordered subdictionaries.

    The subdictionaries have a key that is the name of the site, and a value that is used as a link to the site.

    :param role: The role of the user requesting sites for the main menu.
    :return: Ordered dictionary with an ordered subdictionary based on role. Admin gets all subdictionaries.
    """
    sites = OrderedDict()
    if role == 'chief' or role == 'admin':
        sites['Bookingsjef'] = OrderedDict()
        sites['Bookingsjef']['Tilbud'] = '/offer_review'
        sites['Bookingsjef']['Oversikt over tilbud'] = '/offer_history'
        sites['Bookingsjef']['Statistikk for booking'] = '/booking_stats'
        sites['Bookingsjef']['Økonomisk rapport'] = '/concerts_by_venue'

    if role == 'booker' or role == 'admin':
        sites['Bookingansvarlig'] = OrderedDict()
        sites['Bookingansvarlig']['Lag tilbud'] = '/offer_create'
        sites['Bookingansvarlig']['Tilbud sendt'] = '/offer_sent'
        sites['Bookingansvarlig']['Band etter scene'] = '/bands_by_venue'
        sites['Bookingansvarlig']['Konsert etter sjanger'] = '/concerts_by_genre'
        sites['Bookingansvarlig']['Registrer band'] = '/band_create'
        sites['Bookingansvarlig']['Søk etter band'] = '/band_search'

    if role == 'organizer' or role == 'admin':
        sites['Arrangør'] = OrderedDict()
        sites['Arrangør']['Ledige konserter'] = '/concerts_available'
        sites['Arrangør']['Mine konserter'] = '/concerts_mine'

    if role == 'technician' or role == 'admin':
        sites['Tekniker'] = OrderedDict()
        sites['Tekniker']['Mine jobber'] = '/technician'

    if role == 'manager' or role == 'admin':
        sites['Manager'] = OrderedDict()
        sites['Manager']['Registrer band'] = '/band_create'
        sites['Manager']['Rediger band'] = '/band_edit'
        sites['Manager']['Nye tilbud'] = '/offer_confirm'
    return sites
