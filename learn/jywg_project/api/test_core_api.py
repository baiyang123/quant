import datetime
import os

from learn.jywg_project.emtl.core import login, query_funds_flow, create_order


def test_login():
    validate_key = login(os.getenv("EM_USERNAME", ""), os.getenv("EM_PASSWORD", ""))
    print(validate_key)
    assert validate_key
    assert len(validate_key) == len("b91d8012-b70b-4265-bb5d-f79442531017")


def test_query_funds_flow():
    end_date = datetime.datetime.now(datetime.timezone.utc)
    start_date = end_date - datetime.timedelta(30)
    st = start_date.strftime("%Y-%m-%d")
    et = end_date.strftime("%Y-%m-%d")

    resp = query_funds_flow(100, st, et)
    print(resp)
    assert resp
    assert resp["Status"] == 0


def test_create_order():
    resp = create_order("000002", "B", "SA", 5.01, 100)
    assert resp
    assert resp["Status"] in (0, -1)


if __name__ == '__main__':
    test_login()
    test_query_funds_flow()
    test_create_order()