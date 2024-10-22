from urllib.parse import parse_qs, urlencode


from dependencies import get_session, pagination
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from services.offers import (
    get_column_filters_select_options_context,
    get_filtered_params,
    get_filtered_prediction_records,
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
    request: Request,
    session: Session = Depends(get_session),
    pagination_params: dict = Depends(pagination),
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
        **get_column_filters_select_options_context(
            session=session, filtered_params=filtered_params
        ),
    }

    return templates.TemplateResponse(
        "index",
        context,
    )


@router.get(Path.offers_export_xlsx)
@requires("authenticated")
async def offers_export_xlsx(
    request: Request,
    session: Session = Depends(get_session),
) -> StreamingResponse:
    query_params = request.query_params.multi_items()
    query_params = parse_qs(str(request.query_params))
    query_params.pop("page", None)
    query_params.pop("size", None)

    filter_fields = get_filtered_params(query_params)

    if filter_fields:
        prediction_records = get_filtered_prediction_records(
            filter_fields=filter_fields, session=session, pagination=False
        )
    else:
        prediction_records = get_prediction_records(session=session, pagination=False)

    xlsx_stream = await transform_records_to_xlsx(prediction_records)

    response = StreamingResponse(
        iter([xlsx_stream.getvalue()]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    file_name = "prediction_records.xlsx"
    response.headers["Content-Disposition"] = f"attachment; filename={file_name}"
    return response


@router.get(Path.offers, response_class=HTMLResponse)
@requires("authenticated")
async def offers(
    request: Request,
    session: Session = Depends(get_session),
    pagination_params: dict = Depends(pagination),
):
    query_params = request.query_params.multi_items()
    query_params = parse_qs(str(request.query_params))
    query_params.pop("page", None)
    query_params.pop("size", None)
    q_params = urlencode(query_params, doseq=True)

    filter_fields = get_filtered_params(query_params)

    context = {
        "request": request,
        "q_params": q_params,
        **get_possible_offers_rows_context(
            request, session, pagination_params, filter_fields
        ),
    }

    if request.headers.get("HX-Request") == "true":
        return templates.TemplateResponse(
            "tables/possible_offers/table_content",
            context,
        )
    else:
        context.update(
            get_column_filters_select_options_context(session, filter_fields)
        )
        return templates.TemplateResponse(
            "index",
            context,
        )


@router.get(Path.column_filters_fields, response_class=HTMLResponse)
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
