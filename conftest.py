POINTS_BY_TEST = {}


def pytest_configure(config):
    config.addinivalue_line("markers", "points(value): define puntaje del test")


def pytest_collection_modifyitems(items):
    POINTS_BY_TEST.clear()
    for item in items:
        marker = item.get_closest_marker("points")
        POINTS_BY_TEST[item.nodeid] = float(marker.args[0]) if marker else 0.0


def pytest_terminal_summary(terminalreporter):
    passed_reports = terminalreporter.stats.get("passed", [])
    passed_nodeids = {
        report.nodeid
        for report in passed_reports
        if getattr(report, "when", None) == "call"
    }

    earned = sum(POINTS_BY_TEST.get(nodeid, 0.0) for nodeid in passed_nodeids)
    possible = sum(POINTS_BY_TEST.values())

    terminalreporter.write_sep("=", "Calificacion")
    terminalreporter.write_line(f"Puntos obtenidos: {earned:.2f}/{possible:.2f}")
