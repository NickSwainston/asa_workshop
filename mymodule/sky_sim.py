#! /usr/bin/env python
"""
Determine Andromeda location in ra/dec degrees
"""

from random import uniform
from math import cos, sin, pi


NSRC = 1_000
RA = '00:42:44.3'
DEC = '41:16:09'


def get_radec():
    """
    Generate the ra/dec coordinates of Andromeda
    in decimal degrees.

    Returns
    -------
    ra : float
        The RA, in degrees, for Andromeda
    dec : float
        The DEC, in degrees for Andromeda
    """
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


def clip_to_radius(ra, dec, ras, decs):
    output_ras = []
    output_decs = []
    for ra_i, dec_i in zip(ras, decs):
        if (ra_i - ra)**2 + (dec_i - dec)**2 < 1:
            output_ras.append(ra_i)
            output_decs.append(dec_i)
    return output_ras, output_decs


def main():
    ra_deg, dec_deg = get_radec()
    ras, decs = make_stars(ra_deg, dec_deg)
    ras, decs = clip_to_radius(ra_deg, dec_deg, ras, decs)

    # now write these to a csv file for use by my other program
    with open('catalog.csv','w') as f:
        print("id,ra,dec", file=f)
        for i in range(len(ras)):
            print(f"{i:07d}, {ras[i]:12f}, {decs[i]:12f}", file=f)

