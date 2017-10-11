""" format_7_ho.py -- declares descriptor parser

    Language: Python 3
    Mark A. Caprio
    Patrick J. Fasano
    University of Notre Dame

    2/6/17 (pjf): Initiated (based on format_6_ho.py).
    10/10/17 (mac): Generalize filename format to allow for variable code name
        ("mfdn", "mfdn15", etc.).

"""

import re

# intra-package references
import mfdnres.descriptor

def parser(filename):
    """Parse results filename in format 7, restricted to the ho basis
    special case, but allowing for natural orbitals built on this basis.

    Args:
        filename (string) : filename (as basename)

    Returns:
        (dict) : info parsed from filename

    """

    regex = re.compile(
        # prolog
        r"run(?P<run>\w+)"
        r"\-(?P<code_name>[^\-]+)"
        r"\-(?P<descriptor>"
        # descriptor contents
        r"Z(?P<Z>\d+)\-N(?P<N>\d+)"
        r"\-(?P<interaction>[^\-]+)\-coul(?P<coulomb>\d)"
        r"\-hw(?P<hw>[\d\.]+)"
        r"\-a_cm(?P<lawson>[\d\.]+)"
        r"\-Nmax(?P<Nmax>\d+)(?P<mixed_parity_flag>x)?(?P<fci_flag>\-fci)?"
        r"\-Mj(?P<Mj>[\d\.]+)"
        r"\-lan(?P<lanczos>\d+)"
        r"\-tol(?P<tolerance>\d+\.\d+[eE][+-]\d+)"
        r"((?P<natural_orbital_flag>\-natorb)\-no(?P<natural_orbital_iteration>\d+))?"
        # epilog
        r").res"
    )

    conversions = {
        "Z" : int,
        "N" : int,
        "coulomb" : int,
        "hw" : float,
        "lawson" : float,
        "Nmax" : int,
        "mixed_parity_flag" : (lambda s  :  (s=="x")),
        "fci_flag" : (lambda s  :  (s=="-fci")),
        "Mj" : float,
        "lanczos" : int,
        "natural_orbital_flag" : (lambda s  :  (s=="-natorb")),
        "natural_orbital_iteration" : (lambda i  :  int(i) if (i is not None) else None)
        }

    match = regex.match(filename)
    if (match == None):
        raise ValueError("bad form for MFDn results filename")
    info = match.groupdict()

    # convert fields
    for key in conversions:
        conversion = conversions[key]
        info[key] = conversion(info[key])

    return info

mfdnres.descriptor.register_filename_format("format_7_ho",parser)

if (__name__ == "__main__"):

    filename = r"run0000-mfdn-Z2-N6-Daejeon16-coul1-hw05.000-a_cm20-Nmax02-Mj0.0-lan500-tol1.0e-06-natorb-no0.res"
    info = mfdnres.descriptor.parse_res_filename(filename,filename_format="format_7_ho")
    print(filename)
    print(info)

    filename = r"run0000-mfdn-Z2-N6-Daejeon16-coul1-hw05.000-a_cm20-Nmax02x-Mj0.0-lan500-tol1.0e-06.res"
    info = mfdnres.descriptor.parse_res_filename(filename,filename_format="format_7_ho")
    print(filename)
    print(info)

    filename = r"runpjf0015-mfdn15-Z3-N4-JISP16-coul1-hw20.000-a_cm40-Nmax02-Mj0.5-lan1000-tol1.0e-06-natorb-no0.res"
    info = mfdnres.descriptor.parse_res_filename(filename,filename_format="format_7_ho")
    print(filename)
    print(info)
