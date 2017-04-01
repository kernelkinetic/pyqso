#!/usr/bin/env python3

#    Copyright (C) 2017 Christian Thomas Jacobs.

#    This file is part of PyQSO.

#    PyQSO is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    PyQSO is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with PyQSO.  If not, see <http://www.gnu.org/licenses/>.

import logging

CABRILLO_VERSION = "3.0"


class Cabrillo:

    """ Write a list of records to a file in the Cabrillo format (v3.0).
    For more information, visit http://wwrof.org/cabrillo/ """

    def __init__(self):
        """ Initialise class for I/O of files using the Cabrillo format. """
        return

    def write(self, records, path):

        logging.debug("Writing records to an Cabrillo file...")
        try:
            f = open(path, mode='w', errors="replace")  # Open file for writing

            # Header
            f.write("""START-OF-LOG: %s\n""" % (CABRILLO_VERSION))
            f.write("""CREATED-BY: PyQSO v1.0.0\n""")

            # Write each record to the file.
            for r in records:

                # Frequency
                freq = r["FREQ"]

                # Mode
                if(r["MODE"] == "SSB"):
                    mo = "PH"
                elif(r["MODE"] == "CW"):
                    mo = "CW"
                elif(r["MODE"] == "FM"):
                    mo = "FM"
                else:
                    # FIXME: This assumes that the mode is any other non-CW digital mode, which isn't always going to be the case (e.g. for AM).
                    mo = "RY"

                # Date in yyyy-mm-dd format.
                date = r["QSO_DATE"][0:4] + "-" + r["QSO_DATE"][4:6] + "-" + r["QSO_DATE"][6:8]

                # Time
                time = r["TIME_ON"]

                # The callsign that was used when operating the contest station.
                call_sent = "TEST"

                # Exchange (the part sent to the distant station)
                exch_sent = r["RST_SENT"]

                # Callsign
                call_rcvd = r["CALL"]

                # Exchange (the part received from the distant station)
                exch_rcvd = r["RST_RCVD"]

                # Transmitter ID (must be 0 or 1, if applicable).
                # FIXME: For now this has been hard-coded to 0.
                t = "0"

                f.write("""QSO: %s %s %s %s %s %s %s %s %s\n""" % (freq, mo, date, time, call_sent, exch_sent, call_rcvd, exch_rcvd, t))

            # Footer
            f.write("END-OF-LOG:")

            f.close()

        except IOError as e:
            logging.error("I/O error %d: %s" % (e.errno, e.strerror))
        except Exception as e:  # All other exceptions.
            logging.error("An error occurred when writing the Cabrillo file.")
            logging.exception(e)

        return
