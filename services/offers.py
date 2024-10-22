from time import perf_counter
from typing import Callable, List

from constants import (  # PREDICTION_PROACTIVE_COLUMNS,; PROACTIVE_LTV_COLUMNS,; PROACTIVE_PREDICTIONS_COLUMNS,
    BOOLEAN_SELECT_COMPONENT_PATH,
    DATE_RANGE_START_END_COMPONENT_PATH,
    DEFAULT_ML_MODEL,
    MULTIPLE_SELECT_COMPONENT_PATH,
    NUMBERS_START_END_COMPONENT_PATH,
    PROACTIVE_LTV_COLUMNS,
    PROACTIVE_ML_MODEL,
    PROACTIVE_PREDICTIONS_COLUMNS,
    REACTIVE_LTV_COLUMNS,
    REACTIVE_MODEL_NAME,
    REACTIVE_PREDICTIONS_COLUMNS,
    SELECT_COMPONENT_PATH,
)
from fastapi import Request

# from models import NboChildishMlPredictionProactiveDemo, ProactiveLTV, ProactivePredictions
from models import FilterFormData, NboProactiveLtv, NboProactivePredictions, NboReactiveLtv, NboReactivePredictions
from sqlmodel import Session, func, select
from utils import (
    get_filtered_statement,
    get_model,
    get_model_fields,
    get_models_fields_titles,
    get_paginate_context,
    get_proactive_model,
    get_reactive_model,
)

func: Callable


def get_prediction_statement(ml_model: str = DEFAULT_ML_MODEL) -> select:
    predictions_statement = None
    if ml_model == PROACTIVE_ML_MODEL:
        predictions_statement = (
            select(
                *get_model_fields(NboProactivePredictions, PROACTIVE_PREDICTIONS_COLUMNS),
                *get_model_fields(NboProactiveLtv, PROACTIVE_LTV_COLUMNS),
            )
            .select_from(NboProactivePredictions)
            .join(
                NboProactiveLtv,
                NboProactivePredictions.nbo1_ml_prediction_id_fkey == NboProactiveLtv.nbo1_ml_prediction_id_fkey,
            )
        )
    elif ml_model == REACTIVE_MODEL_NAME:
        predictions_statement = (
            select(
                *get_model_fields(NboReactivePredictions, REACTIVE_PREDICTIONS_COLUMNS),
                *get_model_fields(NboReactiveLtv, REACTIVE_LTV_COLUMNS),
            )
            .select_from(NboReactivePredictions)
            .join(
                NboReactiveLtv,
                NboReactivePredictions.nbo1_ml_prediction_id_fkey == NboReactiveLtv.nbo1_ml_prediction_id_fkey,
            )
        )

    return predictions_statement


def get_prediction_records(session: Session, offset: int = 0, size: int = 5, pagination: bool = True) -> list[dict]:
    predictions_statement = get_prediction_statement()

    if pagination:
        predictions_statement = predictions_statement.offset(offset).limit(size)

    results = session.exec(predictions_statement).all()

    return results


def get_filtered_prediction_records(
    filter_fields: dict, session: Session, offset: int = 0, size: int = 5, pagination: bool = True
) -> list[dict]:
    ml_model = filter_fields.get("custom_ml_model", DEFAULT_ML_MODEL).lower()
    predictions_statement = get_prediction_statement(ml_model)
    predictions_statement = get_filtered_statement(predictions_statement, filter_fields, ml_model)

    if pagination:
        predictions_statement = predictions_statement.offset(offset).limit(size)

    results = session.exec(predictions_statement).all()

    return results


# def get_predictions_total_count(session: Session, ml_model: str = DEFAULT_ML_MODEL) -> int:
#     if ml_model == "proactive":
#         count_statement = (
#             select(func.count())
#             .select_from(NboChildishMlPredictionProactiveDemo)
#             .join(ProactivePredictions, NboChildishMlPredictionProactiveDemo.ft_user_id == ProactivePredictions.user_id)
#             .join(ProactiveLTV, NboChildishMlPredictionProactiveDemo.ft_user_id == ProactiveLTV.user_id)
#         )
#     total_count = session.exec(count_statement).one()

#     return total_count


def get_predictions_total_count(session: Session, ml_model: str = DEFAULT_ML_MODEL) -> int:
    if ml_model == PROACTIVE_ML_MODEL:
        count_statement = (
            select(func.count())
            .select_from(NboProactivePredictions)
            .join(
                NboProactiveLtv,
                NboProactivePredictions.nbo1_ml_prediction_id_fkey == NboProactiveLtv.nbo1_ml_prediction_id_fkey,
            )
        )
    elif ml_model == REACTIVE_MODEL_NAME:
        count_statement = (
            select(func.count())
            .select_from(NboReactivePredictions)
            .join(
                NboReactiveLtv,
                NboReactivePredictions.nbo1_ml_prediction_id_fkey == NboReactiveLtv.nbo1_ml_prediction_id_fkey,
            )
        )

    total_count = session.exec(count_statement).one()

    return total_count


def get_predictions_filtered_total_count(filter_fields: dict, session: Session) -> int:
    ml_model = filter_fields.get("custom_ml_model", DEFAULT_ML_MODEL).lower()
    if ml_model == PROACTIVE_ML_MODEL:
        count_statement = (
            select(func.count())
            .select_from(NboProactivePredictions)
            .join(
                NboProactiveLtv,
                NboProactivePredictions.nbo1_ml_prediction_id_fkey == NboProactiveLtv.nbo1_ml_prediction_id_fkey,
            )
        )
    elif ml_model == REACTIVE_MODEL_NAME:
        count_statement = (
            select(func.count())
            .select_from(NboReactivePredictions)
            .join(
                NboReactiveLtv,
                NboReactivePredictions.nbo1_ml_prediction_id_fkey == NboReactiveLtv.nbo1_ml_prediction_id_fkey,
            )
        )

    count_statement = get_filtered_statement(count_statement, filter_fields, ml_model)
    total_count = session.exec(count_statement).one()

    return total_count


