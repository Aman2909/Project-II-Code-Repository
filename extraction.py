"""
In fullfillment of Project Work - II
Aman Pathak
EN16CS301033
DATA SCIENCE INTERN
FEB-AUG 2020

COPYRIGHT : HVANTAGE TECHNOLOGIES
"""

import requests
import phonenumbers

DOCKER_URL = "http://localhost:8000/parse"
CONTENT_HEADER = {'content-type': 'application/x-www-form-urlencoded'}


def ispresent(extracted, answer_json):
    """
    Creates a key if not present earlier

    :param extracted: entity to check for
    :param answer_json: the output json
    :return: answer json
    """
    if extracted not in answer_json:
        answer_json[str(extracted)] = []
    return answer_json


def check_value(dictionary, entity_json):
    """

    :param dictionary: response
    :param entity_json: output json
    :return: entity_json
    """
    _ = {'day', 'month', 'week', 'month'}
    if dictionary['grain'] == 'day' or dictionary['grain'] == 'month' or dictionary['grain'] == 'week' or dictionary[
        'grain'] == 'year':
        # if dictionary['grain'] in _:
        # checks for grain=day/month/week/year
        entity_json = ispresent('date', entity_json)
        val = str(dictionary['value'])
        # converts the unicode type into sring type for further processing
        lst = val.split('T')[0]
        dateval = lst
        entity_json['date'].append(dateval)

        # [date(index value=0),time(index value=1)]

        if dictionary['grain'] == 'month':
            entity_json = ispresent('month', entity_json)
            monthval = lst.split('-')[1]
            entity_json['month'].append(monthval)
            return entity_json

        if dictionary['grain'] == 'year':
            entity_json = ispresent('year', entity_json)
            yearval = lst.split('-')[0]
            entity_json['year'].append(yearval)
            return entity_json
        return entity_json
        # nothing printed for grain=week

    elif dictionary['grain'] == 'hour' or dictionary['grain'] == 'minute' or dictionary['grain'] == 'second':
        # checks for grain=hour/minute/second
        # check for length
        if len(dictionary['values']) == 3:
            # checks if the length of values(list) inside the key=value is 3
            entity_json = ispresent('time', entity_json)
            val = str(dictionary['value'])
            timeval = val.split('T')[1]
            entity_json['time'].append(timeval)
            return entity_json
            # [date(index value=0),time(index value=1)]

        else:
            entity_json = ispresent('dateTime', entity_json)
            val = str(dictionary['value'])

            # [date(index value=0),time(index value=1)]

            datetime_val = val
            entity_json['dateTime'].append(datetime_val)
            return entity_json


def check_tofrom(dictionary, entity_json):
    """

    :param dictionary: response
    :param entity_json: entity_json
    :return: entity_json
    """
    if dictionary['to']['grain'] == 'day' or dictionary['to']['grain'] == 'month' or dictionary['to'][
        'grain'] == 'week' or dictionary['to']['grain'] == 'year':
        entity_json = ispresent('duration_bt_date', entity_json)
        val1 = str(dictionary['to']['value'])  # converts unicode to string type for further processing
        val2 = str(dictionary['from']['value'])  # converts unicode to string type for further processing
        start_val = val1.split('T')[0]
        end_val = val2.split('T')[0]
        duration_bt_date_val = {'start': start_val, 'end': end_val}
        entity_json['duration_bt_date'].append(duration_bt_date_val)

        if dictionary['to']['grain'] == 'month':  # [year(index value=0),month(index value=1),date(index value=2)]
            entity_json = ispresent('duration_bt_month', entity_json)
            month1 = start_val.split('-')[1]
            month2 = end_val.split('-')[1]
            duration_bt_month_val = {'start': month1, 'end': month2}
            entity_json['duration_bt_month'].append(duration_bt_month_val)
            return entity_json

        if dictionary['to']['grain'] == 'year':
            entity_json = ispresent('duration_bt_year', entity_json)
            year1 = start_val.split('-')[0]
            year2 = end_val.split('-')[0]
            duration_bt_year_val = {'start': year1, 'end': year2}
            entity_json['duration_bt_year'].append(duration_bt_year_val)
            return entity_json
        return entity_json
    elif dictionary['to']['grain'] == 'hour' or dictionary['to']['grain'] == 'minute' or dictionary['to'][
        'grain'] == 'second':
        if len(dictionary['values']) == 3:
            entity_json = ispresent('duration_bt_time', entity_json)
            val1 = str(dictionary['to']['value'])
            val2 = str(dictionary['from']['value'])
            startval = val1.split('T')[1]
            endval = val2.split('T')[1]
            # [date(index value=0),time(index value=1)]
            duration_bt_time_val = {'start': startval, 'end': endval}
            entity_json['duration_bt_time'].append(duration_bt_time_val)
            return entity_json
        else:
            entity_json = ispresent('duration_bt_dateTime', entity_json)
            startval = str(dictionary['to']['value'])
            endval = str(dictionary['from']['value'])
            duration_bt_datetime_val = {'start': startval, 'end': endval}
            entity_json['duration_bt_dateTime'].append(duration_bt_datetime_val)
            return entity_json
            # [date(index value=0),time(index value=1)]


