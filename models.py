from datetime import datetime
from typing import List, Optional

from decouple import config
from fastapi import Form
from pydantic import BaseModel, EmailStr, condecimal
from sqlalchemy.orm import DeclarativeBase
from sqlmodel import Field, SQLModel

PREDICTIONS_DATASET = config("PREDICTIONS_DATASET")
PREDICTIONS_PROACTIVE_TABLE = config("PREDICTIONS_PROACTIVE_TABLE")


# class NboChildishMlPredictionProactive(SQLModel, table=True):
#     __tablename__ = PREDICTIONS_PROACTIVE_TABLE
#     __table_args__ = {"schema": PREDICTIONS_DATASET}

#     ft_user_id: str = Field(primary_key=True)
#     arrangement_id: int = Field(title="Arrangement ID")
#     nbo1_offer_product: str = Field(title="Offer Product")
#     nbo1_offer_term: str = Field(title="Offer Term")
#     nbo1_offer_id: str = Field(title="Offer ID")
#     nbo1_offer_price: float = Field(title="Offer Price")
#     nbo1_offer_discount: str = Field(title="Offer Discount")
#     nbo1_offer_currency_id: int = Field(title="Offer Currency ID")
#     nbo1_ml_prediction_id_fkey: int = Field(title="ML Prediction ID")
#     nbo1_ml_prediction_dt: datetime = Field(title="ML Prediction Date")
#     inserted_datetime: datetime = Field(title="Inserted DateTime")
#     run_date: datetime = Field(title="Run Date")
#     nbo1_offer_currency_code: str = Field(title="Offer Currency Code")
#     # arrangement_id: int
#     # nbo1_offer_product: str
#     # nbo1_offer_term: str
#     # nbo1_offer_id: str
#     # nbo1_offer_price: float
#     # nbo1_offer_discount: str
#     # nbo1_offer_currency_id: int
#     # nbo1_ml_prediction_id_fkey: int
#     # nbo1_ml_prediction_dt: datetime
#     # inserted_datetime: datetime
#     # run_date: datetime
#     # nbo1_offer_currency_code: str


# class NboLtv(SQLModel, table=True):
#     user_id: str = Field(primary_key=True)
#     plan: str
#     region: str
#     currency: str
#     position: str
#     ltv_horizon: str
#     ltv: float


class Base(DeclarativeBase):
    pass


# class NboChildishMlPredictionProactiveDemo(SQLModel, table=True):
#     __tablename__ = "test_nbo_childish_ml_predictions_proactive_demo"
#     __table_args__ = {"schema": PREDICTIONS_DATASET}

#     ft_user_id: str = Field(primary_key=True)
#     arrangement_id: int
#     nbo1_offer_product: str
#     nbo1_offer_term: str
#     nbo1_offer_id: str
#     nbo1_offer_price: float
#     nbo1_offer_discount: str
#     nbo1_offer_currency_id: int
#     nbo1_ml_prediction_id_fkey: int
#     nbo1_ml_prediction_dt: datetime
#     inserted_datetime: datetime
#     run_date: datetime
#     nbo1_offer_currency_code: str


# class ProactivePredictions(SQLModel, table=True):
#     __tablename__ = "test_proactive_predictions_2024-10-01_2024-10-01"
#     __table_args__ = {"schema": PREDICTIONS_DATASET}

#     user_id: str = Field(primary_key=True)
#     Plan: str
#     Probability: float
#     b2c_product_currency_bookkeeping: str
#     geo_billing_b2c_marketing_region_bookkeeping: str
#     rollup_user_position_bookkeeping: str
#     student_flag_bookkeeping: bool
#     visa_payment_method_flag_bookkeeping: bool


class NboProactivePredictions(SQLModel, table=True):
    __tablename__ = "nbo_proactive_predictions_test"
    __table_args__ = {"schema": PREDICTIONS_DATASET}

    nbo1_ml_prediction_id_fkey: str = Field(primary_key=True)
    user_id: str
    plan: str
    product_arrangement_id_bookkeeping: str
    Probability: float = Field(title="probability")
    b2c_product_currency_bookkeeping: str
    geo_billing_b2c_marketing_region_bookkeeping: str
    rollup_user_position_bookkeeping: str
    student_flag_bookkeeping: int
    run_date: datetime
    nbo1_ml_prediction_dt: datetime
    user_dkey_bookkeeping: int


