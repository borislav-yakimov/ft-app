import pytest
from dependencies import get_session
from main import app
from models import ProactiveLTV, ProactivePredictions
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from starlette.testclient import TestClient

# Create a test database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override the get_session dependency to use the test database
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_session] = override_get_db


client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)


def test_export_xlsx(setup_database):
    with TestingSessionLocal() as session:
        session.add_all(
            [
                ProactiveLTV(
                    user_id="user1",
                    plan="Plan A",
                    region="Region 1",
                    currency="USD",
                    position="Position 1",
                    ltv_horizon="1 year",
                    ltv=100.0,
                ),
                ProactivePredictions(
                    user_id="user1",
                    Plan="Plan A",
                    Probability=0.9,
                    b2c_product_currency_bookkeeping="USD",
                    geo_billing_b2c_marketing_region_bookkeeping="Region 1",
                    rollup_user_position_bookkeeping="Position 1",
                    student_flag_bookkeeping=True,
                    visa_payment_method_flag_bookkeeping=False,
                ),
            ]
        )
        session.commit()

    # Make a request to the export_xlsx endpoint
    response = client.get("/offers/export-xlsx")

    # Check the response status code
    assert response.status_code == 200

    # Check the response headers
    assert response.headers["Content-Disposition"] == "attachment; filename=prediction_records.xlsx"

    # Check the response content type
    assert response.headers["Content-Type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

    # Check the response content (you can add more detailed checks here if needed)
    assert response.content is not None
