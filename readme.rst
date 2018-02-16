Technician Dispatch Problem (DOcplex.MP)
========================================
Dieses Programm ist Teil einer Abgabe zu Lösung des Technician Dispatch Problems.
Es entsteht im Seminar Smart Services and the IoT.

.. image:: https://raw.githubusercontent.com/slauber/technician_dispatch_docplex/master/docs/tdp.gif

Requirements
------------
- lokale Installation von `IBM CPlex`_ >= Version 12.7
    - cpoptimizer executable muss im :code:`PYTHONPATH` liegen (insbesondere bei :code:`virtualenv` überprüfen, siehe `DOcplex Doku (lokal)`_)
    - Alternative: Nutzung des Cloud Solvers, siehe `DOcplex Doku (Cloud)`_
- Nutzung von :code:`virtualenv` wird empfohlen, verwendete Pythonversion zur Entwicklung: 3.6
- Abhängigkeiten aus :code:`requirements.txt`

Installation & Nutzung
----------------------
- Abhängigkeiten installieren (siehe oben)
- ggf. Anpassung des Szenarios in der main-Methode der Anwendung (:code:`routingproblem.py`) und Start des Solvers (:code:`python routingproblem.py`)
- Start des Webservers (Linux und macOS :code:`export FLASK_APP=websolve.py&&flask run`, Windows siehe `Flask CLI Doku`_)

Solver
------
Die Implementierung zur Aufstellung und Lösung des Technician Dispatch Problems ist in der :code:`routingproblem.py` zu finden.

Webapp
------
Es gibt eine Webapp, die zur bequemen Steuerung des Simulators dient. Die Webapp ist mit `Flask`_ entwickelt.

.. _IBM CPlex: https://www.ibm.com/analytics/data-science/prescriptive-analytics/cplex-optimizer
.. _DOcplex Doku (lokal): https://ibmdecisionoptimization.github.io/docplex-doc/cp/creating_model.html#solve-a-model-with-local-solver
.. _DOcplex Doku (Cloud): https://ibmdecisionoptimization.github.io/docplex-doc/getting_started.html#using-the-ibm-decision-optimization-on-cloud-service
.. _Flask: http://flask.pocoo.org
.. _Flask CLI Doku: https://flask.pocoo.org/docs/0.12/cli/