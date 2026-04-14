import math

import pytest

import temp_monitor
import temp_monitor_client


# ==========================
# Helpers
# ==========================


def build_monitor(readings, max_readings=None):
    if max_readings is None:
        max_readings = len(readings)
    monitor = temp_monitor.init(max_readings)
    for value in readings:
        temp_monitor.add_reading(monitor, value)
    return monitor


BOGOTA_DAY = [8.0, 9.5, 11.0, 13.5, 15.0, 17.5, 19.0, 20.0, 19.5, 18.0, 16.5, 15.0]


# ==========================
# temp_monitor.py (44 puntos)
# ==========================


# init() - 6 puntos
@pytest.mark.points(3)
def test_init_crea_estructura_basica():
    monitor = temp_monitor.init(10)
    assert monitor == {"max": 10, "readings": [], "total": 0.0}


@pytest.mark.points(3)
def test_init_guarda_maximo_correcto():
    monitor = temp_monitor.init(3)
    assert monitor["max"] == 3


# add_reading() - 6 puntos
@pytest.mark.points(2)
def test_add_reading_agrega_temperatura():
    monitor = temp_monitor.init(5)
    temp_monitor.add_reading(monitor, 12.5)
    assert monitor["readings"] == [12.5]


@pytest.mark.points(2)
def test_add_reading_actualiza_total():
    monitor = temp_monitor.init(5)
    temp_monitor.add_reading(monitor, 2.0)
    temp_monitor.add_reading(monitor, 3.5)
    assert math.isclose(monitor["total"], 5.5)


@pytest.mark.points(2)
def test_add_reading_retorna_mismo_diccionario():
    monitor = temp_monitor.init(5)
    returned = temp_monitor.add_reading(monitor, 1.0)
    assert returned is monitor


# count() - 3 puntos
@pytest.mark.points(1.5)
def test_count_en_bogota():
    monitor = build_monitor(BOGOTA_DAY)
    assert temp_monitor.count(monitor) == 12


@pytest.mark.points(1.5)
def test_count_con_una_lectura():
    monitor = build_monitor([7.7], max_readings=4)
    assert temp_monitor.count(monitor) == 1


# average_temp() - 4 puntos
@pytest.mark.points(2)
def test_average_temp_bogota():
    monitor = build_monitor(BOGOTA_DAY)
    assert math.isclose(temp_monitor.average_temp(monitor), 15.208333333333334)


@pytest.mark.points(2)
def test_average_temp_valores_negativos_y_positivos():
    monitor = build_monitor([-2.0, 0.0, 4.0])
    assert math.isclose(temp_monitor.average_temp(monitor), 2.0 / 3.0)


# format_readings() - 5 puntos
@pytest.mark.points(2.5)
def test_format_readings_formato_exacto_bogota():
    monitor = build_monitor(BOGOTA_DAY)
    assert (
        temp_monitor.format_readings(monitor)
        == "[8.0, 9.5, 11.0, 13.5, 15.0, 17.5, 19.0, 20.0, 19.5, 18.0, 16.5, 15.0]"
    )


@pytest.mark.points(2.5)
def test_format_readings_varios_decimales():
    monitor = build_monitor([3.14159, 2.0, 2.5])
    assert temp_monitor.format_readings(monitor) == "[3.14159, 2.0, 2.5]"


# highest_temp() - 4 puntos
@pytest.mark.points(2)
def test_highest_temp_bogota():
    monitor = build_monitor(BOGOTA_DAY)
    assert math.isclose(temp_monitor.highest_temp(monitor), 20.0)


@pytest.mark.points(2)
def test_highest_temp_todos_negativos():
    monitor = build_monitor([-8.0, -2.0, -3.5, -9.1])
    assert math.isclose(temp_monitor.highest_temp(monitor), -2.0)


# coldest_window() - 8 puntos
@pytest.mark.points(2)
def test_coldest_window_bogota_k3():
    monitor = build_monitor(BOGOTA_DAY)
    assert math.isclose(temp_monitor.coldest_window(monitor, 3), 9.5)


@pytest.mark.points(2)
def test_coldest_window_k1_equivale_minimo():
    monitor = build_monitor([6.0, 4.5, 5.0, 7.2])
    assert math.isclose(temp_monitor.coldest_window(monitor, 1), 4.5)


