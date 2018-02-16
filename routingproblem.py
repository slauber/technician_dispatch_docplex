import json
from typing import Dict, List

import numpy as np
from docplex.mp.model import Model
from docplex.mp.solution import SolveSolution


class Auftrag:
    """Diese Klasse ist für zusätzliche Aufträge, die beim Replanning zum Tragen kommen, bestimmt."""

    fruheste_start_zeit: int
    dauer: int
    spaeteste_end_zeit: int
    strafe: int
    skills: np.array

    def __init__(self, fruehste_start_zeit, dauer, spaeteste_end_zeit, strafe, skills):
        """
        :param fruehste_start_zeit: int (muss so gewählt sein, dass fruehste_start_zeit + dauer + spaeteste_end_zeit < h_max)
        :param dauer: int (Dauer des Auftrags)
        :param spaeteste_end_zeit: int (muss so gewählt sein, dass fruehste_start_zeit + dauer + spaeteste_end_zeit < h_max)
        :param strafe: int (Strafe pro Minute über der spätesten Endzeit)
        :param skills: np.array (Länge muss mindestens ANZ_SKILLS des Problems entsprechen)
        """

        if fruehste_start_zeit + dauer > spaeteste_end_zeit:
            raise ValueError("Späteste Endzeit liegt zu früh")

        self.fruehste_start_zeit = fruehste_start_zeit
        self.dauer = dauer
        self.spaeteste_end_zeit = spaeteste_end_zeit
        self.strafe = strafe
        self.skills = skills

    def __str__(self):
        return '[Auftrag - Frühste Startzeit {}, Dauer {}, späteste Endzeit {}, Strafe {}, Skills {}]'.format(
            self.fruehste_start_zeit, self.dauer
            , self.spaeteste_end_zeit, self.strafe, self.skills)


class ReplanningDaten:
    """Diese Klasse enthält Daten, die für das Replanning eingesetzt werden"""
    start_zeit: np.array
    x: np.array

    def __init__(self, start_zeit, x):
        """Initialisierung mit vorberechneten Startzeiten und Übergängen zum Replanningzeitpunkt

        :param start_zeit: np.array (vorberechnete Startzeiten)
        :param x: np.array (vorberechnete Übergänge)
        """
        self.start_zeit = start_zeit
        self.x = x

    def __str__(self):
        return "Startzeiten:\n{}\nAbgeschlossene Fahrten".format(self.start_zeit, self.x)


class JsonAntwort:
    """
    Hilfsklasse für die JSON Ausgabe
    """

    class Inputs:
        distanzmatrix: list
        fruester_start: list
        auftragsdauer: list
        spaetestes_ende: list
        auftrag_skills: list
        strafe_auftrag: list
        strafe_techniker: list
        techniker_skills: list
        seed: int
        replanned: int

        def __init__(self, distanzmatrix, fruester_start, auftragsdauer, spaetestes_ende, auftrag_skills,
                     strafe_auftrag, strafe_techniker, techniker_skills, seed, replanned):
            self.distanzmatrix = distanzmatrix
            self.fruester_start = fruester_start
            self.auftragsdauer = auftragsdauer
            self.spaetestes_ende = spaetestes_ende
            self.auftrag_skills = auftrag_skills
            self.strafe_auftrag = strafe_auftrag
            self.strafe_techniker = strafe_techniker
            self.techniker_skills = techniker_skills
            self.seed = seed
            self.replanned = replanned

    class Outputs:
        alle_auftraege_erledigt: bool
        fahrten_pro_techniker_sortiert: dict
        startzeiten: dict
        unerledigte_auftraege: list
        solution: str

        def __init__(self, alle_auftraege_erledigt, fahrten_pro_techniker_sortiert, startzeiten, unerledigte_auftraege,
                     solution):
            self.alle_auftraege_erledigt = alle_auftraege_erledigt
            self.fahrten_pro_techniker_sortiert = fahrten_pro_techniker_sortiert
            self.startzeiten = startzeiten
            self.unerledigte_auftraege = unerledigte_auftraege
            self.solution = solution

    solved: bool
    inputs: Inputs
    outputs: Outputs

    def __init__(self, distanzmatrix, fruester_start, auftragsdauer, spaetestes_ende, auftrag_skills, strafe_auftrag,
                 strafe_techniker, techniker_skills, seed,
                 alle_auftraege_erledigt, fahrten_pro_techniker_sortiert, startzeiten, unerledigte_auftraege, solution,
                 solved, replanned=False):
        self.solved = solved
        self.inputs = self.Inputs(distanzmatrix, fruester_start, auftragsdauer, spaetestes_ende, auftrag_skills,
                                  strafe_auftrag, strafe_techniker, techniker_skills, seed, replanned)
        self.outputs = self.Outputs(alle_auftraege_erledigt, fahrten_pro_techniker_sortiert, startzeiten,
                                    unerledigte_auftraege, solution)

    def get_json(self):
        return json.dumps({'solved': self.solved, 'inputs': self.inputs.__dict__, 'outputs': self.outputs.__dict__})


