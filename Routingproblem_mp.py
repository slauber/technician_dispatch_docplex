# coding: utf-8

# # Routing problem

# Wichtig: Die Solver-Binary muss im PYTHONPATH liegen!

import numpy as np
from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution

# Definition der Skillsets der Techniker
TECHNIKER_HAT_SKILL = np.array(
    [[1, 1],
     [0, 1]]
)

# Dauer der Übergänge von a nach b
DISTANZMATRIX = np.array(
    [[0, 30, 70, 20, 15],
     [30, 0, 45, 30, 25],
     [70, 45, 0, 50, 45],
     [20, 30, 50, 0, 30],
     [15, 25, 45, 30, 0]]
)

print(DISTANZMATRIX)

AUFTRAG_BRAUCHT_SKILL = np.array(
    [[1, 1],
     [1, 0],
     [0, 1]]
)

AUFTRAGSDAUER = np.array([45, 10, 10])
FRUESTER_START = np.array([0, 0, 0])
SPAETESTER_START = np.array([300, 400, 0])

H = 300
H_max = 600

STRAFE_AUFTRAG = (100, 100, 100)
STRAFE_TECHNIKER = (0.3, 10.5)

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

#
# Restriktionen
#
#
# Ein Auftrag muss vor H-Max enden & Techniker muss spätestens bis H_max zuhause sein
mdl.add_constraints(
    [FRUESTER_START[i] <= start_zeit[i] for i in range(ANZ_AUFTRAEGE)]
)

mdl.add_constraints(
    [start_zeit[i] + AUFTRAGSDAUER[i] <= H_max for i in range(ANZ_AUFTRAEGE)]
)

mdl.add_equivalence_constraints(
    [
        mdl.add_equivalence(x[(m, i, m + ANZ_AUFTRAEGE)],
                            start_zeit[i] + AUFTRAGSDAUER[i] + DISTANZMATRIX[i][m + ANZ_AUFTRAEGE] <= H_max)
        for i in range(ANZ_AUFTRAEGE) for m in range(ANZ_TECHNIKER)
    ]
)


mdl.add_constraints(
    [
        x[(m, m + ANZ_AUFTRAEGE, i + ANZ_AUFTRAEGE)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_TECHNIKER)
        if m != i
    ]
)

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

mdl.add_constraints(
    [
        x[(m, j, i + ANZ_AUFTRAEGE)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_TECHNIKER)
        for j in range(ANZ_AUFTRAEGE)
        if m != i
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

mdl.add_constraints(
    x[(m, i, j)] <= mdl.sum(
        x[(m, m + ANZ_AUFTRAEGE, t)] for t in range(ANZ_AUFTRAEGE)
    )
    for m in range(ANZ_TECHNIKER)
    for i in range(ANZ_WEGPUNKTE)
    for j in range(ANZ_AUFTRAEGE)
)

# sum (t in Auftrag) x[m][m][t] == sum (t in Auftrag) x[m][t][m]
for m in range(ANZ_TECHNIKER):
    _temp1 = []
    _temp2 = []
    for j in range(ANZ_AUFTRAEGE):
        _temp1.append(x[(m, j, m + ANZ_AUFTRAEGE)])
        _temp2.append(x[(m, m + ANZ_AUFTRAEGE, j)])
    mdl.add_constraint(mdl.sum(_temp1) == mdl.sum(_temp2))


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
mdl.add_constraints(
    [
        mdl.sum([x[(m, j, k)] for k in range(ANZ_WEGPUNKTE)]) <= 1
        for m in range(ANZ_TECHNIKER)
        for j in range(ANZ_AUFTRAEGE)
    ]
)

# intraroute
mdl.add_constraints(
    [
        x[(m, j, l)] <= mdl.sum(
            [x[(m, t, j)] for t in range(ANZ_WEGPUNKTE) if j != t]
        )
        for m in range(ANZ_TECHNIKER)
        for j in range(ANZ_AUFTRAEGE)
        for l in range(ANZ_WEGPUNKTE)
        if l != j
    ]
)

mdl.add_constraints(
    [
        mdl.sum(
            [
                x[(m, j, i)]
                for m in range(ANZ_TECHNIKER)
                for j in range(ANZ_WEGPUNKTE)
            ]
        ) == 1
        for i in range(ANZ_AUFTRAEGE)
    ]
)

# mdl.add_equivalence_constraints(
#    mdl.add_equivalence(
#        mdl.sum(
#            x[(m,i,j)]
#            for i in range(ANZ_WEGPUNKTE)
#            for j in range(ANZ_AUFTRAEGE)
#        ) >= 1,
#        mdl.sum(
#            x[(m,m,j)]
#            for j in range(ANZ_AUFTRAEGE)
#        ) == 1
#    )
#    for m in range(ANZ_TECHNIKER)
# )

mdl.add_constraints(
    [
        x[(m, i, i)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_AUFTRAEGE)
    ]
)

mdl.add_constraints(
    start_zeit[m + ANZ_AUFTRAEGE] == 0
    for m in range(ANZ_TECHNIKER)
)

# mdl.add_equivalence_constraints(
#    mdl.add_equivalence(#
#        x[(m, i, j)],
#        start_zeit[j] >= (start_zeit[i] + AUFTRAGSDAUER[i] + DISTANZMATRIX[i][j])
#    )
#    for m in range(ANZ_TECHNIKER)
#    for i in range(ANZ_AUFTRAEGE)
#    for j in range(ANZ_WEGPUNKTE)
#    if i != j and i != m
# )

# Entscheidungsausdrücke
strafkosten_auftrag = mdl.sum(
    mdl.max(0, start_zeit[i] + AUFTRAGSDAUER[i] - SPAETESTER_START[i]) * STRAFE_AUFTRAG[i]
    for i in range(ANZ_AUFTRAEGE)
)
mdl.add_kpi(strafkosten_auftrag, "Strafkosten Auftrag")

strafkosten_techniker = mdl.sum(
    mdl.max(0, start_zeit[i] + AUFTRAGSDAUER[i], DISTANZMATRIX[i][m + ANZ_AUFTRAEGE] - H)
    * STRAFE_TECHNIKER[m] * x[(m, i, m + ANZ_AUFTRAEGE)]
    for i in range(ANZ_AUFTRAEGE)
    for m in range(ANZ_TECHNIKER)
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
kosten = GEWICHT_STRAFE_AUFTRAG * strafkosten_auftrag + \
         GEWICHT_STRAFE_TECHNIKER * strafkosten_techniker + \
         GEWICHT_TRANSPORT_KOSTEN * transportkosten

mdl.minimize(mdl.sum(start_zeit[i] for i in range(ANZ_AUFTRAEGE)))
#mdl.minimize(kosten)

print("\n", mdl.get_objective_expr())
print(mdl.get_objective_sense(), "\n")
#
# Lösungsauftrag
#
mdl.solve()
mdl.report()

solution: SolveSolution = mdl.solution
print(solution)
