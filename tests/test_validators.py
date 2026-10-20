from app.validators import validate_status, validate_task_id, validate_title


def test_title_valid():
    assert validate_title("Belajar DevSecOps")


def test_title_kosong_dan_non_string():
    assert not validate_title("   ")
    assert not validate_title(None)
    assert not validate_title(123)


def test_title_terlalu_panjang():
    assert not validate_title("a" * 101)


def test_status():
    assert validate_status("todo")
    assert validate_status("done")
    assert not validate_status("selesai")


def test_task_id():
    assert validate_task_id(1)
    assert not validate_task_id(0)
    assert not validate_task_id("1")
