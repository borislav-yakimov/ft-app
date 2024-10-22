import asyncio
import io
import math
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Callable, List, TypedDict

import pandas as pd
from constants import (
    PROACTIVE_LTV_COLUMNS,
    PROACTIVE_ML_MODEL,
    PROACTIVE_PREDICTIONS_COLUMNS,
    REACTIVE_LTV_COLUMNS,
    REACTIVE_MODEL_NAME,
    REACTIVE_PREDICTIONS_COLUMNS,
)
from models import NboProactiveLtv, NboProactivePredictions, NboReactiveLtv, NboReactivePredictions
from numpy import isin
from sqlalchemy import Boolean, DateTime, Float, Row, func
from sqlmodel import Session, SQLModel, or_, select

func: Callable


class PaginateMetadataType(TypedDict):
    pages: int
    page: int
    size: int
    offset: int


@dataclass
class PaginateContextType:
    paginate_metadata: PaginateMetadataType


# def get_model_fields(Model: SQLModel, field_names: list[str]) -> tuple:
#     return (getattr(Model, field) for field in field_names)


def get_model_fields(Model: SQLModel, field_names: List[str], decimal_places: int = 4) -> list:
    fields = []
    for field_name in field_names:
        field = getattr(Model, field_name)
        field_type = Model.__annotations__.get(field_name)
        if field_type in [float, Decimal]:
            field = func.round(field, decimal_places).label(field_name)
        fields.append(field)
    return fields


def get_models_fields_titles(Model: SQLModel, columns: list[str]) -> tuple:
    return (getattr(Model.__fields__[column], "title", column) or column for column in columns)


def get_total_records_count(session: Session, Model: SQLModel) -> int:
    return session.exec(select(func.count()).select_from(Model)).first()


def get_paginate_context(page: int, size: int, offset: int, total_records: int) -> PaginateContextType:
    pages = math.ceil(total_records / size)

    return {"paginate_metadata": {"pages": pages, "page": page, "size": size, "offset": offset}}


# def transform_records_to_xlsx(records: list[Row]):
#     # Convert prediction_records to a DataFrame
#     df = pd.DataFrame(records)

#     # Convert timezone-aware datetimes to timezone-unaware datetimes
#     for column in df.select_dtypes(include=["datetimetz"]).columns:
#         df[column] = df[column].dt.tz_localize(None)

#     # Create a BytesIO stream to hold the XLSX data
#     stream = io.BytesIO()
#     # Save the DataFrame to the BytesIO stream as an XLSX file
#     df.to_excel(stream, index=False, engine="openpyxl")
#     # Seek to the beginning of the stream
#     stream.seek(0)
#     return stream


async def transform_records_to_xlsx(records: List[Row]):
    # Convert prediction_records to a DataFrame
    df = pd.DataFrame(records)

    # Convert timezone-aware datetimes to timezone-unaware datetimes
    for column in df.select_dtypes(include=["datetimetz"]).columns:
        df[column] = df[column].dt.tz_localize(None)

    # Create a BytesIO stream to hold the XLSX data
    stream = io.BytesIO()

    # Define a blocking function to save the DataFrame to the BytesIO stream
    def save_to_stream():
        df.to_excel(stream, index=False, engine="openpyxl")
        stream.seek(0)
        return stream

    # Run the blocking function in a separate thread
    stream = await asyncio.to_thread(save_to_stream)

    return stream


def get_proactive_model(field_name):
    Model = None
    if field_name in PROACTIVE_PREDICTIONS_COLUMNS:
        Model = NboProactivePredictions
    elif field_name in PROACTIVE_LTV_COLUMNS:
        Model = NboProactiveLtv

    return Model


def get_reactive_model(field_name):
    Model = None
    if field_name in REACTIVE_PREDICTIONS_COLUMNS:
        Model = NboReactivePredictions
    elif field_name in REACTIVE_LTV_COLUMNS:
        Model = NboReactiveLtv

    return Model


# def get_filtered_statement(statement, filter_fields):
#     for key, value in filter_fields.items():
#         field = None
#         if not key.startswith("start_") and not key.startswith("end_"):
#             Model = get_proactive_model(key)
#             field = getattr(Model, key)
#         # statement = statement.where(field == value)
#         if isinstance(value, list):
#             or_conditions = [field == value for value in value]
#             statement = statement.where(or_(*or_conditions))
#         elif field and isinstance(field.type, Boolean):
#             value = True if value.lower() == "true" else False
#             statement = statement.where(field == value)
#         elif key.startswith("start_"):
#             field_name = key.replace("start_", "")
#             Model = get_proactive_model(field_name)
#             field = getattr(Model, field_name)
#             if isinstance(field.type, DateTime):
#                 value = datetime.strptime(value, "%m/%d/%Y")
#                 statement = statement.where(field >= value)
#             elif isinstance(field.type, Float):
#                 statement = statement.where(field >= float(value))
#         elif key.startswith("end_"):
#             field = getattr(Model, key.replace("end_", ""))
#             if isinstance(field.type, DateTime):
#                 value = datetime.strptime(value, "%m/%d/%Y")
#                 statement = statement.where(field <= value)
#             elif isinstance(field.type, Float):
#                 statement = statement.where(field <= float(value))
#         else:
#             statement = statement.where(field == value)

#     return statement


def get_model(custom_ml_model, field_name):
    Model = None
    if custom_ml_model == PROACTIVE_ML_MODEL:
        Model = get_proactive_model(field_name)
    elif custom_ml_model == REACTIVE_MODEL_NAME:
        Model = get_reactive_model(field_name)

    return Model


def get_model_and_field(key, ml_model):
    Model = get_model(ml_model, key)
    field = getattr(Model, key, None)
    if field is None:
        raise AttributeError(f"Field '{key}' not found in model '{Model.__name__}'")
    return Model, field


def parse_date(value):
    try:
        return datetime.strptime(value, "%m/%d/%Y")
    except ValueError:
        raise ValueError(f"Value '{value}' is not a valid date format. Expected format: 'mm/dd/yyyy'")


def get_filtered_statement(statement, filter_fields, ml_model):
    EXCLUDED_KEYS = ["custom_ml_model"]

    for key, value in filter_fields.items():
        if key in EXCLUDED_KEYS:
            continue
        if key.startswith("start_") or key.startswith("end_"):
            field_name = key.replace("start_", "").replace("end_", "")
            Model, field = get_model_and_field(field_name, ml_model)
            if isinstance(field.type, DateTime):
                value = parse_date(value)
                if key.startswith("start_"):
                    statement = statement.where(field >= value)
                else:
                    statement = statement.where(field <= value)
            elif isinstance(field.type, Float):
                value = float(value)
                if key.startswith("start_"):
                    statement = statement.where(field >= value)
                else:
                    statement = statement.where(field <= value)
        else:
            Model, field = get_model_and_field(key, ml_model)
            if isinstance(value, list):
                or_conditions = [field == v for v in value]
                statement = statement.where(or_(*or_conditions))
            elif isinstance(field.type, Boolean):
                value = 1 if value.lower() == "true" else 0
                statement = statement.where(field == value)
            else:
                statement = statement.where(field == value)

    return statement
