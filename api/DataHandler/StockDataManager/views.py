from django.shortcuts import render
from .models import DataTable
import yfinance as yf
import datetime
from sqlalchemy import create_engine


def download_data(company_code, first_rating=datetime.datetime(1800, 1, 1), last_rating=datetime.date.today()):
    try:
        return yf.download(company_code, first_rating, last_rating)
    except:
        print('Data download error')


async def inject_data_to_db(request, company_code):
    tick = yf.Ticker(company_code)
    if not DataTable.objects.get(code=company_code).exist():
        dt = DataTable(code=company_code, name=tick.info['shortName'])
        dt.save()
        df = download_data(company_code)
        df['data_table_id'] = [DataTable.objects.get(code=company_code).id] * df.shape(0)
    else:
        print('Work in progress')
        # TODO: napisać co zrobić gdy dana firma została już dodana