@pytest.mark.points(2)
def test_coldest_window_k_total_equivale_promedio_total():
    readings = [1.0, 3.0, 5.0, 7.0]
    monitor = build_monitor(readings)
    assert math.isclose(temp_monitor.coldest_window(monitor, 4), sum(readings) / 4)


@pytest.mark.points(2)
def test_coldest_window_mejor_ventana_al_medio():
    monitor = build_monitor([20.0, 18.0, 5.0, 4.0, 6.0, 30.0])
    assert math.isclose(temp_monitor.coldest_window(monitor, 3), 5.0)


# longest_rising_streak() - 8 puntos
@pytest.mark.points(2)
def test_longest_rising_streak_bogota():
    monitor = build_monitor(BOGOTA_DAY)
    assert temp_monitor.longest_rising_streak(monitor) == 8


@pytest.mark.points(2)
def test_longest_rising_streak_todas_iguales():
    monitor = build_monitor([2.0, 2.0, 2.0, 2.0])
    assert temp_monitor.longest_rising_streak(monitor) == 1


@pytest.mark.points(2)
def test_longest_rising_streak_estricta_con_empates():
    monitor = build_monitor([1.0, 2.0, 2.0, 2.1, 2.2])
    assert temp_monitor.longest_rising_streak(monitor) == 3


@pytest.mark.points(2)
def test_longest_rising_streak_mejor_racha_en_medio():
    monitor = build_monitor([10.0, 9.0, 8.0, 8.5, 9.0, 9.2, 7.0])
    assert temp_monitor.longest_rising_streak(monitor) == 4


# ================================
# temp_monitor_client.py (6 puntos)
# ================================


@pytest.mark.points(2)
def test_client_lee_n_e_inicializa_monitor(monkeypatch, tmp_path):
    path = tmp_path / "entrada.txt"
    path.write_text("3\n1.1\n1.2\n1.3\n", encoding="utf-8")

    calls = {"init": None}

    def fake_init(n):
        calls["init"] = n
        return {"max": n, "readings": [], "total": 0.0}

    monkeypatch.setattr(temp_monitor_client.temp_monitor, "init", fake_init)
    monkeypatch.setattr(
        temp_monitor_client.temp_monitor,
        "add_reading",
        lambda monitor, t: monitor,
    )
    monkeypatch.setattr(
        temp_monitor_client.temp_monitor,
        "longest_rising_streak",
        lambda monitor: 1,
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: str(path))

    temp_monitor_client.main()

    assert calls["init"] == 3


@pytest.mark.points(2)
def test_client_agrega_temperaturas_en_orden(monkeypatch, tmp_path):
    path = tmp_path / "entrada.txt"
    path.write_text("4\n2.5\n2.0\n1.8\n2.1\n", encoding="utf-8")

    calls = []

    monkeypatch.setattr(temp_monitor_client.temp_monitor, "init", lambda n: {"n": n})
    monkeypatch.setattr(
        temp_monitor_client.temp_monitor,
        "add_reading",
        lambda monitor, t: (calls.append(t) or monitor),
    )
    monkeypatch.setattr(
        temp_monitor_client.temp_monitor,
        "longest_rising_streak",
        lambda monitor: 2,
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: str(path))

    temp_monitor_client.main()

    assert calls == [2.5, 2.0, 1.8, 2.1]


@pytest.mark.points(2)
def test_client_imprime_racha(monkeypatch, tmp_path, capsys):
    path = tmp_path / "entrada.txt"
    path.write_text("1\n9.99\n", encoding="utf-8")

    monkeypatch.setattr(temp_monitor_client.temp_monitor, "init", lambda n: {"n": n})
    monkeypatch.setattr(
        temp_monitor_client.temp_monitor,
        "add_reading",
        lambda monitor, t: monitor,
    )
    monkeypatch.setattr(
        temp_monitor_client.temp_monitor,
        "longest_rising_streak",
        lambda monitor: 7,
    )
    monkeypatch.setattr("builtins.input", lambda _prompt: str(path))

    temp_monitor_client.main()
    out = capsys.readouterr().out

    assert out.strip().endswith("7")
