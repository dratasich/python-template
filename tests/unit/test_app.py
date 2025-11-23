from python_template.main import main


def test_main(caplog):
    main()
    assert "Hello from python-template!" in caplog.text
