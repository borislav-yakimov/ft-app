# # from google.auth import credentials
# # from google.cloud import bigquery


# # def get_bq_client():
# #     with bigquery.Client() as client:
# #         return client


# from decouple import config
# from google.cloud import bigquery
# from sqlmodel import Session, create_engine
# from sqlmodel.ext.asyncio.session import AsyncSession

# engine = create_engine(config("DATABASE_URL"), credentials_path=config("GOOGLE_APPLICATION_CREDENTIALS"), echo=True)


# def get_session():
#     with Session(engine) as session:
#         yield session


# def get_bigquery_client():
#     return bigquery.Client()
