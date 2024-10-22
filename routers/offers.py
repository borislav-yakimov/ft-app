from urllib.parse import parse_qs, urlencode

from constants import (
    BOOLEAN_SELECT_COMPONENT_PATH,
    DATE_RANGE_START_END_COMPONENT_PATH,
    MULTIPLE_SELECT_COMPONENT_PATH,
    NUMBERS_START_END_COMPONENT_PATH,
)
from dependencies import get_session, pagination
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from models import FilterFormData
from services.offers import (
    get_column_filters_select_options_context,
    get_field_options,
    get_filtered_params,
    get_possible_offers_rows_context,
    get_prediction_records,
)
from settings import templates
from sqlmodel import Session
from starlette.authentication import requires
from starlette.responses import StreamingResponse
from utils import transform_records_to_xlsx

from .paths import Path

router = APIRouter()


@router.get(Path.home, response_class=HTMLResponse)
@requires("authenticated")
async def home(
    request: Request, session: Session = Depends(get_session), pagination_params: dict = Depends(pagination)
) -> HTMLResponse:

    query_params = request.query_params.multi_items()
    query_params = parse_qs(str(request.query_params))
    query_params.pop("page", None)
    query_params.pop("size", None)
    q_params = urlencode(query_params, doseq=True)
    filtered_params = get_filtered_params(query_params)

    context = {
        "request": request,
        "q_params": q_params,
        **get_possible_offers_rows_context(request, session, pagination_params),
        **get_column_filters_select_options_context(session=session, filtered_params=filtered_params),
    }

    return templates.TemplateResponse(
        "index",
        context,
    )


@router.get("/offers/export-xlsx")
@requires("authenticated")
async def offers_export_xlsx(request: Request, session: Session = Depends(get_session)) -> StreamingResponse:
    prediction_records = get_prediction_records(session=session, pagination=False)

    xlsx_stream = await transform_records_to_xlsx(prediction_records)

    response = StreamingResponse(
        iter([xlsx_stream.getvalue()]), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    file_name = "prediction_records.xlsx"
    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
    return response


@router.get(Path.offers, response_class=HTMLResponse)
@requires("authenticated")
async def offers(
    request: Request, session: Session = Depends(get_session), pagination_params: dict = Depends(pagination)
):
    query_params = request.query_params.multi_items()
    query_params = parse_qs(str(request.query_params))
    query_params.pop("page", None)
    query_params.pop("size", None)
    q_params = urlencode(query_params, doseq=True)

    # filtered_params = {}
    # for field_name, field_value in query_params.items():
    #     field_value = field_value[0] if len(field_value) == 1 else field_value
    #     if field_name not in FilterFormData.model_fields:
    #         raise ValueError(f"{field_name} not in FilterFormData model fields")
    #     if field_value and "default" not in field_value:
    #         filtered_params[field_name] = field_value
    filtered_params = get_filtered_params(query_params)

    context = {
        "request": request,
        "q_params": q_params,
        **get_possible_offers_rows_context(request, session, pagination_params, filtered_params),
    }

    if request.headers.get("HX-Request") == "true":
        return templates.TemplateResponse(
            "tables/possible_offers/table_content",
            context,
        )
    else:
        context.update(get_column_filters_select_options_context(session, filtered_params))
        return templates.TemplateResponse(
            "index",
            context,
        )


@router.get("/column-filters-fields", response_class=HTMLResponse)
@requires("authenticated")
async def get_select_options(request: Request, session: Session = Depends(get_session)):
    query_params = request.query_params.multi_items()
    query_params = parse_qs(str(request.query_params))
    query_params.pop("page", None)
    query_params.pop("size", None)
    q_params = urlencode(query_params, doseq=True)
    filtered_params = get_filtered_params(query_params)
    context = {
        "request": request,
        "q_params": q_params,
        **get_column_filters_select_options_context(session, filtered_params),
    }

    return templates.TemplateResponse(
        "tables/column_filters/table_content",
        context,
    )


# @router.post("/column-filters-fields", response_class=HTMLResponse)
# @requires("authenticated")
# async def post_select_options(request: Request, session: Session = Depends(get_session)):
#     data_dict = await request.json()
#     form_data = FilterFormData(**data_dict)

#     get_possible_offers_rows_context(request, session, pagination_params, data_dict)
#     offers(request, session, pagination_params, data_dict)

#     # for key, value in data_dict.items():
#     #     if value and value != "default":
#     #         pass

#     return templates.TemplateResponse(
#         "tables/column_filters/table_content",
#         {"request": request},
#     )


# @router.post("/select-options")
# @requires("authenticated")
# async def select_options(
#     request: Request, session: Session = Depends(get_session), form_data: FilterFormData = Depends()
# ):
#     print(form_data)
#     context = {}

#     return templates.TemplateResponse(
#         "tables/includes/select_options.html",
#         context,
#     )


# @router.get("/select-options/", response_class=HTMLResponse)
# @requires("authenticated")
# async def select_options(request: Request, session: Session = Depends(get_session), field_name: str = ""):
#     if field_name not in FilterFormData.model_fields.keys():
#         raise ValueError(f"{field_name} not in FilterFormData model fields")

#     # field_maps = {
#     #     "nbo1_offer_product": get_field_distinct,
#     #     "nbo1_offer_term": get_field_distinct,
#     #     "nbo1_offer_id": get_field_distinct,
#     #     "nbo1_offer_price": None,
#     #     "nbo1_ml_prediction_dt": ,
#     #     "nbo1_offer_currency_code": get_field_distinct,
#     #     "plan": get_field_distinct,
#     #     "geo_billing_b2c_marketing_region_bookkeeping": get_field_distinct,
#     #     "rollup_user_position_bookkeeping": get_field_distinct,
#     #     "student_flag_bookkeeping": get_field_distinct,
#     #     "ltv_horizon": get_field_distinct,
#     # }

#     # if field_name not in field_maps:
#     #     raise ValueError(f"{field_name} not in field_maps")

#     options = get_field_distinct(session, field_name)
#     context = {"request": request, "options": options}

#     return templates.TemplateResponse(
#         "tables/includes/select_options",
#         context,
#     )
