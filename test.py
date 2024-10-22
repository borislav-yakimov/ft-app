from google.cloud import bigquery

client = bigquery.Client(project="ft-data-science")

results_ds = client.query(
    """
    SELECT *
    FROM `ft-data-science.test.test-newsletter-metadata`
    """
).to_dataframe()

print(results_ds)
