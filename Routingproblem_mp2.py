from typing import Dict, List

import numpy as np
from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution


class RoutingProblem:
    DISTANZMATRIX: np.array
    TECHNIKER_HAT_SKILL: np.array
    AUFTRAG_BRAUCHT_SKILL: np.array

    AUFTRAGSDAUER: np.array
    FRUESTER_START: np.array
    SPAETESTES_ENDE: np.array

    H: int
    H_max: int

    STRAFE_AUFTRAG: np.array
    STRAFE_TECHNIKER: np.array

    KRAFTSTOFF_KOSTEN = 0.15

    GEWICHT_STRAFE_AUFTRAG = 1000
    GEWICHT_STRAFE_TECHNIKER = 100
    GEWICHT_TRANSPORT_KOSTEN = 1

    ANZ_TECHNIKER: int
    ANZ_AUFTRAEGE: int
    ANZ_WEGPUNKTE: int
    ANZ_SKILLS: int

    mdl: Model

    def generate_data(self, anz_techniker: int, anz_auftraege: int, anz_skills: int,
                      tageslaenge: int, max_tageslaenge: int, seed: int):
        anz_wegpunkte = anz_techniker + anz_auftraege
        np.random.seed(seed)
        distanzmatrix = np.random.randint(0, 60, size=(anz_wegpunkte, anz_wegpunkte))
        distanzmatrix = (distanzmatrix + distanzmatrix.T)
        np.fill_diagonal(distanzmatrix, 0)

        self.H = tageslaenge
        self.H_max = max_tageslaenge

        self.DISTANZMATRIX = distanzmatrix
        self.TECHNIKER_HAT_SKILL = np.random.randint(0, 2, size=(anz_techniker, anz_skills))
        self.AUFTRAG_BRAUCHT_SKILL = np.random.randint(0, 2, size=(anz_auftraege, anz_skills))
        self.AUFTRAGSDAUER = np.random.randint(10, 120, size=anz_wegpunkte)
        for i in range(anz_techniker):
            self.AUFTRAGSDAUER[anz_auftraege + i] = 0

        self.FRUESTER_START = np.random.randint(0, 120, size=anz_auftraege)

        self.SPAETESTES_ENDE = np.zeros(anz_auftraege)
        for i in range(anz_auftraege):
            self.SPAETESTES_ENDE[i] = self.FRUESTER_START[i] + self.AUFTRAGSDAUER[i] + np.random.randint(30, 120)

        self.STRAFE_AUFTRAG = np.random.randint(25, 300, size=anz_auftraege)
        self.STRAFE_TECHNIKER = np.random.randint(5, 20, size=anz_techniker)

        self.ANZ_AUFTRAEGE = anz_auftraege
        self.ANZ_SKILLS = anz_skills
        self.ANZ_TECHNIKER = anz_techniker
        self.ANZ_WEGPUNKTE = anz_wegpunkte

        # check generated skillset and regenerate if necessary
        skill_check = np.zeros(self.ANZ_AUFTRAEGE, dtype=bool)
        for techniker in self.TECHNIKER_HAT_SKILL:
            for i, auftrag in enumerate(self.AUFTRAG_BRAUCHT_SKILL):
                skill_check[i] = skill_check[i] or np.logical_or(techniker, np.logical_not(auftrag)).all()

        if (not skill_check.all()):
            print("Warning - Generated data was inconsistent - Regenerating using seed ", seed + 1)
            self.generate_data(anz_techniker, anz_auftraege, anz_skills, tageslaenge, max_tageslaenge, seed + 1)

    def set_data(self):
        pass

    def print_input(self):
        print('Distanzmatrix\n', self.DISTANZMATRIX)
        print('Frühster Start\n', self.FRUESTER_START)
        print('Auftragsdauer\n', self.AUFTRAGSDAUER)
        print('Spätestes Ende\n', self.SPAETESTES_ENDE)
        print('Technikerskills\n', self.TECHNIKER_HAT_SKILL)
        print('Auftragskills\n', self.AUFTRAG_BRAUCHT_SKILL)

    def create_model(self):
        mdl = Model(name="Technician Dispatch Problem")

        # Abkürzung für loop ranges
        r_auftraege = range(self.ANZ_AUFTRAEGE)
        r_wegpunkte = range(self.ANZ_WEGPUNKTE)
        r_techniker = range(self.ANZ_TECHNIKER)
        r_skills = range(self.ANZ_SKILLS)

        x = mdl.binary_var_cube(self.ANZ_TECHNIKER, self.ANZ_WEGPUNKTE, self.ANZ_WEGPUNKTE, name="Fahrt")
        start_zeit = mdl.integer_var_list(self.ANZ_WEGPUNKTE, name="Startzeit")

        # Entscheidungsausdrücke
        strafkosten_auftrag = mdl.sum(
            mdl.max(0, start_zeit[i] + self.AUFTRAGSDAUER[i] - self.SPAETESTES_ENDE[i]) * self.STRAFE_AUFTRAG[i]
            for i in r_auftraege
        )
        mdl.add_kpi(strafkosten_auftrag, "Strafkosten Auftrag")
        #
        strafkosten_techniker = mdl.sum(
            mdl.max(0, start_zeit[i] + self.AUFTRAGSDAUER[i], self.DISTANZMATRIX[i][m + self.ANZ_AUFTRAEGE] - self.H)
            * self.STRAFE_TECHNIKER[m] * x[(m, i, m + self.ANZ_AUFTRAEGE)]
            for i in r_auftraege
            for m in r_techniker
        )
        mdl.add_kpi(strafkosten_techniker, "Strafkosten Techniker")
        #
        transportkosten = mdl.sum(
            x[(m, i, j)] * self.DISTANZMATRIX[i][j] * self.KRAFTSTOFF_KOSTEN
            for m in r_techniker
            for i in r_wegpunkte
            for j in r_wegpunkte
        )
        mdl.add_kpi(transportkosten, "Transportkosten")

        mdl.minimize(
            strafkosten_auftrag * self.GEWICHT_STRAFE_AUFTRAG + strafkosten_techniker * self.GEWICHT_STRAFE_TECHNIKER
        )

        print("\n", mdl.get_objective_expr())
        print(mdl.get_objective_sense(), "\n")

        # Startzeit eines Auftrags muss nach frühestem Startpunkt liegen
        mdl.add_constraints(
            self.FRUESTER_START[i] <= start_zeit[i]
            for i in r_auftraege
        )

        # Startzeit und Auftragsdauer müssen vor H_max enden
        mdl.add_constraints(
            start_zeit[i] + self.AUFTRAGSDAUER[i] <= self.H_max
            for i in r_auftraege
        )

        [
            mdl.add_if_then(
                x[(m, i, m + self.ANZ_AUFTRAEGE)] == 1,
                start_zeit[i] + self.AUFTRAGSDAUER[i] + self.DISTANZMATRIX[i][
                    m + self.ANZ_AUFTRAEGE] <= self.H_max
            )
            for i in r_auftraege for m in r_techniker
        ]

        # Fährt nicht von anderem Wegpunkt zu fremden Depot
        mdl.add_constraints(
            x[(m, i, t + self.ANZ_AUFTRAEGE)] == 0
            for m in r_techniker
            for i in r_wegpunkte
            for t in r_techniker
            if (t != m)
        )

        # Fährt nicht von anderem Depot zu einem Wegpunkt
        mdl.add_constraints(
            x[(m, i + self.ANZ_AUFTRAEGE, j)] == 0
            for m in r_techniker
            for i in r_techniker
            for j in r_wegpunkte
            if m != i
        )

        # Fährt maximal einmal von seinem Depot los
        mdl.add_constraints(
            mdl.sum(
                x[(m, m + self.ANZ_AUFTRAEGE, j)]
                for j in r_auftraege
            ) <= 1
            for m in r_techniker
        )

        # Fährt maximal einmal nach Hause
        mdl.add_constraints(
            mdl.sum(
                x[(m, j, m + self.ANZ_AUFTRAEGE)]
                for j in r_auftraege
            ) <= 1
            for m in r_techniker
        )

        # Beginnt die Route im eigenen Depot
        mdl.add_constraints(
            x[(m, i, j)] <= mdl.sum(
                x[(m, m + self.ANZ_AUFTRAEGE, t)] for t in r_auftraege
            )
            for m in r_techniker
            for i in r_wegpunkte
            for j in r_auftraege
        )

        # Endet die Route im eigenen Depot
        mdl.add_constraints(
            x[(m, i, j)] <= mdl.sum(
                x[(m, t, m + self.ANZ_AUFTRAEGE)]
                for t in r_auftraege
                if t != i
            )
            for m in r_techniker
            for i in r_wegpunkte
            for j in r_auftraege
            if i != j
            if (i < self.ANZ_AUFTRAEGE) or (i == m + self.ANZ_AUFTRAEGE)
        )

        # Fährt maximal einmal von einem Wegpunkt zu einem anderen Wegpunkt
        mdl.add_constraints(
            mdl.sum(
                x[(m, j, k)]
                for k in r_wegpunkte
            ) <= 1
            for m in r_techniker
            for j in r_wegpunkte
            if m + self.ANZ_AUFTRAEGE != j
        )

        # Wenn er von einem Auftrag wegfährt, dann muss er dort auch hingefahren sein
        mdl.add_constraints(
            x[(m, j, l)] <= mdl.sum([
                x[(m, t, j)]
                for t in r_wegpunkte
                if j != t
                if l != t
            ]
            )
            for m in r_techniker
            for j in r_auftraege
            for l in r_wegpunkte
            if l != j
        )

        # Jeder Auftrag muss genaz einmal besucht worden sein
        mdl.add_constraints(
            mdl.sum(
                [
                    x[(m, j, i)]
                    for m in r_techniker
                    for j in r_wegpunkte
                ]
            ) == 1
            for i in r_auftraege
        )

        # Ein Auftrag besucht sich nicht selbst
        mdl.add_constraints(
            x[(m, i, i)] == 0
            for m in r_techniker
            for i in r_auftraege
        )

        # Defaultwert für Technikerstart
        mdl.add_constraints(
            start_zeit[m + self.ANZ_AUFTRAEGE] == 0
            for m in r_techniker
        )

        # Zeitconstraints, Startzeiten müssen der Route entsprechen
        [
            mdl.add_if_then(
                x[(m, i, j)] == 1,
                start_zeit[j] >= (start_zeit[i] + self.AUFTRAGSDAUER[i] + self.DISTANZMATRIX[i][j])
            )
            for m in r_techniker
            for i in r_wegpunkte
            for j in r_auftraege
            if i != j
        ]

        # Skill constraint
        mdl.add_constraints(
            self.AUFTRAG_BRAUCHT_SKILL[i][s] - (1 - x[(m, i, j)]) <= self.TECHNIKER_HAT_SKILL[m][s]
            for m in r_techniker
            for i in r_auftraege
            for j in r_wegpunkte
            for s in r_skills
        )

        #print(mdl.export_as_lp_string())
        self.mdl = mdl

    def solve_model(self, timeout: int = 10):
        self.mdl.set_time_limit(timeout)
        self.mdl.solve()
        self.mdl.report()
        print(self.mdl.get_solve_details())

        solution: SolveSolution = self.mdl.solution
        print(solution)

        solution_dict = solution.as_dict()
        fahrten_pro_techniker: Dict[int, List] = {}
        for m in range(self.ANZ_TECHNIKER):
            for i in range(self.ANZ_WEGPUNKTE):
                for j in range(self.ANZ_WEGPUNKTE):
                    if 'Fahrt_{}_{}_{}'.format(m, i, j) in solution_dict:
                        if m in fahrten_pro_techniker:
                            fahrten_pro_techniker[m].append((i, j))
                        else:
                            fahrten_pro_techniker[m] = [(i, j)]

        fahrten_pro_techniker_sortiert = {}

        for techniker, fahrten in fahrten_pro_techniker.items():
            current_node = techniker + self.ANZ_AUFTRAEGE
            fahrten_pro_techniker_sortiert[techniker] = [current_node]
            while True:
                next_node = None
                i = 0
                while (next_node is None):
                    if fahrten[i][0] == current_node:
                        next_node = fahrten[i][1]
                    else:
                        i = i + 1

                fahrten_pro_techniker_sortiert[techniker].append(next_node)
                current_node = next_node
                if (current_node == techniker + self.ANZ_AUFTRAEGE):
                    break

        print(fahrten_pro_techniker_sortiert)
        for techniker, fahrten in fahrten_pro_techniker_sortiert.items():
            str = "Techniker {} fährt von seinem Depot ".format(techniker)
            for fahrt in fahrten:
                if fahrt <= self.ANZ_AUFTRAEGE:
                    str = str + "zu Auftrag {} (Startzeit: {}) ".format(fahrt,
                                                                        solution_dict["Startzeit_{}".format(fahrt)])
            str = str + "und zurück zu seinem Depot."

            print(str)



if __name__ == '__main__':
    problem = RoutingProblem()

    problem.generate_data(anz_techniker=3, anz_auftraege=5, anz_skills=2, tageslaenge=500, max_tageslaenge=600,
                          seed=15)
    problem.print_input()

    problem.create_model()
    problem.solve_model()
