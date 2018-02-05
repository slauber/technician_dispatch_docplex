Technician Dispatch Problem (DOcplex.MP)
========================================
Dieses Programm ist Teil einer Abgabe zu Lösung des Technician Dispatch Problems.
Es entsteht im Seminar Smart Services and the IoT.

.. image:: https://raw.githubusercontent.com/slauber/technician_dispatch_docplex/master/docs/tdp.gif

Requirements
------------
- lokale Installation von `IBM CPlex`_ >= Version 12.7
    - cpoptimizer executable muss im PYTHONPATH liegen (insbesondere bei virtualenv überprüfen, `DOcplex Doku`_)
- Abhängigkeiten aus requirements.txt

Solver
------
Die Implementierung zur Aufstellung und Lösung des Technician Dispatch Problems ist in der :code:`routingproblem.py` zu finden.

Webapp
------
Es gibt eine Webapp, die zur bequemen Steuerung des Simulators dient. Die Webapp ist mit `Flask`_ entwickelt und lässt sich mit :code:`flask run` ausführen, wenn die Umgebungsvariable :code:`FLASK_APP=websolve` gesetzt ist.

.. _IBM CPlex: https://www.ibm.com/analytics/data-science/prescriptive-analytics/cplex-optimizer
.. _DOcplex Doku: http://ibmdecisionoptimization.github.io/docplex-doc/cp/creating_model.html#solve-a-model-with-local-solver
.. _Flask: http://flask.pocoo.org