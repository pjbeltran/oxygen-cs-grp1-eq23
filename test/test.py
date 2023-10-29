import sys
sys.path.append('../src')

import main

def test_import_main():
    try:
        assert "Main" in dir(main)
        print("Import successful.")
    except Exception as e:
        assert False, f"Import failed: {dir(main.Main)}"

def test_host_variable():
    mockMain = main.Main(
        host="test-host",
        token="test-token",
        tickets=2,
        t_max=30,
        t_min=18,
        database="test-database"
    )

    assert "test-host", f"{mockMain.HOST}"

def test_token_variable():
    mockMain = main.Main(
        host="test-host",
        token="test-token",
        tickets=2,
        t_max=30,
        t_min=18,
        database="test-database"
    )

    assert "test-token", f"{mockMain.TOKEN}"    

def test_T_MAX_variable():
    mockMain = main.Main(
        host="test-host",
        token="test-token",
        tickets=2,
        t_max=30,
        t_min=18,
        database="test-database"
    )

    assert 30, f"{mockMain.T_MAX}"       

def test_T_MIN_variable():
    mockMain = main.Main(
        host="test-host",
        token="test-token",
        tickets=2,
        t_max=30,
        t_min=18,
        database="test-database"
    )

    assert 18, f"{mockMain.T_MIN}"       

if __name__ == '__main__':
    pytest.main()
