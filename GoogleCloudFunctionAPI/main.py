import functions_framework


@functions_framework.http
def get_info(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    request_json = request.get_json(silent=True)
    request_args = request.args

    import requests
    import pycountry as pyc
    import pandas as pd
    import numpy
    import flask
    from flask import jsonify

    if request_json and 'country' in request_json:
        countryReq = request_json['country']
    elif request_args and 'country' in request_args:
        countryReq = request_args['country']
    else:
        return jsonify({"status": 0})

    indicators = ['SH.STA.MMRT', 'SE.PRM.TENR.FE', 'SE.ADT.LITR.FE.ZS', 'SG.DMK.SRCR.FN.ZS']
    indicatorLabels = ['maternalMortality', 'womenSecondaryEducation', 'femaleAdultLiteracy', 'reproductiveAutonomy']
    indicatorFactor = [100000, 100, 100, 100]
    response = {
        "status": 2
    }

    try:
        country = pyc.countries.search_fuzzy(countryReq)[0]
    except LookupError:
        return jsonify({"status": 1})
    else:
        print(country)
        #########################
        # TRAVEL ADVISORY API
        #########################
        # extract json info for the country we care about
        trav_url = "https://www.travel-advisory.info/api?countrycode=" + str(
            country.alpha_2)  # concatenates url and country code
        trav_ad_json = requests.get(trav_url).json()  # extracts json from this url containing country of interest

        # pull score if sources_active > 0
        if trav_ad_json['data'][str(country.alpha_2)]['advisory']['sources_active'] > 0:  # if more than one source
            response["travel_adv"] = (trav_ad_json['data'][str(country.alpha_2)]['advisory']['score']) / 5

        else:
            response["travel_adv"] = None
        for count, indicator in enumerate(indicators):
            responseData = requests.get(
                'https://api.worldbank.org/v2/country/' + country.alpha_3 + '/indicator/' + indicator + '?format=json').json()
            try:
                response[indicatorLabels[count]] = numpy.nanmean(pd.json_normalize(responseData[1])['value']) / \
                                                   indicatorFactor[count]
            except TypeError:
                response[indicatorLabels[count]] = None
            except AttributeError:
                response[indicatorLabels[count]] = None

        info_dict = {'Afghanistan': None, 'Albania': 5.4, 'Angola': 13.2, 'Armenia': None, 'Azerbaijan': 32.7,
                     'Bangladesh': None, 'Benin': 13.8, 'Bolivia': 7.7, 'Burkina Faso': 20.4, 'Burundi': 27.7,
                     'Cambodia': 19.5, 'Cameroon': 22.7, 'Chad': 42.4, 'Colombia': 2.4, 'Comoros': 16.0, 'Congo': None,
                     'Congo Democratic Republic': 41.6, "Cote d'Ivoire": 25.3, 'Dominican Republic': 1.6, 'Egypt': None,
                     'Eritrea': 46.2, 'Eswatini': 12.3, 'Ethiopia': 28.4, 'Gabon': 23.1, 'Gambia': 26.4, 'Ghana': 12.1,
                     'Guatemala': 4.2, 'Guinea': 40.3, 'Guyana': 8.9, 'Haiti': 6.4, 'Honduras': 5.8, 'India': 23.2,
                     'Indonesia': 13.0, 'Jordan': None, 'Kenya': 22.1, 'Kyrgyz Republic': 22.7, 'Lesotho': 18.5,
                     'Liberia': 18.9, 'Madagascar': 16.1, 'Malawi': 6.8, 'Maldives': 11.5, 'Mali': 39.4,
                     'Moldova': 11.0, 'Morocco': 45.2, 'Mozambique': 7.4, 'Myanmar': 23.7, 'Namibia': 13.6,
                     'Nepal': 12.7, 'Nicaragua': 6.6, 'Niger': 29.2, 'Nigeria': 18.6, 'Pakistan': 24.4, 'Peru': 1.8,
                     'Philippines': 5.1, 'Rwanda': 15.5, 'Sao Tome and Principe': 11.0, 'Senegal': 23.2,
                     'Sierra Leone': 29.4, 'South Africa': 3.6, 'Tajikistan': 44.3, 'Tanzania': 29.6,
                     'Timor-Leste': 46.2, 'Togo': 13.5, 'Turkey': 7.0, 'Turkmenistan': 36.2, 'Uganda': 24.8,
                     'Ukraine': 3.7, 'Yemen': 27.6, 'Zambia': 24.4, 'Zimbabwe': 18.2}
        if country.name in info_dict:
            sftsi_score = info_dict[country.name] / 50
            response["sftsi"] = sftsi_score * 100

        su = 0
        for n, v in enumerate(response.values()):
            if not v == None:
                su += v

        overall = su / (n + 1)
        response["overall"] = overall

        return jsonify(response)