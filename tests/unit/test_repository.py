from python_template.infrastructure.repository import Repository


def test_initialization(db_mock):
    repo = Repository(db_client=db_mock, a_config_parameter=["test"])
    assert repo is not None
    assert repo.get(1) == "test"


def test_put_and_get(repo):
    item_id = repo.put("new_item")
    assert item_id == 1
    retrieved_item = repo.get(item_id)
    assert retrieved_item == "new_item"


def test_get_nonexistent(repo):
    result = repo.get(999)
    assert result is None


def test_disconnected_db_raises(db_mock):
    db_mock.is_connected.return_value = False
    repo = Repository(db_client=db_mock, a_config_parameter=["test"])
    try:
        repo.get(1)
        raise AssertionError("Expected ConnectionError")
    except ConnectionError as e:
        assert "not connected" in str(e)
