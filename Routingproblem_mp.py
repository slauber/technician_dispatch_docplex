# coding: utf-8

# # Routing problem

# Wichtig: Die Solver-Binary muss im PYTHONPATH liegen!

import numpy as np
from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution

TECHNIKER = ["T1", "T2", "T3", "T4", "T5"]

# Definition der Skillsets der Techniker
TECHNIKER_HAT_SKILL = np.array(
    [[0, 1, 0],
     [1, 1, 0],
     [0, 1, 1],
     [1, 0, 1],
     [0, 0, 1]]
)

# Dauer der Übergänge von a nach b
DISTANZMATRIX = np.array(
    [[0, 50, 50, 70, 70, 60, 60, 40, 40, 100, 45, 45, 70, 70, 55, 55],
     [50, 0, 45, 45, 65, 70, 50, 25, 90, 60, 70, 70, 30, 30, 90, 90],
     [50, 45, 0, 60, 70, 50, 40, 150, 80, 40, 50, 50, 60, 60, 30, 30],
     [70, 45, 60, 0, 25, 90, 50, 65, 60, 50, 90, 90, 50, 50, 40, 40],
     [70, 65, 70, 25, 0, 50, 40, 70, 70, 100, 50, 50, 100, 100, 60, 60],
     [60, 70, 50, 90, 50, 0, 40, 150, 30, 90, 20, 20, 80, 80, 50, 50],
     [60, 50, 40, 50, 40, 40, 0, 30, 40, 50, 60, 60, 80, 80, 20, 20],
     [40, 25, 150, 65, 70, 150, 30, 0, 60, 80, 50, 50, 200, 200, 30, 30],
     [40, 90, 80, 60, 70, 30, 40, 60, 0, 50, 30, 30, 40, 40, 50, 50],
     [100, 60, 40, 50, 100, 90, 90, 50, 80, 0, 50, 50, 40, 40, 80, 80],
     [45, 70, 50, 90, 50, 20, 60, 50, 40, 50, 0, 0, 50, 50, 100, 100],
     [45, 70, 50, 90, 50, 20, 60, 50, 40, 50, 0, 0, 50, 50, 100, 100],
     [70, 30, 60, 50, 100, 80, 80, 200, 40, 40, 50, 50, 0, 0, 100, 100],
     [70, 30, 60, 50, 100, 80, 80, 200, 40, 40, 50, 50, 0, 0, 100, 100],
     [55, 90, 30, 40, 60, 50, 20, 30, 50, 80, 100, 100, 100, 100, 0, 0]]
)

AUFTRAG_BRAUCHT_SKILL = np.array(
    [[1, 1, 0],
     [0, 1, 1],
     [1, 1, 0],
     [1, 0, 1],
     [1, 0, 1],
     [1, 0, 0],
     [1, 0, 0],
     [0, 1, 1],
     [0, 1, 0],
     [0, 1, 0]]
)

AUFTRAGSDAUER = np.array([45, 45, 45, 30, 30, 45, 30, 30, 45, 60, 0, 0, 0, 0, 0])
FRUESTER_START = np.array([0, 100, 100, 0, 200, 0, 0, 0, 300, 20, 0, 0, 0, 0, 0])
SPAETESTER_START = np.array([150, 300, 300, 250, 300, 300, 400, 500, 500, 250, 0, 0, 0, 0, 0])

H = 480
H_max = 600

STRAFE_AUFTRAG = (100, 100, 100, 50, 50, 100, 50, 50, 100, 150)
STRAFE_TECHNIKER = (0.5, 0.4, 0.3, 0.4, 0.4)

KRAFTSTOFF_KOSTEN = 0.15

# Gewichtete Werte für Zielfunktion
GEWICHT_STRAFE_AUFTRAG = 1000
GEWICHT_STRAFE_TECHNIKER = 100
GEWICHT_TRANSPORT_KOSTEN = 1

ANZ_TECHNIKER = len(TECHNIKER_HAT_SKILL)
ANZ_AUFTRAEGE = len(AUFTRAG_BRAUCHT_SKILL)
ANZ_WEGPUNKTE = len(DISTANZMATRIX)

# sanity checks
print('ANZ_TECHNIKER:', ANZ_TECHNIKER)
print('ANZ_AUFTRAEGE:', ANZ_AUFTRAEGE)
print('ANZ_WEGPUNKTE:', ANZ_WEGPUNKTE)
print('len(AUFTRAG_BRAUCHT_SKILL):', len(AUFTRAG_BRAUCHT_SKILL))

# Modell erstellen
mdl = Model(name="techicians")

#
# Entscheidungsvariablen
#
x = mdl.binary_var_cube(ANZ_TECHNIKER, ANZ_WEGPUNKTE, ANZ_WEGPUNKTE, name="Fahrten")
start_zeit = mdl.integer_var_list(ANZ_WEGPUNKTE, name="Startzeit")

# Entscheidungsausdrücke
strafkosten_auftrag = mdl.sum(
    [
        mdl.max(0, start_zeit[i] + AUFTRAGSDAUER[i] - SPAETESTER_START[i]) * STRAFE_AUFTRAG[i]
        for i in range(ANZ_AUFTRAEGE)
    ]
)
mdl.add_kpi(strafkosten_auftrag, "Strafkosten Auftrag")

