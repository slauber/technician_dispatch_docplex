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
    try:
        techniker = int(request.args.get('techniker'))
        auftraege = int(request.args.get('auftraege'))
        skills = int(request.args.get('skills'))
        seed = int(request.args.get('seed'))
        tageslaenge = int(request.args.get('tageslaenge'))
        max_tageslaenge = int(request.args.get('max_tageslaenge'))
    except:
        return app.response_class(
            response="Inputs invalid",
            status=500
        )

    problem = routingproblem.RoutingProblem()
    problem.generate_data(anz_techniker=techniker, anz_auftraege=auftraege, anz_skills=skills,
                          tageslaenge=tageslaenge, max_tageslaenge=max_tageslaenge, seed=seed)

    problem.create_model()  # Modell aus generierten Daten herstellen
    problem.solve_model(timeout=28)  # Typischer maximaler HTTP Request Timeout liegt bei 30s
    json = problem.print_solution(True, True)  # JSON Daten für den Webclient und Debugdaten in der Konsole
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
