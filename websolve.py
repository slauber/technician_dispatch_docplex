import numpy
from flask import Flask, request, send_from_directory, redirect
from flask_cors import CORS
import routingproblem

app = Flask(__name__, static_url_path='')
CORS(app)


@app.route('/app/<path:path>')
def serve_app(path):
    """Statische Dateiausgabe

    Sendet die gewünschte Datei zurück. Wird zur Ausgabe der Webapp verwendet.

    """
    return send_from_directory('html', path)


@app.route('/')
@app.route('/app')
def redirect_user():
    """Weiterleitung

    Leitet den User zur Webapp um.

    """
    return redirect('/app/index.html')


@app.route("/solve", methods=["GET"])
def solve():
    """Route zur JSON-API des Solvers, erwartet einen parametrisierten GET-Request

    Berechnet optimale Route für das gegebene Problem

    Beispiel: http://localhost:5000/solve?techniker=2&auftraege=4&skills=2&seed=1234&tageslaenge=500&max_tageslaenge=600

    :return: response_class
    """
    problem: routingproblem.RoutingProblem = None
    replanning_auftrag: routingproblem.Auftrag = None
    replanning_zeitpunkt: int = None

    try:
        print(request.args)
        techniker = int(request.args.get('techniker'))
        auftraege = int(request.args.get('auftraege'))
        skills = int(request.args.get('skills'))
        tageslaenge = int(request.args.get('tageslaenge'))
        max_tageslaenge = int(request.args.get('maxTageslaenge'))

        # Seed is optional
        seed = int(request.args.get('seed')) if request.args.get('seed') else None
        min_distanz = int(request.args.get('minDistanz'))
        max_distanz = int(request.args.get('maxDistanz'))
        min_start = int(request.args.get('minStart'))
        max_start = int(request.args.get('maxStart'))
        max_dauer = int(request.args.get('maxDauer'))
        e_dauer = int(request.args.get('eDauer'))
        max_ende = int(request.args.get('maxEnde'))
        e_ende = int(request.args.get('eEnde'))
        max_strafe_auftrag = int(request.args.get('maxStrafeAuftrag'))
        e_strafe_auftrag = int(request.args.get('eStrafeAuftrag'))
        max_strafe_techniker = int(request.args.get('maxStrafeTechniker'))
        e_strafe_techniker = int(request.args.get('eStrafeTechniker'))

        if request.args.get('advanced') == "true":
            problem = routingproblem.RoutingProblem()
            problem.daten_generieren(techniker, auftraege, skills, tageslaenge, max_tageslaenge, seed,
                                     min_distanz, max_distanz, min_start, max_start, max_dauer, e_dauer, max_ende,
                                     e_ende,
                                     max_strafe_auftrag, e_strafe_auftrag, max_strafe_techniker, e_strafe_techniker)

            if request.args.get('replanning') == "true":
                replanning_zeitpunkt = int(request.args.get('reZeitpunkt'))
                re_fruester_start = int(request.args.get('reFruesterStart'))
                re_spaetestes_ende = int(request.args.get('reSpaetestesEnde'))
                re_dauer = int(request.args.get('reDauer'))
                re_strafe = int(request.args.get('reStrafe'))
                re_skills = numpy.array(request.args.get('reSkills').split(',')).astype(dtype=int)
                replanning_auftrag = routingproblem.Auftrag(re_fruester_start, re_dauer, re_spaetestes_ende, re_strafe,
                                                            re_skills)


        else:
            problem = routingproblem.RoutingProblem(anz_techniker=techniker, anz_auftraege=auftraege, anz_skills=skills,
                                                    tageslaenge=tageslaenge, max_tageslaenge=max_tageslaenge)
    except:
        return app.response_class(
            response="Inputs invalid",
            status=500
        )

    problem.modell_aus_daten_aufstellen()  # Modell aus generierten Daten herstellen

    if replanning_auftrag:
        problem.solve_model(timeout=14)  # Typischer maximaler HTTP Request Timeout liegt bei 30s

        erstes_ergebnis = problem.json_ausgabe()

        problem.modell_aus_daten_aufstellen(replanning_daten=problem.parameter_zum_zeitpunkt(replanning_zeitpunkt),
                                            neuer_auftrag=replanning_auftrag)

        problem.solve_model(timeout=14)

        return app.response_class(
            response=problem.json_ausgabe(),
            status=200,
            mimetype='application/json'
        )

    else:
        problem.solve_model(timeout=29)  # Typischer maximaler HTTP Request Timeout liegt bei 30s
        json = problem.json_ausgabe()  # JSON Daten für den Webclient und Debugdaten in der Konsole
        if json:
            return app.response_class(
                response=json,
                status=200,
                mimetype='application/json'
            )
        else:
            return app.response_class(
                status=500
            )
