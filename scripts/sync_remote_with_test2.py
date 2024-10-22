from google.cloud import bigquery
import os
from datetime import datetime, date


def copy_table_data(
    source_project, source_dataset, source_table, destination_project, destination_dataset, destination_table
):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/borislav/.config/gcloud/application_default_credentials.json"

    source_client = bigquery.Client(project=source_project)

    page_count = 0
    total_results = 0
    # Use context manager for source client
    try:
        source_table_ref = f"{source_project}.{source_dataset}.{source_table}"
        select_query = f"SELECT * FROM `{source_table_ref}`"
        select_query_job = source_client.query(select_query)

        # Initialize counters

        # Collect all rows from all pages
        rows_to_insert = []
        for page in select_query_job.result().pages:
            page_count += 1
            for row in page:
                total_results += 1
                row_dict = dict(row)
                for key, value in row_dict.items():
                    if isinstance(value, datetime) or isinstance(value, date):
                        row_dict[key] = value.isoformat()
                rows_to_insert.append(row_dict)

        print(f"Total pages: {page_count}")
        print(f"Total results: {total_results}")
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    finally:
        source_client.close()
        print("Source client closed.")

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = (
        "/mnt/c/Borislav Yakimov/KEYS/Google BigQuery service k ey/apt-cycling-435908-k2-7926cb64574c.json"
    )

    # Use context manager for destination client
    # with bigquery.Client(project=destination_project) as destination_client:
    #     destination_table_ref = f"{destination_project}.{destination_dataset}.{destination_table}"

    #     # Insert rows into the destination table
    #     errors = destination_client.insert_rows_json(destination_table_ref, rows_to_insert)

    #     if errors:
    #         print(f"Errors occurred while inserting rows: {errors}")
    #     else:
    #         print(f"Data copied from {source_table_ref} to {destination_table_ref}")

    destination_client = bigquery.Client(project=destination_project)

    batch_size = 10_000
    total_batches = (total_results // batch_size) + 1
    try:
        destination_table_ref = f"{destination_project}.{destination_dataset}.{destination_table}"

        # Insert rows into the destination table in batches
        # Adjust batch size as needed
        for i in range(0, len(rows_to_insert), batch_size):
            batch = rows_to_insert[i : i + batch_size]
            errors = destination_client.insert_rows_json(destination_table_ref, batch, timeout=600)

            if errors:
                print(f"Errors occurred while inserting rows: {errors}")
            else:
                print(f"Batch {i // batch_size + 1} / {total_batches} inserted successfully.")
    except KeyboardInterrupt:
        print("Process interrupted by user.")
    finally:
        destination_client.close()
        print("Destination client closed.")


if __name__ == "__main__":
    source_project = "ft-data-science"
    source_dataset = "test"

    source_nbo_proactive_predictions_test_table = "nbo_proactive_predictions_test"
    source_nbo_proactive_ltv_test_table = "nbo_proactive_ltv_test"

    source_nbo_reactive_predictions_test_table = "nbo_reactive_predictions_test"
    source_nbo_reactive_ltv_test_table = "nbo_reactive_ltv_test_v1"
    # source_proactive_ltv_table = "proactive_ltv_2024-10-01_2024-10-01"

    destination_project = "apt-cycling-435908-k2"
    destination_dataset = "test"

    destination_nbo_proactive_predictions_test_table = "nbo_proactive_predictions_test"
    destination_nbo_proactive_ltv_test_table = "nbo_proactive_ltv_test"

    destination_nbo_reactive_predictions_test_table = "nbo_reactive_predictions_test"
    destination_nbo_reactive_ltv_test_table = "nbo_reactive_ltv_test_v1"
    # destination_proactive_ltv_table = "test_proactive_ltv_2024-10-01_2024-10-01"

    copy_table_data(
        source_project,
        source_dataset,
        source_nbo_proactive_predictions_test_table,
        destination_project,
        destination_dataset,
        destination_nbo_proactive_predictions_test_table,
    )

    copy_table_data(
        source_project, source_dataset, source_nbo_proactive_ltv_test_table,
        destination_project, destination_dataset, destination_nbo_proactive_ltv_test_table
    )

    # copy_table_data(
    #     source_project,
    #     source_dataset,
    #     source_nbo_reactive_predictions_test_table,
    #     destination_project,
    #     destination_dataset,
    #     destination_nbo_reactive_predictions_test_table,
    # )

    # copy_table_data(
    #     source_project,
    #     source_dataset,
    #     source_nbo_reactive_ltv_test_table,
    #     destination_project,
    #     destination_dataset,
    #     destination_nbo_reactive_ltv_test_table,
    # )
