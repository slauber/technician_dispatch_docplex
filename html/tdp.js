'use strict';

var xhttp = new XMLHttpRequest();

function processInput() {
    var progress_indicator = document.querySelector('#progress_indicator');
    progress_indicator.style.display = "block";
    var cancel_button = document.querySelector('#btnCancel');
    cancel_button.disabled = false;
    var solve_button = document.querySelector('#btnSolve');
    solve_button.disabled = true;
    var inputs = document.getElementsByTagName("INPUT");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === 'text') {
            inputs[i].disabled = true;
        }
    }

    var techniker = document.querySelector('#techniker').value;
    var auftraege = document.querySelector('#auftraege').value;
    var skills = document.querySelector('#skills').value;
    var seed = document.querySelector('#seed').value;
    var tageslaenge = document.querySelector('#tageslaenge').value;
    var maxTageslaenge = document.querySelector('#maxTageslaenge').value;

    var minDistanz = document.querySelector('#minDistanz').value;
    var maxDistanz = document.querySelector('#maxDistanz').value;
    var minStart = document.querySelector('#minStart').value;
    var maxStart = document.querySelector('#maxStart').value;
    var maxDauer = document.querySelector('#maxDauer').value;
    var eDauer = document.querySelector('#eDauer').value;
    var maxEnde = document.querySelector('#maxEnde').value;
    var eEnde = document.querySelector('#eEnde').value;
    var maxStrafeAuftrag = document.querySelector('#maxStrafeAuftrag').value;
    var eStrafeAuftrag = document.querySelector('#eStrafeAuftrag').value;
    var maxStrafeTechniker = document.querySelector('#maxStrafeTechniker').value;
    var eStrafeTechniker = document.querySelector('#eStrafeTechniker').value;

    var replanning = document.querySelector('#switch-replanning').checked;
    var reZeitpunkt = document.querySelector('#reZeitpunkt').value;
    var reFruesterStart = document.querySelector('#reFruesterStart').value;
    var reSpaetestesEnde = document.querySelector('#reSpaetestesEnde').value;
    var reDauer = document.querySelector('#reDauer').value;
    var reStrafe = document.querySelector('#reStrafe').value;
    var reSkills = document.querySelector('#reSkills').value;


    var advancedSwitch = document.querySelector("#switch-advanced").checked;

    xhttp.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            enableFields();
            var response = JSON.parse(this.responseText);
            if (response.solved === true) {
                appendSolution(response);
                var clear_button = document.querySelector('#btnClear');
                clear_button.disabled = false;
                showToast("Lösung gefunden.");
            } else {
                showToast("Es konnte keine Lösung gefunden werden.");
            }

        } else {
            if (this.status === 500) {
                showToast("Ein Fehler bei der Verarbeitung der Daten ist aufgetreten.");
                cancel();
            }
        }
    };

    xhttp.open("GET",
        "http://localhost:5000/solve?techniker=" + techniker + "&auftraege=" + auftraege +
        "&skills=" + skills + "&tageslaenge=" + tageslaenge + "&maxTageslaenge=" + maxTageslaenge +
        "&seed=" + seed + "&minDistanz=" + minDistanz + "&maxDistanz=" + maxDistanz + "&minStart=" + minStart +
        "&maxStart=" + maxStart + "&maxDauer=" + maxDauer + "&eDauer=" + eDauer + "&maxEnde=" + maxEnde +
        "&eEnde=" + eEnde + "&maxStrafeAuftrag=" + maxStrafeAuftrag + "&eStrafeAuftrag=" + eStrafeAuftrag +
        "&maxStrafeTechniker=" + maxStrafeTechniker + "&eStrafeTechniker=" + eStrafeTechniker + "&advanced=" + advancedSwitch +
        "&replanning=" + replanning + "&reZeitpunkt=" + reZeitpunkt + "&reFruesterStart=" + reFruesterStart + "&reSpaetestesEnde=" + reSpaetestesEnde +
        "&reDauer=" + reDauer + "&reStrafe=" + reStrafe + "&reSkills=" + encodeURIComponent(reSkills),
        true);
    xhttp.send();

}

function toggleAdvanced() {
    var advancedPanel = document.querySelector("#panel-advanced");
    var advancedSwitch = document.querySelector("#switch-advanced");
    if (!advancedSwitch.checked) {
        advancedPanel.style.display = "none";
        resetAdvanced();
        document.querySelector("#switch-replanning").checked = false;
        toggleReplan();
    } else {
        advancedPanel.style.display = "block";
    }
}

