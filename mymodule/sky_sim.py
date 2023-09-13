#! /usr/bin/env python
"""
Determine Andromeda location in ra/dec degrees
"""

import argparse
from random import uniform
from math import cos, sin, pi
import logging

import mymodule


NSRC = 1_000
RA = '00:42:44.3'
DEC = '41:16:09'

def skysim_parser():
    """
    Configure the argparse for skysim

    Returns
    -------
    parser : argparse.ArgumentParser
        The parser for skysim.
    """
    parser = argparse.ArgumentParser(prog='sky_sim', prefix_chars='-', description="Simulate a sky")
    parser.add_argument('--version', action='version', version=f'%(prog)s {mymodule.__version__}')
    parser.add_argument('--ra', dest = 'ra', type=float, default=None,
                        help="Central ra (degrees) for the simulation location")
    parser.add_argument('--dec', dest = 'dec', type=float, default=None,
                        help="Central dec (degrees) for the simulation location")
    parser.add_argument('--out', dest='out', type=str, default='catalog.csv',
                        help='destination for the output catalog')
    parser.add_argument('--logging', type=str, default='INFO',
                        help='Logging level from (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
    return parser


def get_radec():
    # from wikipedia
    andromeda_ra = '00:42:44.3'
    andromeda_dec = '41:16:09'

    d, m, s = andromeda_dec.split(':')
    dec = int(d)+int(m)/60+float(s)/3600

    h, m, s = andromeda_ra.split(':')
    ra = 15*(int(h)+int(m)/60+float(s)/3600)
    ra = ra/cos(dec*pi/180)
    return ra,dec


def make_stars(ra, dec, nsrc=NSRC):
    """
    Generate NSRC stars within 1 degree of the given ra/dec

    Parameters
    ----------
    ra,dec : float
        The ra and dec in degrees for the central location.
    nsrc : int
        The number of star locations to generate

    Returns
    -------
    ras, decs : list
        A list of ra and dec coordinates.
    """
    ras = []
    decs = []
    for _ in range(nsrc):
        ras.append(ra + uniform(-1,1))
        decs.append(dec + uniform(-1,1))
    return ras, decs


def clip_to_radius(ra, dec, ras, decs, log=logging.getLogger("<my module>")):
    output_ras = []
    output_decs = []
    for ra_i, dec_i in zip(ras, decs):
        log.debug(f"Checking {ra_i} {dec_i}")
        log.debug(f"Distance {(ra_i - ra)**2 + (dec_i - dec)**2}")
        if (ra_i - ra)**2 + (dec_i - dec)**2 < 1:
            log.debug("Within 1 degree")
            output_ras.append(ra_i)
            output_decs.append(dec_i)
    return output_ras, output_decs


def main():
    parser = skysim_parser()
    options = parser.parse_args()
    loglevels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    logging.basicConfig(
        format="%(name)s:%(levelname)s %(message)s",
        level=loglevels[options.logging]
    )
    log = logging.getLogger("sky_sim")

    # if ra/dec are not supplied the use a default value
    if None in [options.ra, options.dec]:
        log.debug("No ra/dec specified, using Andromeda")
        ra_deg, dec_deg = get_radec()
    else:
        ra_deg = options.ra
        dec_deg = options.dec
        log.debug(f"Using ra/dec {ra_deg} {dec_deg}")

    log.info(f"Making {NSRC} stars")
    ras, decs = make_stars(ra_deg, dec_deg)
    log.info("Clipping to 1 degree radius")
    ras, decs = clip_to_radius(ra_deg, dec_deg, ras, decs, log=log)
    log.info(f"Found {len(ras)} stars within 1 degree of {ra_deg} {dec_deg}")

    # now write these to a csv file for use by my other program
    with open(options.out,'w') as f:
        print("id,ra,dec", file=f)
        for i in range(len(ras)):
            print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}", file=f)
    log.info(f"Wrote {options.out}")

