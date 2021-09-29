"""prüft, ob Zeitfenster aktuell sind
"""

import datetime

from . import log

def set_date(now, begin, end):
    """ setzt das Datum auf das heutige Datum, bzw. falls der Endzeitpunkt am nächsten Tag ist, auf morgen

    Parameters
    ----------
    now : datetime
        aktuelles Datum und Uhrzeit
    begin : datetime
        Beginn des Zeitfensters
    end : datetime
        Ende des Zeitfensters

    Return
    ------
    begin, end: datetime
        Zeitfenster mit heutigen bzw. morgigen Datum
    """
    try:
        begin = begin.replace(now.year, now.month, now.day)
        end = end.replace(now.year, now.month, now.day)
        if begin > end:
            # Endzeit ist am nächsten Tag
            end = end + datetime.timedelta(days=1)
        return begin, end
    except Exception as e:
        log.exception_logging(e)
        return None, None


def is_timeframe_valid(now, begin, end):
    """ überprüft, ob das Zeitfenster des Ladeplans aktuell ist.

    Parameters
    ----------
    now : datetime
        aktuelles Datum und Uhrzeit
    begin : datetime
        Beginn des Zeitfensters
    end : datetime
        Ende des Zeitfensters

    Returns
    -------
    True : aktuell
    False : nicht aktuell
    """
    try:
        if ((now < begin) == False) and ((now < end) == True):
            return True
        else:
            return False
    except Exception as e:
        log.exception_logging(e)
        return False


def check_plans_timeframe(plans, hours=None):
    """ geht alle Pläne durch.

    Parameters
    ----------
    plans: dictionary
        Liste der Pläne, deren Zeitfenster geprüft werden sollen
    hours = None: int
        Stunden, die der Beginn vorher liegen soll; Werden keine Stunden angegeben, wird der Beginn dem Dictionary entnommen.

    Returns
    -------
    plan: erster aktiver Plan
    None: falls kein Plan aktiv ist
    """
    state = False
    try:
        for plan in plans:
            # Nur Keys mit Plannummer berücksichtigen
            try:
                if isinstance(plans[plan], dict) == True:
                    state = check_timeframe(plans[plan], hours)
                    if state == True:
                        return plan
            except:
                pass
        else:
            return None
    except Exception as e:
        log.exception_logging(e)
        return None


def check_timeframe(plan, hours):
    """ schaut, ob Plaene aktiv sind, prüft, ob das Zeitfenster aktuell ist.

    Parameters
    ----------
    plan: dictionary
        Plan dessen Zeitfenster geprüft werden soll
    hours = None: int
        Stunden, die der Beginn vorher liegen soll; Werden keine Stunden angegeben, wird der Beginn dem Dictionary entnommen.

    Returns
    -------
    True: Zeitfenster gültig
    False: Zeitfenster nicht gültig
    """
    state = None
    try:
        if plan["active"] == True:
            now = datetime.datetime.today()
            if hours == None:
                begin = datetime.datetime.strptime(plan["time"][0], '%H:%M')
                end = datetime.datetime.strptime(plan["time"][1], '%H:%M')
            else:
                end = datetime.datetime.strptime(plan["time"], '%H:%M')

            if plan["frequency"]["selected"] == "once":
                if hours == None:
                    beginDate = datetime.datetime.strptime(
                        plan["frequency"]["once"][0], "%y-%m-%d")
                    begin = begin.replace(
                        beginDate.year, beginDate.month, beginDate.day)
                    endDate = datetime.datetime.strptime(
                        plan["frequency"]["once"][1], "%y-%m-%d")
                else:
                    endDate = datetime.datetime.strptime(
                        plan["frequency"]["once"][0], "%y-%m-%d")
                    end = end.replace(
                        endDate.year, endDate.month, endDate.day)
                    begin = _calc_begin(end, hours)
                end = end.replace(
                    endDate.year, endDate.month, endDate.day)
                state = is_timeframe_valid(now, begin, end)

            elif plan["frequency"]["selected"] == "daily":
                if hours == None:
                    begin, end = set_date(now, begin, end)
                else:
                    end = end.replace(now.year, now.month, now.day)
                    # Wenn der Zeitpunkt an diesem Tag schon vorüber ist, nächsten Tag prüfen.
                    if end < now:
                        end += datetime.timedelta(days = 1)
                    begin = _calc_begin(end, hours)
                state = is_timeframe_valid(now, begin, end)

            elif plan["frequency"]["selected"] == "weekly":
                if hours == None:
                    if begin < end:
                        # Endzeit ist am gleichen Tag
                        if plan["frequency"]["weekly"][now.weekday()] == True:
                            begin, end = set_date(now, begin, end)
                            state = is_timeframe_valid(
                                now, begin, end)
                        else:
                            state = False
                    else:
                        if (plan["frequency"]["weekly"][now.weekday()] or plan["frequency"]["weekly"][now.weekday()+1]) == True:
                            begin, end = set_date(now, begin, end)
                            state = is_timeframe_valid(
                                now, begin, end)
                        else:
                            state = False
                else:
                    if plan["frequency"]["weekly"][now.weekday()] == True:
                        end = end.replace(
                            end.year, end.month, end.day)
                        begin = _calc_begin(end, hours)
                        state = is_timeframe_valid(
                            now, begin, end)
                    else:
                        state = False
    except Exception as e:
        log.exception_logging(e)
        return None
    return state