function toggleReplan() {
    var replanElements = document.getElementsByClassName("replanning-field");
    var replanSwitch = document.querySelector("#switch-replanning");
    for (var i = 0; i < replanElements.length; i++) {
        replanElements[i].disabled = !replanSwitch.checked;
    }
}

function updateReplanRegex() {
    var skillsetSize = document.querySelector('#skills').value;
    console.log(skillsetSize);
    document.querySelector('#reSkills').pattern = "([01],){" + (skillsetSize - 1) + "}[01]{1}";
}

function enableFields() {
    var progress_indicator = document.querySelector('#progress_indicator');
    progress_indicator.style.display = "none";
    var cancel_button = document.querySelector('#btnCancel');
    cancel_button.disabled = true;
    var solve_button = document.querySelector('#btnSolve');
    solve_button.disabled = false;
    var inputs = document.getElementsByTagName("INPUT");
    for (var i = 0; i < inputs.length; i++) {
        if (inputs[i].type === 'text') {
            inputs[i].disabled = false;
        }
    }
}

function cancel() {
    xhttp.abort();
    enableFields()
}

function resetAdvanced() {
    document.querySelector('#seed').value = "";
    document.querySelector('#minDistanz').value = 0;
    document.querySelector('#maxDistanz').value = 120;
    document.querySelector('#minStart').value = 0;
    document.querySelector('#maxStart').value = 300;
    document.querySelector('#maxDauer').value = 180;
    document.querySelector('#eDauer').value = 60;
    document.querySelector('#maxEnde').value = 120;
    document.querySelector('#eEnde').value = 60;
    document.querySelector('#maxStrafeAuftrag').value = 100;
    document.querySelector('#eStrafeAuftrag').value = 25;
    document.querySelector('#maxStrafeTechniker').value = 100;
    document.querySelector('#eStrafeTechniker').value = 25;
}

function isArray(what) {
    return Object.prototype.toString.call(what) === '[object Array]';
}

/* Funktioniert mit 2D Matrizen und Listen */
function createTable(data) {
    var table_html = "<table class='mdl-data-table'><thead><tr>";
    var is2d = isArray(data[0]);

    for (var i_uber = -1; i_uber < (is2d ? data[0].length : data.length); i_uber++) {
        if (i_uber >= 0) {
            table_html += "<th>" + i_uber + "</th>";
        }
        else {
            table_html += "<th>&nbsp;</th>";
        }
    }
    table_html += "</tr></thead>";

    for (var i_matrix = 0; i_matrix < (is2d ? data.length : 1); i_matrix++) {
        table_html += "<tr>";
        for (var j_matrix = 0; j_matrix < (is2d ? data[0].length : data.length); j_matrix++) {
            if (j_matrix === 0) {
                table_html += "<th>" + (is2d ? i_matrix : "&nbsp;") + "</th>";
            }
            table_html += "<td>" + (is2d ? data[i_matrix][j_matrix] : data[j_matrix]) + "</td>";
        }
        table_html += "</tr>";
    }
    table_html += "</table>";
    return table_html;
}