def check_from(dictionary, entity_json):
    """

    :param dictionary: response
    :param entity_json: entity_json
    :return: entity_json
    """
    if dictionary['from']['grain'] == 'day' or dictionary['from']['grain'] == 'month' or dictionary['from'][
        'grain'] == 'week' or dictionary['from']['grain'] == 'year':
        entity_json = ispresent('date', entity_json)
        val = str(dictionary['from']['value'])
        lst = val.split('T')[0]
        dateval = lst
        entity_json['date'].append(dateval)

        if dictionary['from']['grain'] == 'month':
            # [year(index value=0),month(index value=1),date(index value=2)]
            entity_json = ispresent('month', entity_json)
            monthval = lst.split('-')[1]
            entity_json['month'].append(monthval)
            return entity_json

        elif dictionary['from']['grain'] == 'year':
            # [year(index value=0),month(index value=1),date(index value=2)]
            entity_json = ispresent('year', entity_json)
            yearval = lst.split('-')[0]
            entity_json['year'].append(yearval)
            # nothing printted for grain=week
            return entity_json
        return entity_json
    elif dictionary['from']['grain'] == 'hour' or dictionary['from']['grain'] == 'minute' or dictionary['from'][
        'grain'] == 'second':
        # check for length
        if len(dictionary['values']) == 3:
            entity_json = ispresent('time', entity_json)
            val = str(dictionary['from']['value'])
            lst = val.split('T')[1]  # [date(index value=0),time(index value=1)]
            timeval = lst
            entity_json['time'].append(timeval)
            return entity_json
        else:
            entity_json = ispresent('dateTime', entity_json)
            datetimeval = str(dictionary['from']['value'])
            entity_json['dateTime'].append(datetimeval)
            # [date(index value=0),time(index value=1)]
            return entity_json


def check_to(dictionary, entity_json):
    """

    :param dictionary: response
    :param entity_json: entity_json
    :return: entity_json
    """
    if dictionary['to']['grain'] == 'day' or dictionary['to']['grain'] == 'month' or dictionary['to'][
        'grain'] == 'week' or dictionary['to']['grain'] == 'year':
        entity_json = ispresent('date', entity_json)
        val = str(dictionary['to']['value'])
        lst = val.split('T')[0]
        dateval = lst
        entity_json['date'].append(dateval)

        if dictionary['to']['grain'] == 'month':
            # [year(index value=0),month(index value=1),date(index value=2)]
            entity_json = ispresent('month', entity_json)
            monthval = lst.split('-')[1]
            entity_json['month'].append(monthval)
            return entity_json
        elif dictionary['to']['grain'] == 'year':  # [year(index value=0),month(index value=1),date(index value=2)]
            entity_json = ispresent('year', entity_json)
            yearval = lst.split('-')[0]
            entity_json['year'].append(yearval)
            # nothing printted for grain=week
            return entity_json
        return entity_json

    elif dictionary['to']['grain'] == 'hour' or dictionary['to']['grain'] == 'minute' or dictionary['to'][
        'grain'] == 'second':
        # check for length
        if len(dictionary['values']) == 3:
            entity_json = ispresent('time', entity_json)
            val = str(dictionary['to']['value'])
            lst = val.split('T')[1]  # [date(index value=0),time(index value=1)]
            timeval = lst
            entity_json['time'].append(timeval)
            return entity_json
        else:
            entity_json = ispresent('dateTime', entity_json)
            datetimeval = str(dictionary['to']['value'])
            # [date(index value=0),time(index value=1)]
            entity_json['dateTime'].append(datetimeval)
            return entity_json


def parse_currency(entity_json, value_json):
    """
    Parses Currency
    :param entity_json: entity_json
    :param value_json: response
    :return: entity_json
    """
    entity_json = ispresent('currency', entity_json)
    if value_json['type'] == "interval":
        if 'to' in value_json and 'from' in value_json:
            money_json = {'currency_range':
                              {'to': {'value': value_json['to']['value'],
                                      'unit': value_json['to']['unit']},
                               'from': {'value': value_json['from']['value'],
                                        'unit': value_json['from']['unit']}
                               }
                          }
        elif 'to' in value_json:
            money_json = {'currency_range':
                              {'to': {'value': value_json['to']['value'],
                                      'unit': value_json['to']['unit']},
                               }
                          }
        else:
            money_json = {'currency_range':
                              {'from': {'value': value_json['from']['value'],
                                        'unit': value_json['from']['unit']}
                               }
                          }
    else:
        money_json = {'value': value_json['value'], 'unit': value_json['unit']}
    entity_json['currency'].append(money_json)
    return entity_json


def parse_ordinal(entity_json, value_json):
    """
    Parses Ordinal

    :param entity_json: entity_json
    :param value_json: response
    :return: entity_json
    """
    entity_json = ispresent('ordinal', entity_json)
    ordinal_json = value_json['value']
    entity_json['ordinal'].append(ordinal_json)
    return entity_json


