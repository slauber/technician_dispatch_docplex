from flask import Flask, request, send_from_directory, redirect
from flask_cors import CORS
import Routingproblem_mp2

app = Flask(__name__, static_url_path='')
CORS(app)


@app.route('/app/<path:path>')
def serve_app(path):
    return send_from_directory('html', path)


@app.route('/')
@app.route('/app')
def redirect_user():
    return redirect('/app/index.html')


@app.route("/solve", methods=["GET"])
def solve():
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

    problem = Routingproblem_mp2.RoutingProblem()
    problem.generate_data(anz_techniker=techniker, anz_auftraege=auftraege, anz_skills=skills,
                          tageslaenge=tageslaenge, max_tageslaenge=max_tageslaenge, seed=seed)

    problem.create_model()
    problem.solve_model(timeout=25)
    problem.print_solution(True, True)
    json = problem.get_json()
    return app.response_class(
        response=json,
        status=200,
        mimetype='application/json'
    )