def _calc_begin(end, hours):
    """ berechnet den Zeitpunkt, der die angegebenen Stunden vor dem Endzeitpunkt liegt.

    Parameter
    ---------
    end: datetime
        Endzeitpunkt
    hours: int
        Stunden, die der Beginn vorher liegen soll

    Return
    ------
    datetime: berechneter Zeitpunkt
    """
    try:
        prev = datetime.timedelta(hours)
        return end - prev
    except Exception as e:
        log.exception_logging(e)
        return None

def check_duration(plan, duration):
    """ prüft, ob der in angegebene Zeitpunkt abzüglich der Dauer jetzt ist. 
    Um etwas Puffer zu haben, werden bei Überschreiten des Zeitpunkts die nachfolgenden 20 Min auch noch als Ladezeit zurückgegeben.

    Paramter
    --------
    plan : dictionary
        Plan, für den geprüft werden soll, ob mit der Ladung begonnen werden soll

    duration: float
        vorraussichtliche Ladedauer

    Return
    ------
    2, int: Zeitpunkt ist um mehr als 5 Min überschritten worden, verbleibende Zeit in h
    1, 0: Ladung sollte starten
    0, 0: hat noch Zeit
    """
    try:
        now = datetime.datetime.today()
        end = datetime.datetime.strptime(plan["time"], '%H:%M')

        if plan["frequency"]["selected"] == "once":
            endDate = datetime.datetime.strptime(
                plan["frequency"]["once"][0], "%y-%m-%d")
            end = end.replace(endDate.year, endDate.month, endDate.day)
            state, remaining_time = _is_duration_valid(now, duration, end)
            if -0.33 <= remaining_time < 0:
                remaining_time = remaining_time * -1
            elif remaining_time < -0.33:
                state = 0
                remaining_time = 0
            return state, remaining_time

        elif plan["frequency"]["selected"] == "daily":
            end = end.replace(now.year, now.month, now.day)
            # Wenn der Zeitpunkt an diesem Tag schon vorüber ist (verbleibende Zeit ist negativ), nächsten Tag prüfen.
            state, remaining_time = _is_duration_valid(now, duration, end)
            # Bis zwanzig Minuten nach Überschreiten des Zeitpunkts darf noch geladen werden.
            if -0.33 <= remaining_time < 0:
                remaining_time = remaining_time * -1
            elif remaining_time < -0.33:
                delta = datetime.timedelta(days = 1)
                end += delta
                state, remaining_time = _is_duration_valid(now, duration, end)
            return state, remaining_time
        elif plan["frequency"]["selected"] == "weekly":
            if plan["frequency"]["weekly"][now.weekday()] == True:
                end = end.replace(now.year, now.month, now.day)
                state, remaining_time = _is_duration_valid(now, duration, end)
                # Zeitpunkt ist an diesem Tag noch nicht vorbei
                if state == 1:
                    return state, remaining_time
                elif -0.33 <= remaining_time < 0:
                    remaining_time = remaining_time * -1
                else:
                # Wenn der Zeitpunkt an diesem Tag schon vorüber ist (verbleibende Zeit ist negativ), nächsten Tag prüfen.
                    delta = datetime.timedelta(days = 1)
                    end += delta
                    state, remaining_time = _is_duration_valid(now, duration, end)
                return state, remaining_time
            # prüfen, ob für den nächsten Tag ein Termin ansteht und heute schon begonnen werden muss
            if plan["frequency"]["weekly"][now.weekday()+1] == True:
                end = end.replace(now.year, now.month, now.day)
                delta = datetime.timedelta(days = 1)
                end += delta
                return _is_duration_valid(now, duration, end)
            else:
                return False, 0
    except Exception as e:
        log.exception_logging(e)
        return False