function appendSolution(result) {
    var d = new Date();
    var ts = d.getTime();

    var solutions = document.querySelector('.solution-container');
    var solution = document.createElement("div");
    var anzRouten = Object.keys(result.outputs.fahrten_pro_techniker_sortiert).length;

    solution.classList.add('tdp-solution-wrapper');

    var html = "<div class=\"tdp-card-wide mdl-card mdl-shadow--4dp\" id='" + ts + "'>";
    html += "<div class=\"mdl-card__title\">";
    html += "<h2 class=\"mdl-card__title-text\">Ergebnis für Seed " + result.inputs.seed + "</h2></div>";
    html += "<div class=\"mdl-card__supporting-text\">";
    if (result.inputs.replanned) {
        html += "<span>Diese Planung wurde mit Replanning durchgeführt</span><br>";
    }
    html += "<span>" + (result.outputs.alle_auftraege_erledigt ?
        "Es konnten alle Aufträge erledigt werden ✅." : "Es konnten nicht alle Aufträge erledigt werden ❌.") + "</span>";

    if (!result.outputs.alle_auftraege_erledigt) {
        html += "<h4>Unerledigte Aufträge</h4><span>" + result.outputs.unerledigte_auftraege + "</span>"
    }

    if (anzRouten > 0) {
        html += "<h4>" + (anzRouten > 1 ? "Routen" : "Route") + "</h4>";
    }

    html += "<ul class=\"tdp-list-item mdl-list\">";
    for (var key in result.outputs.fahrten_pro_techniker_sortiert) {
        if (result.outputs.fahrten_pro_techniker_sortiert.hasOwnProperty(key)) {
            html += "<li class=\"mdl-list__item\"><span class=\"mdl-list__item-primary-content\">";
            html += "<i class=\"material-icons mdl-list__item-icon\">person</i>";
            html += "Techniker " + key + " fährt von seinem Depot ";
            for (var wegpunkt_i = 1; wegpunkt_i < result.outputs.fahrten_pro_techniker_sortiert[key].length - 1; wegpunkt_i++) {
                var auftrag = result.outputs.fahrten_pro_techniker_sortiert[key][wegpunkt_i];
                html += "zu Auftrag " + auftrag + " (Startzeit " + result.outputs.startzeiten[parseInt(auftrag)];
                html += "), danach ";
            }
            html += "wieder in sein Depot.</span></li>"
        }
    }
    html += "</ul>";

    html += "<div class=\"mdl-grid\"><div class=\"mdl-cell\">";
    html += "<h5>Distanzmatrix</h5>" + createTable(result.inputs.distanzmatrix);
    html += "</div></div>";

    html += "<div class=\"mdl-grid\"><div class=\"mdl-cell mdl-cell--6-col\">";
    html += "<h5>Techniker Skills</h5>" + createTable(result.inputs.techniker_skills);
    html += "</div><div class=\"mdl-cell mdl-cell--6-col\">";
    html += "<h5>Auftrag Skills</h5>" + createTable(result.inputs.auftrag_skills);
    html += "</div></div>";

    html += "<div class=\"mdl-grid\"><div class=\"mdl-cell mdl-cell--6-col\">";
    html += "<h5>Frühster Start</h5>" + createTable(result.inputs.fruester_start);
    html += "</div><div class=\"mdl-cell mdl-cell--6-col\">";
    html += "<h5>Spätestes Ende</h5>" + createTable(result.inputs.spaetestes_ende);
    html += "</div></div>";

    html += "<div class=\"mdl-grid\"><div class=\"mdl-cell mdl-cell--6-col\">";
    html += "<h5>Strafkosten Auftrag</h5>" + createTable(result.inputs.strafe_auftrag);
    html += "</div><div class=\"mdl-cell mdl-cell--6-col\">";
    html += "<h5>Strafkosten Techniker</h5>" + createTable(result.inputs.strafe_techniker);
    html += "</div></div>";

    html += "<div class=\"mdl-grid\"><div class=\"mdl-cell mdl-cell--6-col\">";
    html += "<h5>Auftragsdauer</h5>" + createTable(result.inputs.auftragsdauer);
    html += "</div><div class=\"mdl-cell mdl-cell--6-col\">";
    html += "</div></div>";

    /* Zeitstempel */
    html += "<div><div class=\"mdl-card__actions mdl-card--border\">";
    html += "<span class=\"tdp-card-image__filename\">" + d.toLocaleString() + "</span></div>";

    /* Kartenmenü */
    html += "<div class=\"mdl-card__menu\">";
    html += "<button onclick=\"clearSolution(" + ts + ")\"";
    html += "class=\"mdl-button mdl-button--icon mdl-js-button mdl-js-ripple-effect\">";
    html += "<i class=\"material-icons\">clear</i></button></div></div>";

    solution.innerHTML = html;

    solutions.insertBefore(solution, solutions.firstChild);
}

function clearSolution(id) {
    var node = document.getElementById(id).parentElement;
    var parent = node.parentElement;
    parent.removeChild(node);
    if (parent.children.length === 0) {
        clearSolutions();
    }
}

function clearSolutions() {
    var solutions = document.querySelector('.solution-container');
    solutions.innerHTML = "";
    var clear_button = document.querySelector('#btnClear');
    clear_button.disabled = true;
}

function showToast(text) {
    'use strict';
    var snackbarContainer = document.querySelector('#tdp-toast-example');
    var data = {message: text};
    snackbarContainer.MaterialSnackbar.showSnackbar(data);
}