def get_field_distinct(session: Session, field_name: str, filtered_params: dict) -> List[str]:
    custom_ml_model = filtered_params.get("custom_ml_model", DEFAULT_ML_MODEL).lower()
    # Model = None
    # if custom_ml_model == PROACTIVE_ML_MODEL:
    #     Model = get_proactive_model(field_name)
    # elif custom_ml_model == REACTIVE_MODEL_NAME:
    #     Model = get_reactive_model(field_name)
    Model = get_model(custom_ml_model, field_name)

    if not Model:
        raise ValueError(f"Field {field_name} not found in any of the models")

    field = getattr(Model, field_name)
    statement = select(field).distinct().select_from(Model)
    results = session.exec(statement).all()

    return results


def get_possible_offers_rows_context(
    request: Request, session: Session, pagination_params: dict, filter_fields: dict | None = None
) -> dict:
    page, size, offset = pagination_params

    start_time = perf_counter()
    if filter_fields:
        prediction_records = get_filtered_prediction_records(filter_fields, session, offset, size, session)
        total_records = get_predictions_filtered_total_count(filter_fields, session)
    else:
        prediction_records = get_prediction_records(session, offset, size, session)
        total_records = get_predictions_total_count(session)

    end_time = perf_counter()
    print(f"Time taken to fetch records: {end_time - start_time:.2f} seconds")

    paginate_context = get_paginate_context(*pagination_params, total_records)
    pages = paginate_context["paginate_metadata"]["pages"]

    result_pages_repr = (
        f"{offset + 1}-{total_records if page == pages else offset + size} of { total_records }"
        if total_records > 0
        else ""
    )

    def get_model_fields_titles_by_model_type(model_type: str = DEFAULT_ML_MODEL):
        if model_type == PROACTIVE_ML_MODEL:
            return [
                *get_models_fields_titles(NboProactivePredictions, PROACTIVE_PREDICTIONS_COLUMNS),
                *get_models_fields_titles(NboProactiveLtv, PROACTIVE_LTV_COLUMNS),
            ]
        elif model_type == REACTIVE_MODEL_NAME:
            return [
                *get_models_fields_titles(NboReactivePredictions, REACTIVE_PREDICTIONS_COLUMNS),
                *get_models_fields_titles(NboReactiveLtv, REACTIVE_LTV_COLUMNS),
            ]

    context = {
        "possible_offers_columns": get_model_fields_titles_by_model_type(),
        "prediction_records": prediction_records,
        "metadata": {
            "result_pages_repr": result_pages_repr,
        },
        **paginate_context,
    }

    return context


def get_field_options(session: Session, filtered_params: dict) -> Callable:
    def inner(field_name: str, template: str):
        field_context = {"name": field_name, "template": template}

        if template == MULTIPLE_SELECT_COMPONENT_PATH or template == SELECT_COMPONENT_PATH:
            options = get_field_distinct(session, field_name, filtered_params)
            field_context["options"] = options

        return field_context

    return inner


def get_custom_field_options(field_name: str, template: str):
    field_context = {"name": field_name, "template": template}
    if field_name == "custom_ml_model":
        options = [
            "Reactive",
            "Proactive",
        ]
        field_context["options"] = options

    return field_context


def get_column_filters_select_options_context(session: Session, filtered_params: dict) -> dict:
    get_options = get_field_options(session, filtered_params)

    fields = [
        get_custom_field_options("custom_ml_model", SELECT_COMPONENT_PATH),
        get_options("nbo1_offer_product", MULTIPLE_SELECT_COMPONENT_PATH),
        get_options("nbo1_offer_term", MULTIPLE_SELECT_COMPONENT_PATH),
        get_options("nbo1_offer_id", MULTIPLE_SELECT_COMPONENT_PATH),
        get_options("nbo1_offer_price", NUMBERS_START_END_COMPONENT_PATH),
        get_options("nbo1_ml_prediction_dt", DATE_RANGE_START_END_COMPONENT_PATH),
        get_options("run_date", DATE_RANGE_START_END_COMPONENT_PATH),
        get_options("nbo1_offer_currency_code", MULTIPLE_SELECT_COMPONENT_PATH),
        get_options("plan", MULTIPLE_SELECT_COMPONENT_PATH),
        get_options("geo_billing_b2c_marketing_region_bookkeeping", MULTIPLE_SELECT_COMPONENT_PATH),
        get_options("rollup_user_position_bookkeeping", MULTIPLE_SELECT_COMPONENT_PATH),
        get_options("student_flag_bookkeeping", BOOLEAN_SELECT_COMPONENT_PATH),
        get_options("ltv_horizon", MULTIPLE_SELECT_COMPONENT_PATH),
    ]

    context = {"column_filter_fields": fields}

    return context


def get_filtered_params(query_params):
    filtered_params = {}
    for field_name, field_value in query_params.items():
        field_value = field_value[0] if len(field_value) == 1 else field_value
        if field_name not in FilterFormData.model_fields:
            raise ValueError(f"{field_name} not in FilterFormData model fields")
        if field_value and "default" not in field_value:
            filtered_params[field_name] = field_value

    return filtered_params