def _is_duration_valid(now, duration, end):
    """ prüft, ob der Endzeitpunkt der Ladung abzüglich der Ladedauer in den nächsten 5 Min liegt oder schon vorüber ist.

    Parameter
    ---------
    now: datetime
        aktuelles Datum und Uhrzeit

    duration: float 
        vorraussichtliche Ladedauer

    end: datetime
        Zeitpunkt, an dem die Ladung beendet sein soll

    Return
    ------
    2, int: Zeitpunkt ist um mehr als 5 Min überschritten worden, verbleibende Zeit in h
    1, 0: Ladung sollte starten
    0, 0: hat noch Zeit
    """
    try:
        delta = datetime.timedelta(
            hours=int(duration), minutes=((duration % 1)*60))
        begin = end - delta
        difference = (now - begin).total_seconds()
        if difference > 0:
            remaining_time = duration-(difference/3600)
            return 2, remaining_time
        elif difference > (-300):
            return 1, 0
        else:
            return 0, 0
    except Exception as e:
        log.exception_logging(e)
        return 1, 0


def is_list_valid(hourlist):
    """ prüft, ob eine der angegebenen Unix-Zeiten aktuell ist.

    Parameter
    ---------
    hourlist: list
        Liste mit Unix-Zeiten

    Return
    ------
    True: aktuelle Stunde ist in der Liste enthalten
    False: aktuelle Stunde ist nicht in der Liste enthalten
    """
    try:
        now = datetime.datetime.today()
        for hour in hourlist:
            timestamp = datetime.datetime.fromtimestamp(float(hour))
            if timestamp.hour == now.hour:
                return True
            else:
                return False
    except Exception as e:
        log.exception_logging(e)
        return False


def check_timestamp(timestamp, duration):
    """ prüft, ob der Zeitstempel innerhalb der angegebenen Zeit liegt

    Parameter
    ---------
    timestamp: str
        Zeitstempel, der geprüft werden soll
    duration:
        Zeitspanne in s, in der der Zeitstempel gültig ist

    Return
    ------
    True: Zeit ist noch nicht abgelaufen
    False: Zeit ist abgelaufen
    """
    try:
        stamp = datetime.datetime.strptime(timestamp, "%m/%d/%Y, %H:%M:%S")
        now = datetime.datetime.today()
        delta = datetime.timedelta(seconds=duration)
        if (now-delta) > stamp:
            return False
        else:
            return True
    except Exception as e:
        log.exception_logging(e)
        return True


