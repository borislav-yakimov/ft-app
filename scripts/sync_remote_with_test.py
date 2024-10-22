# from google.cloud import bigquery
# import os
# from datetime import datetime, date

# def copy_table_data(
#     source_project, source_dataset, source_table, destination_project, destination_dataset, destination_table
# ):
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/borislav/.config/gcloud/application_default_credentials.json"
#     source_client = bigquery.Client(project=source_project)
#     source_table_ref = f"{source_project}.{source_dataset}.{source_table}"
#     select_query = f"SELECT * FROM `{source_table_ref}`"
#     select_query_job = source_client.query(select_query)
#     rows = select_query_job.result()

#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
#         "/mnt/c/Borislav Yakimov/KEYS/Google BigQuery service k ey/apt-cycling-435908-k2-7926cb64574c.json"
#     )
#     destination_client = bigquery.Client(project=destination_project)
#     destination_table_ref = f"{destination_project}.{destination_dataset}.{destination_table}"

#     rows_to_insert = []
#     for row in rows:
#         row_dict = dict(row)
#         for key, value in row_dict.items():
#             if isinstance(value, datetime) or isinstance(value, date):
#                 row_dict[key] = value.isoformat()
#         rows_to_insert.append(row_dict)
#     errors = destination_client.insert_rows_json(destination_table_ref, rows_to_insert)

#     if errors:
#         print(f"Errors occurred while inserting rows: {errors}")
#     else:
#         print(f"Data copied from {source_table_ref} to {destination_table_ref}")


# if __name__ == "__main__":
#     source_project = "ft-data-science"
#     source_dataset = "test"
#     source_proactive_predictions_table = "proactive_predictions_2024-10-01_2024-10-01"
#     source_ml_predictions_demo_table = "nbo_childish_ml_predictions_proactive_demo"
#     source_proactive_ltv_table = "proactive_ltv_2024-10-01_2024-10-01"

#     destination_project = "apt-cycling-435908-k2"
#     destination_dataset = "test_nbo_ltv_df"
#     destination_proactive_predictions_table = "test_proactive_predictions_2024-10-01_2024-10-01"
#     destination_ml_predictions_demo_table = "test_nbo_childish_ml_predictions_proactive_demo"
#     destination_proactive_ltv_table = "test_proactive_ltv_2024-10-01_2024-10-01"

#     # copy_table_data(
#     #     source_project,
#     #     source_dataset,
#     #     source_ml_predictions_demo_table,
#     #     destination_project,
#     #     destination_dataset,
#     #     destination_ml_predictions_demo_table,
#     # )

#     # copy_table_data(
#     #     source_project, source_dataset, source_proactive_predictions_table,
#     #     destination_project, destination_dataset, destination_proactive_predictions_table
#     # )

#     # copy_table_data(
#     #     source_project,
#     #     source_dataset,
#     #     source_proactive_ltv_table,
#     #     destination_project,
#     #     destination_dataset,
#     #     destination_proactive_ltv_table,
#     # )
