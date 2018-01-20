import numpy as np
from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution

# TECHNIKER_HAT_SKILL = np.array(
#    [
#        [0, 1],
#        [1, 1],
#        [0, 1]
#    ]
# )

TECHNIKER_HAT_SKILL = np.array(
    [
        [0, 1],
        [1, 0]
    ]
)

DISTANZMATRIX = np.array(
    [[0, 30, 70, 20, 15],
     [30, 0, 45, 30, 25],
     [70, 45, 0, 50, 45],
     [20, 30, 50, 0, 30],
     [15, 25, 45, 30, 0]]
)

# DISTANZMATRIX = np.array(
#     [[0, 30, 70, 20, 15, 10],
#      [30, 0, 45, 30, 25, 15],
#      [70, 45, 0, 50, 45, 15],
#      [20, 30, 50, 0, 30, 15],
#      [15, 25, 45, 30, 0, 10],
#      [15, 25, 45, 30, 15, 0]]
# )

AUFTRAG_BRAUCHT_SKILL = np.array(
    [[1, 0],
     [1, 0],
     [0, 1]]
)

AUFTRAGSDAUER = np.array([45, 10, 10])
FRUESTER_START = np.array([0, 0, 0])
SPAETESTES_ENDE = np.array([300, 400, 0])

H = 400
H_max = 500

STRAFE_AUFTRAG = (100, 100, 100)
STRAFE_TECHNIKER = (10.5, 10.5)

KRAFTSTOFF_KOSTEN = 0.15

GEWICHT_STRAFE_AUFTRAG = 1000
GEWICHT_STRAFE_TECHNIKER = 100
GEWICHT_TRANSPORT_KOSTEN = 1

ANZ_TECHNIKER = len(TECHNIKER_HAT_SKILL)
ANZ_AUFTRAEGE = len(AUFTRAG_BRAUCHT_SKILL)
ANZ_WEGPUNKTE = len(DISTANZMATRIX)
ANZ_SKILLS = len(TECHNIKER_HAT_SKILL[0])

mdl = Model(name="Technician Dispatch Problem")

x = mdl.binary_var_cube(ANZ_TECHNIKER, ANZ_WEGPUNKTE, ANZ_WEGPUNKTE, name="Fahrten")
start_zeit = mdl.integer_var_list(ANZ_WEGPUNKTE, name="Startzeit")

mdl.maximize(H_max - start_zeit[0] + H_max - start_zeit[1] + H_max - start_zeit[2])
print("\n", mdl.get_objective_expr())
print(mdl.get_objective_sense(), "\n")

# Startzeit eines Auftrags muss nach frühestem Startpunkt liegen
mdl.add_constraints(
    [FRUESTER_START[i] <= start_zeit[i] for i in range(ANZ_AUFTRAEGE)]
)

# Startzeit und Auftragsdauer müssen vor H_max enden
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

# Fährt nicht von anderem Wegpunkt zu fremden Depot
mdl.add_constraints(
    [
        x[(m, i, t + ANZ_AUFTRAEGE)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_WEGPUNKTE)
        for t in range(ANZ_TECHNIKER)
        if (t != m)
    ]
)

# Fährt nicht von anderem Depot zu einem Wegpunkt
mdl.add_constraints(
    [
        x[(m, i + ANZ_AUFTRAEGE, j)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_TECHNIKER)
        for j in range(ANZ_WEGPUNKTE)
        if m != i
    ]
)

# Fährt maximal einmal von seinem Depot los
mdl.add_constraints(
    [
        mdl.sum(
            x[(m, m + ANZ_AUFTRAEGE, j)]
            for j in range(ANZ_AUFTRAEGE)
        ) <= 1
        for m in range(ANZ_TECHNIKER)
    ]
)

# Fährt maximal einmal nach Hause
mdl.add_constraints(
    mdl.sum(
        x[(m, j, m + ANZ_AUFTRAEGE)]
        for j in range(ANZ_AUFTRAEGE)
    ) <= 1
    for m in range(ANZ_TECHNIKER)
)

# Beginnt die Route im eigenen Depot
mdl.add_constraints(
    x[(m, i, j)] <= mdl.sum(
        x[(m, m + ANZ_AUFTRAEGE, t)] for t in range(ANZ_AUFTRAEGE)
    )
    for m in range(ANZ_TECHNIKER)
    for i in range(ANZ_WEGPUNKTE)
    for j in range(ANZ_AUFTRAEGE)
)

# Endet die Route im eigenen Depot
# mdl.add_constraints(
#    x[(m, i, j)] <= mdl.sum(
#        x[(m, t, m + ANZ_AUFTRAEGE)]
#        for t in range(ANZ_AUFTRAEGE)
#    )
#    for m in range(ANZ_TECHNIKER)
#    for i in range(ANZ_WEGPUNKTE)
#    for j in range(ANZ_AUFTRAEGE)
# )
#

# Fährt maximal einmal von einem Wegpunkt zu einem anderen Wegpunkt
mdl.add_constraints(
    mdl.sum(
        x[(m, j, k)]
        for k in range(ANZ_WEGPUNKTE)
    ) <= 1
    for m in range(ANZ_TECHNIKER)
    for j in range(ANZ_WEGPUNKTE)
    if m + ANZ_AUFTRAEGE != j
)

# Wenn er von einem Auftrag wegfährt, dann muss er dort auch hingefahren sein
mdl.add_constraints(
    [
        x[(m, j, l)] <= mdl.sum(
            [
                x[(m, t, j)]
                for t in range(ANZ_WEGPUNKTE)
                if j != t
                if l != t
            ]
        )
        for m in range(ANZ_TECHNIKER)
        for j in range(ANZ_AUFTRAEGE)
        for l in range(ANZ_WEGPUNKTE)
        if l != j
    ]
)

# Wenn er einen Auftrag besucht, dann muss er von dort auch wieder wegfahren
mdl.add_constraints(
    x[(m, l, j)] <= mdl.sum(
        x[(m, j, i)]
        for i in range(ANZ_WEGPUNKTE)
        if i != j
    )
    for m in range(ANZ_TECHNIKER)
    for l in range(ANZ_WEGPUNKTE)
    for j in range(ANZ_AUFTRAEGE)
    if l != j
)

# Jeder Auftrag muss besucht worden sein
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

# Ein Auftrag besucht sich nicht selbst
mdl.add_constraints(
    [
        x[(m, i, i)] == 0
        for m in range(ANZ_TECHNIKER)
        for i in range(ANZ_AUFTRAEGE)
    ]
)

# Defaultwert für Technikerstart
mdl.add_constraints(
    start_zeit[m + ANZ_AUFTRAEGE] == 0
    for m in range(ANZ_TECHNIKER)
)

# Skill constraint
mdl.add_constraints(
    AUFTRAG_BRAUCHT_SKILL[i][s] - (1 - x[(m, i, j)]) <= TECHNIKER_HAT_SKILL[m][s]
    for m in range(ANZ_TECHNIKER)
    for i in range(ANZ_AUFTRAEGE)
    for j in range(ANZ_WEGPUNKTE)
    for s in range(ANZ_SKILLS)
)
print(mdl.has_objective())
mdl.solve()
mdl.report()

solution: SolveSolution = mdl.solution
print(solution)