def create_timestamp():
    """ erzeugt einen Zeitstempel mit dem aktuellen Datum und Uhrzeit

    Return
    ------
    str: aktuelles Datum und Uhrzeit
    """
    try:
        stamp = datetime.datetime.today().strftime("%m/%d/%Y, %H:%M:%S")
        return stamp
    except Exception as e:
        log.exception_logging(e)
        return None

def create_timestamp_YYYYMM():
    """ erzeugt einen Zeitstempel mit dem aktuellen Jahr und Monat

    Return
    ------
    str: aktuelles Datum
    """
    try:
        stamp = datetime.datetime.today().strftime("%Y%m")
        return stamp
    except Exception as e:
        log.exception_logging(e)
        return None

def create_timestamp_YYYYMMDD():
    """ erzeugt einen Zeitstempel mit dem aktuellen Jahr und Monat und Tag

    Return
    ------
    str: aktuelles Datum
    """
    try:
        stamp = datetime.datetime.today().strftime("%Y%m%d")
        return stamp
    except Exception as e:
        log.exception_logging(e)
        return None

def create_timestamp_time():
    """ erzeugt einen Zeitstempel mit der aktuellen Uhrzeit

    Return
    ------
    str: aktuelle Uhrzeit
    """
    try:
        stamp = datetime.datetime.today().strftime("%H:%M")
        return stamp
    except Exception as e:
        log.exception_logging(e)
        return None

def get_difference_to_now(timestamp_begin):
    """ ermittelt den Abstand zwischen zwei Zeitstempeln.

    Parameter
    ---------
    timestamp_begin: str %m/%d/%Y, %H:%M:%S
        Anfangszeitpunkt

    Return
    ------
    diff: str
        Differenz HH:MM, ggf DD days, HH:MM
    """
    try:
        begin = datetime.datetime.strptime(timestamp_begin[:-3], "%m/%d/%Y, %H:%M")
        now = datetime.datetime.today()
        diff = (now - begin)
        return str(diff)[:-10]
    except Exception as e:
        log.exception_logging(e)
        return 0

def get_difference(timestamp_begin, timestamp_end):
    """ ermittelt den Abstand zwischen zwei Zeitstempeln in Sekunden.

    Parameter
    ---------
    timestamp_begin: str %m/%d/%Y, %H:%M:%S
        Anfangszeitpunkt
    timestamp_end: str %m/%d/%Y, %H:%M:%S
        Anfangszeitpunkt

    Return
    ------
    diff: int
        Differenz in Sekunden
    """
    try:
        begin = datetime.datetime.strptime(timestamp_begin, "%m/%d/%Y, %H:%M:%S")
        end = datetime.datetime.strptime(timestamp_end, "%m/%d/%Y, %H:%M:%S")
        diff = (begin - end)
        return diff.total_seconds()
    except Exception as e:
        log.exception_logging(e)
        return 0

def duration_sum(first, second):
    """ addiert zwei Zeitstrings und gibt das Ergebnis als String zurück.

    Parameter
    ---------
    first, second: str
        Zeitstrings HH:MM ggf DD:HH:MM
    Return
    ------
    sum: str
        Summe der Zeitstrings
    """
    first = __get_timedelta_obj(first)
    second = __get_timedelta_obj(second)
    sum = first + second 
    return str(sum)

def __get_timedelta_obj(time):
    """ erstellt aus einem String ein timedelta-Objekt.

    Parameter
    ---------
    time: str
        Zeitstrings HH:MM ggf DD:HH:MM
    Return
    ------
    time: timedelta
    """
    time_charged = time.split(":")
    if len(time_charged) == 2:
        time = datetime.timedelta(hours=int(time_charged[0]), minutes=int(time_charged[1]))
    elif len(time_charged) == 3:
        time = datetime.timedelta(days=int(time_charged[0]), hours=int(time_charged[1]), minutes=int(time_charged[2]))
    return time