strafkosten_techniker = mdl.sum(
    [
        mdl.max(0, start_zeit[i] + AUFTRAGSDAUER[i], DISTANZMATRIX[i][m + ANZ_AUFTRAEGE] - H)
        * STRAFE_TECHNIKER[m] * x[(m, i, m + ANZ_AUFTRAEGE)]
        for i in range(ANZ_AUFTRAEGE)
        for m in range(ANZ_TECHNIKER)
    ]
)
mdl.add_kpi(strafkosten_techniker, "Strafkosten Techniker")

transportkosten = mdl.sum(
    x[(m, i, j)] * DISTANZMATRIX[i][j] * KRAFTSTOFF_KOSTEN
    for m in range(ANZ_TECHNIKER)
    for i in range(ANZ_WEGPUNKTE)
    for j in range(ANZ_WEGPUNKTE)
)
mdl.add_kpi(transportkosten, "Transportkosten")

#
# Zielfunktion
#
kosten = GEWICHT_STRAFE_AUFTRAG * strafkosten_auftrag + GEWICHT_STRAFE_TECHNIKER * strafkosten_techniker + GEWICHT_TRANSPORT_KOSTEN * transportkosten
mdl.minimize(kosten)

#
# Restriktionen
#
#
# Ein Auftrag muss vor H-Max enden & Techniker muss spätestens bis H_max zuhause sein
mdl.add_constraints(
    [FRUESTER_START[i] + AUFTRAGSDAUER[i] <= start_zeit[i] + AUFTRAGSDAUER[i] for i in range(ANZ_AUFTRAEGE)]
)

mdl.add_constraints(
    [start_zeit[i] + AUFTRAGSDAUER[i] <= H_max for i in range(ANZ_AUFTRAEGE)]
)

mdl.add_equivalence_constraints(
    [
        mdl.add_equivalence(x[(m, i, m)],
                            start_zeit[i] + AUFTRAGSDAUER[i] + DISTANZMATRIX[i][m] <= H_max)
        for i in range(ANZ_AUFTRAEGE) for m in range(ANZ_TECHNIKER)
    ]
)

mdl.add_constraints(
    [
        x[(m, m + ANZ_AUFTRAEGE, i)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_TECHNIKER)
        if m != i
    ]
)
mdl.add_constraints(
    [
        x[(m, j, i + ANZ_AUFTRAEGE)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_TECHNIKER)
        for j in range(ANZ_AUFTRAEGE) if m != i
    ]
)
mdl.add_constraints(
    [
        x[(m, i + ANZ_AUFTRAEGE, j)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_TECHNIKER)
        for j in range(ANZ_AUFTRAEGE) if m != i
    ]
)

# ctOnlyHome_1: sum(t in Auftrag) x[m][m][t] <= 1; /* Techniker darf maximal nur einmal starten, und das nur vom eigenen Standort*/
for m in range(ANZ_TECHNIKER):
    _temp = []
    for j in range(ANZ_AUFTRAEGE):
        _temp.append(x[(m, m + ANZ_AUFTRAEGE, j)])
    mdl.add_constraint(mdl.sum(_temp) <= 1)

# onlyhome2
for m in range(ANZ_TECHNIKER):
    _temp = []
    for j in range(ANZ_AUFTRAEGE):
        _temp.append(x[(m, j, m + ANZ_AUFTRAEGE)])
    mdl.add_constraint(mdl.sum(_temp) <= 1)

# forall(m, i in Techniker, j in Auftrag: m != i){
# ctOnlyHome_3: x[m][m][j] == 1 => sum (t in Auftrag) x[m][t][m] == 1

# sum (t in Auftrag) x[m][m][t] == sum (t in Auftrag) x[m][t][m]
for m in range(ANZ_TECHNIKER):
    _temp1 = []
    _temp2 = []
    for j in range(ANZ_AUFTRAEGE):
        _temp1.append(x[(m, j, m + ANZ_AUFTRAEGE)])
        _temp2.append(x[(m, m + ANZ_AUFTRAEGE, j)])
    mdl.add_constraint(mdl.sum(_temp1) == mdl.sum(_temp2))

# oh5
mdl.add_constraints(
    [
        x[(m, i + ANZ_AUFTRAEGE, t + ANZ_AUFTRAEGE)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_TECHNIKER)
        if (m != i)
        for t in range(ANZ_TECHNIKER)
        if (t != m)
    ]
)

# oh6
mdl.add_constraints(
    [
        x[(m, i + ANZ_AUFTRAEGE, t)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_TECHNIKER)
        if (m != i)
        for t in range(ANZ_AUFTRAEGE)
    ]
)

# oh7
# for k in r#ange(ANZ_WEGPUNKTE):
#    mdl.add_constraint(
#
#    )
mdl.add_constraints(
    [
        mdl.sum([x[(m, j, k)] for k in range(ANZ_WEGPUNKTE)]) <= 1
        for m in range(ANZ_TECHNIKER)
        for j in range(ANZ_AUFTRAEGE)
    ]
)

mdl.print_information()

#
# Lösungsauftrag
#
mdl.solve()
mdl.report()

solution: SolveSolution = mdl.solution
print(solution)