class NboProactiveLtv(SQLModel, table=True):
    __tablename__ = "nbo_proactive_ltv_test"
    __table_args__ = {"schema": PREDICTIONS_DATASET}

    nbo1_ml_prediction_id_fkey: str = Field(primary_key=True)
    ft_user_id: str
    user_dkey: int
    arrangement_id: int
    nbo1_offer_product: str
    nbo1_offer_term: str
    nbo1_offer_currency_id: int
    nbo1_offer_id: str
    nbo1_offer_price: float
    nbo1_offer_discount: str
    nbo1_ml_prediction_dt: datetime
    run_date: datetime
    nbo1_offer_currency_code: str
    plan: str
    ltv_horizon: str
    ltv: float
    inserted_datetime: datetime


class NboReactivePredictions(SQLModel, table=True):
    __tablename__ = "nbo_reactive_predictions_test"
    __table_args__ = {"schema": PREDICTIONS_DATASET}

    nbo1_ml_prediction_id_fkey: str = Field(primary_key=True)
    user_id: str
    product_arrangement_id_bookkeeping: str
    Probability: float = Field(title="probability")
    b2c_product_currency_bookkeeping: str
    geo_billing_b2c_marketing_region_bookkeeping: str
    rollup_user_position_bookkeeping: str
    student_flag_bookkeeping: bool
    run_date: datetime
    nbo1_ml_prediction_dt: datetime
    offered_product: str
    percent_rrp: int
    product_arrangement_id_bookkeeping: int
    user_dkey_bookkeeping: int


class NboReactiveLtv(SQLModel, table=True):
    __tablename__ = "nbo_reactive_ltv_test_v1"
    __table_args__ = {"schema": PREDICTIONS_DATASET}

    ft_user_id: str
    user_dkey: int
    nbo1_ml_prediction_id_fkey: str = Field(primary_key=True)
    arrangement_id: int
    nbo1_offer_product: str
    nbo1_offer_term: str
    nbo1_offer_currency_id: int
    nbo1_offer_id: str
    nbo1_offer_price: float
    nbo1_offer_discount: str
    nbo1_ml_prediction_dt: datetime
    run_date: datetime
    nbo1_offer_currency_code: str
    plan: str
    ltv_horizon: str
    ltv: float
    inserted_datetime: datetime


# class ProactivePredictions(SQLModel, table=True):
#     __tablename__ = "test_proactive_predictions_2024-10-01_2024-10-01"
#     __table_args__ = {"schema": PREDICTIONS_DATASET}

#     user_id: str = Field(primary_key=True)
#     Plan: str
#     Probability: float
#     b2c_product_currency_bookkeeping: str
#     geo_billing_b2c_marketing_region_bookkeeping: str
#     rollup_user_position_bookkeeping: str
#     student_flag_bookkeeping: bool
#     visa_payment_method_flag_bookkeeping: bool


# class ProactiveLTV(SQLModel, table=True):
#     __tablename__ = "test_proactive_ltv_2024-10-01_2024-10-01"
#     __table_args__ = {"schema": PREDICTIONS_DATASET}

#     user_id: str = Field(primary_key=True)
#     plan: str
#     region: str
#     currency: str
#     position: str
#     ltv_horizon: str
#     ltv: float


class User(BaseModel):
    name: str
    locale: str
    email: EmailStr
    preferred_username: str
    given_name: str
    family_name: str
    zoneinfo: str

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.name


class FilterFormData(BaseModel):
    nbo1_offer_product: Optional[List[str]]
    nbo1_offer_term: Optional[List[str]] = Form(None)
    nbo1_offer_id: Optional[List[str]] = Form(None)
    start_nbo1_offer_price: Optional[str] = Form(None)
    end_nbo1_offer_price: Optional[str] = Form(None)
    end_nbo1_ml_prediction_dt: Optional[str] = Form(None)
    start_nbo1_ml_prediction_dt: Optional[str] = Form(None)
    start_run_date: Optional[str] = Form(None)
    end_run_date: Optional[str] = Form(None)
    nbo1_offer_currency_code: Optional[List[str]] = Form(None)
    plan: Optional[List[str]] = Form(None)
    geo_billing_b2c_marketing_region_bookkeeping: Optional[List[str]] = Form(None)
    rollup_user_position_bookkeeping: Optional[List[str]] = Form(None)
    student_flag_bookkeeping: Optional[bool] = Form(None)
    ltv_horizon: Optional[List[str]] = Form(None)
    ltv_start: Optional[str] = Form(None)
    ltv_end: Optional[str] = Form(None)

    # Custom fields
    custom_ml_model: Optional[str] = Form(None, title="ML Model")