def parse_url(entity_json, value_json):
    """
    Parses URL
    :param entity_json: entity_json
    :param value_json: response
    :return: entity_json
    """
    entity_json = ispresent('hyperlink', entity_json)
    hyperlink_json = value_json['value']
    entity_json['hyperlink'].append(hyperlink_json)
    return entity_json


def parse_quantity(entity_json, value_json):
    """
    Parses quantity
    :param entity_json: entity_json
    :param value_json: response
    :return: entity_json
    """
    entity_json = ispresent('quantity', entity_json)
    quantity_json = {"value": value_json['value'], "unit": value_json['unit'], }
    if 'product' in value_json:
        quantity_json['product'] = value_json['product']
    entity_json['quantity'].append(quantity_json)
    return entity_json


def parse_email(entity_json, value_json):
    """
    Parses email
    :param entity_json: entity_json
    :param value_json: response
    :return: entity_json
    """
    entity_json = ispresent('email', entity_json)
    email_json = value_json['value']
    entity_json['email'].append(email_json)
    return entity_json


def parse_phone_number(entity_json, value_list):
    """
    Parses phone number
    :param value_list: response
    :param entity_json: entity_json
    :return: entity_json
    """
    entity_json = ispresent('phone_number', entity_json)
    phone_number_json = {'country_code': value_list[0], 'national_number': value_list[1]}
    entity_json['phone_number'].append(phone_number_json)
    return entity_json


def isphone_number_check(ph_num):
    """
    Checks valid US phone number
    :param ph_num: phone number
    :return:
    """
    region = "US"
    a = phonenumbers.PhoneNumberMatcher(ph_num, region)
    if a.has_next():
        temp = str(a.next().number).split(' ')
        code, phone_number = temp[2], temp[5]
        return [code, phone_number]
    return False


def parse_number(entity_json, value_json):
    """
    Parses number
    :param entity_json: entity_json
    :param value_json: response
    :return: entity_json
    """
    entity_json = ispresent('number', entity_json)
    number = value_json['value']
    entity_json['number'].append(number)
    return entity_json


def compare(entity_json, entity_to_be_extracted):
    """
    Removes unwanted entities
    :param entity_json: entity_json
    :param entity_to_be_extracted: list of entities
    :return: entity_json
    """
    if entity_to_be_extracted[0] == 'all':
        # print(entity_json)
        return entity_json
    # entity_to_be_extracted = entity_to_be_extracted.split(',')
    to_remove = entity_json.keys() - set(entity_to_be_extracted)
    if to_remove:
        for i in to_remove:
            entity_json.pop(i)
    extras = set(entity_to_be_extracted) - entity_json.keys()
    if extras:
        for i in extras:
            entity_json.update({i: ''})
    return entity_json


def parser(text, entities_to_be_extracted):
    """
    Driver function
    :param text: Phrase of the user
    :param entities_to_be_extracted: entities required by user
    :return: entity_json
    """
    data_to_be_parsed = {'locale': 'en_GB', 'tz': 'Asia/Kolkata', 'text': text}
    entities_to_be_extracted = entities_to_be_extracted.split(',')
    response = requests.post(DOCKER_URL, data_to_be_parsed, CONTENT_HEADER)
    response_json = response.json()
    # print(json.dumps(response_json, indent=4))
    entity_json = {}
    is_phone = False
    for i in response_json:
        dimension = i['dim']
        # if dimension in entities_to_be_extracted or dimension == 'amount-of-money' or dimension == 'phone-number':
        if dimension == 'time':
            if 'value' in i['value']:
                check_value(i['value'], entity_json)

            elif 'to' in i['value'] and 'from' in i['value']:
                check_tofrom(i['value'], entity_json)

            elif 'from' in i['value'] and 'to' not in i['value']:
                check_from(i['value'], entity_json)

            elif 'to' in i['value'] and 'from' not in i['value']:
                check_to(i['value'], entity_json)

        elif dimension == 'amount-of-money':
            entity_json = parse_currency(entity_json, i['value'])

        elif dimension == 'quantity':
            entity_json = parse_quantity(entity_json, i['value'])

        elif dimension == 'email':
            entity_json = parse_email(entity_json, i['value'])

        elif dimension == 'url':
            entity_json = parse_url(entity_json, i['value'])

        elif dimension == 'ordinal':
            entity_json = parse_ordinal(entity_json, i['value'])

        elif dimension == 'phone-number':
            entity = i['value']['value']
            valid = isphone_number_check(entity)
            if valid:
                parse_phone_number(entity_json, valid)
                is_phone = entity

        elif dimension == 'number' and not is_phone == i['body']:
            entity_json = parse_number(entity_json, i['value'])
    else:
        pass

    entity_json = compare(entity_json, entities_to_be_extracted)
    entity = {'entities': entity_json}

    return entity


if __name__ == '__main__':
    parser("Let's meet at 8pm", 'all')
