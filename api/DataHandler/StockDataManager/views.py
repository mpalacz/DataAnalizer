from django.shortcuts import render
from .models import DataTable, Stock
import yfinance as yf
import datetime
from sqlalchemy import create_engine
from api.DataHandler.DataHandler.settings import DATABASES as db
from django.http import HttpResponse


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
        latest_date = Stock.objects.filter(data_table=DataTable.objects.get(code=company_code).id).latest().date
        df = download_data(company_code, latest_date)
    engine = create_engine(f'mysql://{db.values("USER")}:{db.values("PASSWORD")}@{db.values("HOST")}:{db.values("PORT")}/{db.values("NAME")}')
    df.to_sql('stock', con=engine, if_exists='append')
    return HttpResponse(200)
