STATIC_FILE_DIRECTORY = "/static"

# POSSIBLE_OFFERS_COLUMNS = [
#     "ft_user_id",
#     "arrangement_id",
#     "nbo1_offer_product",
#     "nbo1_offer_term",
#     "nbo1_offer_id",
#     "nbo1_offer_price",
#     "nbo1_offer_discount",
#     "nbo1_offer_currency_id",
#     "nbo1_ml_prediction_id_fkey",
#     "nbo1_ml_prediction_dt",
# ]


# PREDICTION_PROACTIVE_COLUMNS = [
#     "ft_user_id",
#     "arrangement_id",
#     "nbo1_offer_product",
#     "nbo1_offer_term",
#     "nbo1_offer_id",
#     "nbo1_offer_price",
#     "nbo1_offer_discount",
#     "nbo1_ml_prediction_dt",
#     "run_date",
#     "nbo1_offer_currency_code",
# ]

# PROACTIVE_PREDICTIONS_COLUMNS = [
#     "Plan",
#     "Probability",
#     "b2c_product_currency_bookkeeping",
#     "geo_billing_b2c_marketing_region_bookkeeping",
#     "rollup_user_position_bookkeeping",
#     "student_flag_bookkeeping",
#     # Will be added in future
#     # "user_dkey_bookkeeping",
#     # "product_arrangement_id_bookkeeping",
#     # ...
#     # "visa_payment_method_flag_bookkeeping",
# ]

# PROACTIVE_LTV_COLUMNS = ["ltv_horizon", "ltv"]

PROACTIVE_PREDICTIONS_COLUMNS = [
    # "nbo1_ml_prediction_id_fkey",
    "user_id",
    "product_arrangement_id_bookkeeping",
    "Probability",
    "b2c_product_currency_bookkeeping",
    "geo_billing_b2c_marketing_region_bookkeeping",
    "rollup_user_position_bookkeeping",
    "student_flag_bookkeeping",
]

PROACTIVE_LTV_COLUMNS = [
    "nbo1_offer_product",
    "nbo1_offer_term",
    "nbo1_offer_id",
    "nbo1_offer_price",
    "nbo1_offer_discount",
    "nbo1_ml_prediction_dt",
    "run_date",
    "nbo1_offer_currency_code",
    "plan",
    "ltv_horizon",
    "ltv",
]

REACTIVE_PREDICTIONS_COLUMNS = [
    # "nbo1_ml_prediction_id_fkey",
    "user_id",
    "product_arrangement_id_bookkeeping",
    "Probability",
    "b2c_product_currency_bookkeeping",
    "geo_billing_b2c_marketing_region_bookkeeping",
    "rollup_user_position_bookkeeping",
    "student_flag_bookkeeping",
]

REACTIVE_LTV_COLUMNS = [
    "nbo1_offer_product",
    "nbo1_offer_term",
    "nbo1_offer_id",
    "nbo1_offer_price",
    "nbo1_offer_discount",
    "nbo1_ml_prediction_dt",
    "run_date",
    "nbo1_offer_currency_code",
    "plan",
    "ltv_horizon",
    "ltv",
]

PROACTIVE_ML_MODEL = "proactive"
REACTIVE_MODEL_NAME = "reactive"
DEFAULT_ML_MODEL = REACTIVE_MODEL_NAME

SELECT_COMPONENT_PATH = "components/select.jinja"
MULTIPLE_SELECT_COMPONENT_PATH = "components/multiple_select.jinja"
BOOLEAN_SELECT_COMPONENT_PATH = "components/boolean_select.jinja"
NUMBERS_START_END_COMPONENT_PATH = "components/numbers_start_end.jinja"
DATE_RANGE_START_END_COMPONENT_PATH = "components/date_range_start_end.jinja"
