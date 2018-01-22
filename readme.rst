Technician Dispatch Problem (DOcplex.MP)
========================================
Dieses Programm ist Teil einer Abgabe zu Lösung des Technician Dispatch Problems.
Es entsteht im Seminar Smart Services and the IoT.

Requirements
------------
- lokale Installation von `IBM CPlex` >= Version 12.7
    - cpoptimizer executable muss im PYTHONPATH liegen (insbesondere bei virtualenv überprüfen, `DOcplex Doku)
- Abhängigkeiten aus requirements.txt

Solver
------
Die Implementierung zur Aufstellung und Lösung des Technician Dispatch Problems ist in der :code:`routingproblem.py zu finden.

Webapp
------
Es gibt eine Webapp, die zur bequemen Steuerung des Simulators dient. Die Webapp ist mit `Flask` entwickelt und lässt sich mit :code:`flask run ausführen, wenn die Umgebungsvariable :code:`FLASK_APP=websolve` gesetzt ist.

.. _IBM CPlex: https://www.ibm.com/analytics/data-science/prescriptive-analytics/cplex-optimizer
.. _DOcplex Doku: http://ibmdecisionoptimization.github.io/docplex-doc/cp/creating_model.html#solve-a-model-with-local-solver
.. _Flask: http://flask.pocoo.org