class RoutingProblem:
    """Diese Klasse umfasst den gesamten Simulator des Technician Dispatch Problems"""
    DISTANZMATRIX: np.array
    TECHNIKER_HAT_SKILL: np.array

    AUFTRAGSDAUER: np.array
    FRUESTER_START: np.array
    SPAETESTES_ENDE: np.array
    AUFTRAG_BRAUCHT_SKILL: np.array

    H: int  # Reguläre Arbeitszeit
    H_max: int  # Maximale Arbeitszeit (harte Grenze)

    STRAFE_AUFTRAG: np.array
    STRAFE_TECHNIKER: np.array

    TRANSPORT_KOSTEN = 0.15  # Betriebskosten pro Zeiteinheit während der Fahrt zwischen zwei Standorten

    GEWICHT_STRAFE_AUFTRAG_UNERFUELLT = 10000  # XL
    GEWICHT_STRAFE_AUFTRAG = 1000  # L
    GEWICHT_STRAFE_TECHNIKER = 100  # M
    GEWICHT_TRANSPORT_KOSTEN = 1  # S

    ANZ_TECHNIKER: int
    ANZ_AUFTRAEGE: int
    ANZ_WEGPUNKTE: int
    ANZ_SKILLS: int

    SEED: int
    REPLANNED = False

    mdl: Model
    solution: SolveSolution

    x: {}
    start_zeit = []

    alle_auftraege_erledigt = False
    fahrten_pro_techniker_sortiert = {}
    startzeiten = {}
    unerledigte_auftraege = []

    def __init__(self, anz_techniker: int = None, anz_auftraege: int = None, anz_skills: int = None,
                 tageslaenge: int = None, max_tageslaenge: int = None, seed: int = None):
        """
        :param anz_techniker: int (Anzahl Techniker)
        :param anz_auftraege: int (Anzahl Aufträge)
        :param anz_skills: int (Länge der gewünschten Skillarrays)
        :param tageslaenge: int (nach dieser Länge wird für jeden Techniker pro Minute seine Strafkosten veranschlagt)
        :param max_tageslaenge: int (wird niemals überschritten, zu dieser Zeit muss jeder Techniker in seinem Depot sein)
        :param seed: int (Initialisierung für PRNG)
        """
        self.solution = None
        self.alle_auftraege_erledigt = False
        self.fahrten_pro_techniker_sortiert = {}
        self.startzeiten = {}
        self.unerledigte_auftraege = []
        self.mdl = None
        self.x = {}
        self.start_zeit = []

        if (anz_techniker and anz_auftraege and anz_skills and tageslaenge and max_tageslaenge):
            self.daten_generieren(anz_techniker, anz_auftraege, anz_skills, tageslaenge, max_tageslaenge, seed)

    def __str__(self):
        if hasattr(self, "ANZ_WEGPUNKTE"):
            return """[RoutingProblem

[Modell]
Distanzmatrix:\n{}\n
Frühste Startzeit: \t{}
Auftragsdauer: \t\t{}
Späteste Endzeit: \t{}
Technikerskills:
{}
Auftragskills:
{}
Seed: {}

]
        """.format(self.DISTANZMATRIX, self.FRUESTER_START, self.AUFTRAGSDAUER, self.SPAETESTES_ENDE,
                   self.TECHNIKER_HAT_SKILL, self.AUFTRAG_BRAUCHT_SKILL, self.SEED)
        else:
            return '[RoutingProblem\n\n[Modell]\nNicht vorhanden\n\n]'


    def daten_generieren(self, anz_techniker: int, anz_auftraege: int, anz_skills: int,
                         tageslaenge: int, max_tageslaenge: int, seed: int = None, min_distanz: int = 0,
                         max_distanz: int = 150,
                         min_start: int = 0, max_start: int = 300, max_dauer: int = 180, e_dauer=60,
                         max_ende: int = 120,
                         e_ende: int = 60, max_strafe_auftrag: int = 100, e_strafe_auftrag: int = 25,
                         max_strafe_techniker: int = 100,
                         e_strafe_techniker: int = 25):
        """Initialisiert die Ausgangsdaten, die später zur Modellgenerierung herangezogen werden.

        :param anz_techniker: int (Anzahl Techniker)
        :param anz_auftraege: int (Anzahl Aufträge)
        :param anz_skills: int (Länge der gewünschten Skillarrays)
        :param tageslaenge: int (nach dieser Länge wird für jeden Techniker pro Minute seine Strafkosten veranschlagt)
        :param max_tageslaenge: int (wird niemals überschritten, zu dieser Zeit muss jeder Techniker in seinem Depot sein)
        :param seed: int (Initialisierung für PRNG)
        :param min_distanz: int (minimale Distanz für die Distanzmatrix in Minuten)
        :param max_distanz: int (maximale Distanz für die Distanzmatrix in Minuten)
        :param min_start: int (minimaler frühster Startzeitpunkt für Aufträge)
        :param max_start: int (maximaler frühster Startzeitpunkt für Aufträge)
        :param max_dauer: int (maximale Dauer eines Auftrags (binomialverteilt))
        :param e_dauer: int (Erwartungswert der Dauer eines Auftrags (binomialverteilt))
        :param max_ende: int (maximale Pufferzeit im Wartungsfenster des Auftrags (binomialverteilt))
        :param e_ende: int (Erwartungswert der Pufferzeit im Wartungsfenster des Auftrags (binomialverteilt))
        :param max_strafe_auftrag: int (maximale Strafe pro Minute außerhalb des Wartungsfensters des Auftrags (binomialverteilt))
        :param e_strafe_auftrag: int (Erwartungswert der Strafe pro Minute außerhalb des Wartungsfensters des Auftrags (binomialverteilt))
        :param max_strafe_techniker: int (maximale Strafe pro Minute außerhalb der Tagesdauer des Technikers (binomialverteilt))
        :param e_strafe_techniker:  int (Erwartungswert der  Strafe pro Minute außerhalb der Tagesdauer des Technikers (binomialverteilt))
        """

        anz_wegpunkte = anz_techniker + anz_auftraege

        # Wenn kein Seed gegeben ist, ziehe einen und speichere ihn
        if not seed:
            seed = np.random.randint(2 ** 32 - 1)
        np.random.seed(seed)
        self.SEED = seed

        # Gib eine symmetrische Distanzmatrix mit gegebenen Parametern aus
        distanzmatrix = np.random.randint(min_distanz, int(max_distanz / 2), size=(anz_wegpunkte, anz_wegpunkte))
        distanzmatrix = (distanzmatrix + distanzmatrix.T)
        np.fill_diagonal(distanzmatrix, 0)
        self.DISTANZMATRIX = distanzmatrix

        # Setze Tageslänge
        self.H = tageslaenge
        self.H_max = max_tageslaenge

        # Generiere Skillsets, binomialverteilt
        self.TECHNIKER_HAT_SKILL = np.random.binomial(n=1, p=(2 / 3), size=(anz_techniker, anz_skills))
        self.AUFTRAG_BRAUCHT_SKILL = np.random.binomial(n=1, p=(1 / 3), size=(anz_auftraege, anz_skills))

        # Generiere frühste Auftragsstartzeiten, gleichverteilt
        self.FRUESTER_START = np.random.randint(min_start, max_start, size=anz_auftraege)

        # Generiere Auftragsdauern, binomialverteilt
        self.AUFTRAGSDAUER = np.random.binomial(n=max_dauer, p=(e_dauer / max_dauer), size=anz_wegpunkte)
        for i in range(anz_techniker):
            self.AUFTRAGSDAUER[anz_auftraege + i] = 0

        # Generiere Pufferzeit im Wartungsfenster der Aufträge, binomialverteilt
        self.SPAETESTES_ENDE = np.zeros(anz_auftraege, dtype=int)
        for i in range(anz_auftraege):
            self.SPAETESTES_ENDE[i] = self.FRUESTER_START[i] + self.AUFTRAGSDAUER[i] + np.random.binomial(n=max_ende,
                                                                                                  p=(e_ende / max_ende))
        # Generiere Strafzahlungen, binomialverteilt
        self.STRAFE_AUFTRAG = np.random.binomial(n=max_strafe_auftrag, p=(e_strafe_auftrag / max_strafe_auftrag),
                                                 size=anz_auftraege)
        self.STRAFE_TECHNIKER = np.random.binomial(n=max_strafe_techniker,
                                                   p=(e_strafe_techniker / max_strafe_techniker), size=anz_techniker)

        self.ANZ_AUFTRAEGE = anz_auftraege
        self.ANZ_SKILLS = anz_skills
        self.ANZ_TECHNIKER = anz_techniker
        self.ANZ_WEGPUNKTE = anz_wegpunkte

        # Überprüfe, ob die Techniker die Aufträge mit ihren Skillsets ausführen können
        skill_check = np.zeros(self.ANZ_AUFTRAEGE, dtype=bool)
        for techniker in self.TECHNIKER_HAT_SKILL:
            for i, auftrag in enumerate(self.AUFTRAG_BRAUCHT_SKILL):
                skill_check[i] = skill_check[i] or np.logical_or(techniker, np.logical_not(auftrag)).all()
        if (not skill_check.all()):
            print("Warnung - Skillset-Daten sind inkonsistent, es wird ein neuer Seed ({}) verwendet".format(seed + 1))
            self.daten_generieren(anz_techniker, anz_auftraege, anz_skills, tageslaenge, max_tageslaenge, seed + 1)

    def modell_aus_daten_aufstellen(self, replanning_daten=None, neuer_auftrag: Auftrag = None):
        """Stellt das Linearprogramm aus den vorinitialisierten Daten auf

        Wichtig: Zugriff auf die Aufträge und Depots sind in gemeinsamen Arrays x und DISTANZMATRIX.
            Das bedeutet, dass man für den Zugriff auf Depots den Index um ANZ_AUFTRAEGE inkrementieren muss.
            Beispiel für die Fahrt von Techniker 0 von Auftrag 2 in sein Depot: x[(0, 2, ANZ_AUFTRAGE+0)].

            Die Indizierung von x ist speziell, der Zugriff muss über ein Python Set aus Indizes bestehen, daher die
            etwas merkwürdige Syntax x[()]

        Indizes beginnen immer bei 0.

        1. Das Modell um einen potenziellen Replanning-Auftrag erweitert
        2. Die Zielfunktion wird mit 4 KPIs erstellt
        3. Die Constraints werden hinzugefügt

        :param replanning_daten:
        :param neuer_auftrag:
        """
        mdl = Model(name="Technician Dispatch Problem")

        # Wenn ein neuer Auftrag hinzukommt -> Replanning, dann passe die Arrays und Matrizen an
        if neuer_auftrag:
            # Inkrementiere Anzahlen
            self.ANZ_AUFTRAEGE += 1
            self.ANZ_WEGPUNKTE += 1

            # Füge Auftrag an letzer Stelle hinzu
            self.AUFTRAG_BRAUCHT_SKILL = np.vstack((self.AUFTRAG_BRAUCHT_SKILL, np.array(neuer_auftrag.skills)))
            self.STRAFE_AUFTRAG = np.hstack((self.STRAFE_AUFTRAG, np.array(neuer_auftrag.strafe)))
            self.FRUESTER_START = np.hstack((self.FRUESTER_START, np.array(neuer_auftrag.fruehste_start_zeit)))
            self.AUFTRAGSDAUER = np.hstack((self.AUFTRAGSDAUER[:self.ANZ_AUFTRAEGE - 1], np.array(neuer_auftrag.dauer),
                                            self.AUFTRAGSDAUER[self.ANZ_AUFTRAEGE - 1:]))
            self.SPAETESTES_ENDE = np.hstack(
                (self.SPAETESTES_ENDE, np.array(neuer_auftrag.spaeteste_end_zeit, dtype=int)))

            # Generiere neue Distanzen für den neuen Wegpunkt
            zufallsdistanzen = np.random.randint(0, 120, size=self.ANZ_WEGPUNKTE)
            zufallsdistanzen[self.ANZ_AUFTRAEGE - 1] = 0
            self.DISTANZMATRIX = np.insert(self.DISTANZMATRIX, self.ANZ_AUFTRAEGE - 1,
                                           np.delete(zufallsdistanzen, self.ANZ_AUFTRAEGE - 1), 0)
            self.DISTANZMATRIX = np.insert(self.DISTANZMATRIX, self.ANZ_AUFTRAEGE - 1, zufallsdistanzen, 1)

        # Abkürzung für loop ranges
        r_auftraege = range(self.ANZ_AUFTRAEGE)
        r_wegpunkte = range(self.ANZ_WEGPUNKTE)
        r_techniker = range(self.ANZ_TECHNIKER)
        r_skills = range(self.ANZ_SKILLS)

        # Entscheidungsvariablen
        x = mdl.binary_var_cube(self.ANZ_TECHNIKER, self.ANZ_WEGPUNKTE, self.ANZ_WEGPUNKTE, name="Fahrt")
        start_zeit = mdl.integer_var_list(self.ANZ_WEGPUNKTE, name="Startzeit")

        # Entscheidungsausdrücke
        #
        # Summe der Strafkosten für verspätetet erledigte Aufträge
        strafkosten_auftrag_verspaetet = mdl.sum(
            mdl.max(0, start_zeit[i] + self.AUFTRAGSDAUER[i] - self.SPAETESTES_ENDE[i]) * self.STRAFE_AUFTRAG[i]
            for i in r_auftraege
        )
        mdl.add_kpi(strafkosten_auftrag_verspaetet, "Strafkosten Auftrag verspätet")

        # Summe der Strafkosten für unerledigte Aufträge
        strafkosten_auftrag_unerfuellt = mdl.sum(
            mdl.max((1 - start_zeit[i]) * 10000, 0) * self.STRAFE_AUFTRAG[i]
            for i in r_auftraege
        )
        mdl.add_kpi(strafkosten_auftrag_unerfuellt, "Strafkosten Auftrag unerfüllter")

        # Summe der Strafkosten für verspätetet zurückgekehrte Techniker
        strafkosten_techniker = mdl.sum(
            mdl.max(0, start_zeit[i] + self.AUFTRAGSDAUER[i], self.DISTANZMATRIX[i][m + self.ANZ_AUFTRAEGE] - self.H)
            * self.STRAFE_TECHNIKER[m] * x[(m, i, m + self.ANZ_AUFTRAEGE)]
            for i in r_auftraege
            for m in r_techniker
        )
        mdl.add_kpi(strafkosten_techniker, "Strafkosten Techniker")

        # Summe der Transportkosten
        transportkosten = mdl.sum(
            x[(m, i, j)] * self.DISTANZMATRIX[i][j] * self.TRANSPORT_KOSTEN
            for m in r_techniker
            for i in r_wegpunkte
            for j in r_wegpunkte
        )
        mdl.add_kpi(transportkosten, "Transportkosten")

        # Gewichteter Entscheidungsausdruck
        mdl.minimize(
            strafkosten_auftrag_verspaetet * self.GEWICHT_STRAFE_AUFTRAG + strafkosten_techniker * self.GEWICHT_STRAFE_TECHNIKER +
            self.GEWICHT_STRAFE_AUFTRAG_UNERFUELLT * strafkosten_auftrag_unerfuellt
        )

        # Constraints
        #
        # Startzeit eines Auftrags muss nach frühestem Startpunkt liegen
        for i in r_auftraege:
            mdl.add_if_then(
                mdl.sum(
                    x[(m, j, i)]
                    for m in r_techniker
                    for j in r_wegpunkte
                ) >= 1,
                self.FRUESTER_START[i] <= start_zeit[i]
            )

        # Startzeit und Auftragsdauer müssen vor H_max enden
        mdl.add_constraints(
            start_zeit[i] + self.AUFTRAGSDAUER[i] <= self.H_max
            for i in r_auftraege
        )

        # Wenn eine Fahrt von einem Auftrag zu einem Depot stattfindet, dann muss die Ankunftszeit vor H_max liegen
        for i in r_auftraege:
            for m in r_techniker:
                mdl.add_if_then(
                    x[(m, i, m + self.ANZ_AUFTRAEGE)] == 1,
                    start_zeit[i] + self.AUFTRAGSDAUER[i] + self.DISTANZMATRIX[i][
                        m + self.ANZ_AUFTRAEGE] <= self.H_max
                )

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
            for l in r_auftraege
            if l != j
        )

        # Wenn er von einem Auftrag wegfährt, dann muss er dort auch hingefahren sein
        mdl.add_constraints(
            x[(m, j, l)] <= mdl.sum([
                x[(m, t, j)]
                for t in r_wegpunkte
                if j != t
            ]
            )
            for m in r_techniker
            for j in r_auftraege
            for l in r_wegpunkte
            if l != j
        )

        # Jeder Auftrag mit positiver Startzeit muss angefahren worden sein
        for i in r_auftraege:
            mdl.add_if_then(
                start_zeit[i] >= 1,
                mdl.sum(
                    [
                        x[(m, j, i)]
                        for m in r_techniker
                        for j in r_wegpunkte
                    ]
                ) == 1
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

        # Setze vorberechnete Replanning-Daten als constraint fix
        if replanning_daten:
            self.REPLANNED = True

            mdl.add_constraints(
                start_zeit[i] == replanning_daten.start_zeit[i]
                for i in range(self.ANZ_AUFTRAEGE - 1)
                if replanning_daten.start_zeit[i] != 0
            )

            mdl.add_constraints(
                x[(m, i, j)] == replanning_daten.x[m][i][j]
                for m in r_techniker
                for i in range(self.ANZ_AUFTRAEGE - 1)
                for j in range(self.ANZ_AUFTRAEGE - 1)
                if replanning_daten.x[m][i][j] != 0
            )
        else:
            self.REPLANNED = False

        # Speichere Modell
        self.x = x
        self.start_zeit = start_zeit
        self.mdl = mdl

    def solve_model(self, timeout: int = 120):
        """Startet den Solver

        :param timeout: int (timeout in s, nach dem die Optimierung abgebrochen wird)
        """
        self.mdl.set_time_limit(timeout)
        self.mdl.solve()
        self.solution = self.mdl.solution

        # Datenaufbereitung zur einfacheren Verwendung
        if self.solution:
            solution_dict = self.solution.as_dict()

            # Fahrten pro Techniker zugreifbar machen
            fahrten_pro_techniker: Dict[int, List] = {}
            for m in range(self.ANZ_TECHNIKER):
                for i in range(self.ANZ_WEGPUNKTE):
                    for j in range(self.ANZ_WEGPUNKTE):
                        if 'Fahrt_{}_{}_{}'.format(m, i, j) in solution_dict:
                            if m in fahrten_pro_techniker:
                                fahrten_pro_techniker[m].append((i, j))
                            else:
                                fahrten_pro_techniker[m] = [(i, j)]

            # Fahrten pro Techniker in korrekter Reihenfolge ausgeben
            self.fahrten_pro_techniker_sortiert = {}
            for techniker, fahrten in fahrten_pro_techniker.items():
                current_node = techniker + self.ANZ_AUFTRAEGE
                self.fahrten_pro_techniker_sortiert[techniker] = [current_node]
                while True:
                    next_node = None
                    i = 0
                    while (next_node is None):
                        if fahrten[i][0] == current_node:
                            next_node = fahrten[i][1]
                        else:
                            i = i + 1

                    self.fahrten_pro_techniker_sortiert[techniker].append(next_node)
                    current_node = next_node
                    if (current_node == techniker + self.ANZ_AUFTRAEGE):
                        break

            # Überprüfe, ob alle Fahrten angetreten wurden
            self.alle_auftraege_erledigt = set(["Startzeit_{}".format(i) for i in range(self.ANZ_AUFTRAEGE)]).issubset(
                set(self.solution.as_dict().keys()))

            # Ermittle unerledigte Aufträge
            self.unerledigte_auftraege = []
            if not self.alle_auftraege_erledigt:
                restauftraege = [item for item in set(["Startzeit_{}".format(i) for i in range(self.ANZ_AUFTRAEGE)]) if
                                 item not in set(self.solution.as_dict().keys())]
                for auftrag in restauftraege:
                    self.unerledigte_auftraege.append(int(auftrag[10:]))

    def print_solution(self, print_stats=False, print_details=False, print_lp=False):
        """Gibt die Lösung auf der command line aus
        :param print_stats: bool (gibt erweiterte Informationen des Solvers aus)
        :param print_details: bool (gibt alle Lösungswerte und das Linearprogramm aus)
        """
        if print_stats:
            print(self.mdl.get_solve_details())
        if self.solution:
            if print_details:
                print(self.solution)
            if print_lp:
                print(self.mdl.export_as_lp_string())

            for techniker, fahrten in self.fahrten_pro_techniker_sortiert.items():
                techniker_str = "Techniker {} fährt von seinem Depot ".format(techniker)
                for fahrt in fahrten:
                    if fahrt != self.ANZ_AUFTRAEGE + techniker:
                        techniker_str = techniker_str + "zu Auftrag {} (Startzeit: {}) ".format(fahrt,
                                                                                                self.solution.as_dict()[
                                                                                                    "Startzeit_{}".format(
                                                                                                        fahrt)])
                techniker_str = techniker_str + "und zurück zu seinem Depot."
                print(techniker_str)

            if self.alle_auftraege_erledigt:
                print("Es wurden alle Aufträge in der Periode erledigt")
            else:
                print("Es konnten nicht alle Aufträge in der Periode erledigt werden.")
                print(self.unerledigte_auftraege)

        else:
            print("Es gibt keine Lösung")
            return json.dumps(
                {
                    "solved": False
                }
            )

    def json_ausgabe(self):
        """Formatiert die Daten in JSON

        :return: str (enthält in JSON kodierte Daten, die vom Webserver ausgeliefert werden)
        """
        if self.solution:
            start_zeit_geloest = self.solution.get_values(self.start_zeit[i] for i in range(self.ANZ_AUFTRAEGE))
            startzeiten = {i: start_zeit_geloest[i] for i in range(self.ANZ_AUFTRAEGE)}

            json_data = JsonAntwort(
                solved=True,
                distanzmatrix=self.DISTANZMATRIX.tolist(),
                fruester_start=self.FRUESTER_START.tolist(),
                auftragsdauer=self.AUFTRAGSDAUER.tolist(),
                spaetestes_ende=self.SPAETESTES_ENDE.tolist(),
                techniker_skills=self.TECHNIKER_HAT_SKILL.tolist(),
                auftrag_skills=self.AUFTRAG_BRAUCHT_SKILL.tolist(),
                strafe_auftrag=self.STRAFE_AUFTRAG.tolist(),
                strafe_techniker=self.STRAFE_TECHNIKER.tolist(),
                seed=self.SEED,
                alle_auftraege_erledigt=self.alle_auftraege_erledigt,
                fahrten_pro_techniker_sortiert=self.fahrten_pro_techniker_sortiert,
                startzeiten=startzeiten,
                unerledigte_auftraege=sorted(self.unerledigte_auftraege),
                solution=str(self.solution),
                replanned=self.REPLANNED
            )

            return json_data.get_json()
        else:
            json_data = {"solved": False}
            return json.dumps(json_data)


    def parameter_zum_zeitpunkt(self, t: int):
        """Ermittle den Zustand zum Zeitpunkt t, um ihn für das Replanning verwenden zu können.
        Sofern eine Fahrt bereits angetreten wurde, wird diese auch nicht mehr geändert.

        Beispiel: Ein Auftrag (Dauer 15) wurde um 70 begonnen. Die Eingabe dieser Funktion sei t=96, der Techniker ist
        dementsprechend schon zu seinem nächsten Auftrag unterwegs. Dieser Auftrag wird als gesetzt betrachtet und ist
        somit als erledigt gekennzeichnet, obwohl er beispielsweise erst um 130 beginnt.

        :param t: int (gewünschter Zeitpunkt, zu dem die Daten ermittelt werden sollen)
        :return: Replanning_Daten (enthält die Liste aller Fahrten und Startzeiten, die bereits erledigt wurden
        """
        if self.solution:
            done_matrix = np.zeros((self.ANZ_TECHNIKER, self.ANZ_WEGPUNKTE, self.ANZ_WEGPUNKTE), dtype=bool)
            tatsaechliche_start_zeit = np.zeros(self.ANZ_AUFTRAEGE, dtype=int)

            for techniker, auftraege in self.fahrten_pro_techniker_sortiert.items():
                letzter_auftrag = techniker + self.ANZ_AUFTRAEGE
                for aktueller_auftrag in auftraege:
                    if aktueller_auftrag is not techniker + self.ANZ_AUFTRAEGE:
                        abfahrt = self.solution.get_value(self.start_zeit[letzter_auftrag]) + self.AUFTRAGSDAUER[
                            letzter_auftrag]
                        if abfahrt < t:
                            tatsaechliche_start_zeit[aktueller_auftrag] = self.solution.get_value(
                                self.start_zeit[aktueller_auftrag])
                            done_matrix[techniker, letzter_auftrag, aktueller_auftrag] = True
                    letzter_auftrag = aktueller_auftrag
            rp_daten = ReplanningDaten(tatsaechliche_start_zeit, done_matrix)
            return rp_daten
        else:
            raise Exception('No solution available to analyze')



if __name__ == '__main__':
    problem = RoutingProblem(anz_techniker=2, anz_auftraege=2, anz_skills=2, tageslaenge=400, max_tageslaenge=500)

    problem.modell_aus_daten_aufstellen()

    problem.solve_model()
    problem.print_solution(print_details=False, print_stats=False)

    replanning_um_200 = problem.parameter_zum_zeitpunkt(200)
    neuer_auftrag_200 = Auftrag(195, 15, 270, 10, np.array([1, 0]))
    print('\nNeuer Auftrag: ', neuer_auftrag_200)
    print('Replanning erfolgt zur t=200\n')
    problem.modell_aus_daten_aufstellen(replanning_daten=replanning_um_200, neuer_auftrag=neuer_auftrag_200)

    problem.solve_model()
    problem.print_solution(print_details=False, print_stats=False)

    print('Replanning erfolgt zur t=300\n')
    replanning_um_300 = problem.parameter_zum_zeitpunkt(300)
    neuer_auftrag_300 = Auftrag(298, 15, 390, 5, np.array([1, 0]))
    problem.modell_aus_daten_aufstellen(replanning_um_300, neuer_auftrag_300)

    problem.solve_model()
    problem.print_solution(print_details=False, print_stats=False)
