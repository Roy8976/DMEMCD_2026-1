"""Herramientas didácticas mínimas para datos tabulares Olist (no limpia sin permiso).

Se usan únicamente los nueve archivos CSV en work-at-olist-data/datasets/.
No hay sustitución silenciosa por datos de demostración. Se validan las llaves.
"""
from __future__ import annotations
from pathlib import Path
import warnings
import numpy as np
import pandas as pd

FILE_NAMES = {
    'games': 'games.csv',
}
REQUIRED = ["AppID", "Name", "Genres", "Price", "Peak CCU", "Positive", "Negative"]
#EXPECTED = {
#    'orders': ['order_id','customer_id','order_status','order_purchase_timestamp','order_estimated_delivery_date'],
#    'customers': ['customer_id','customer_unique_id','customer_city','customer_state','customer_zip_code_prefix'],
#    'items': ['order_id','order_item_id','product_id','seller_id','price','freight_value'],
#    'payments': ['order_id','payment_sequential','payment_type','payment_installments','payment_value'],
#    'reviews': ['review_id','order_id','review_score'],
#    'products': ['product_id','product_category_name'],
#    'sellers': ['seller_id','seller_city','seller_state'],
#    'translation': ['product_category_name','product_category_name_english'],
#    'geolocation': ['geolocation_zip_code_prefix','geolocation_lat','geolocation_lng'],

#}
#DATE_COLS = {
#    'orders': ['order_purchase_timestamp','order_approved_at','order_delivered_carrier_date',
#              'order_delivered_customer_date','order_estimated_delivery_date'],
#    'items': ['shipping_limit_date'],
#    'reviews': ['review_creation_date','review_answer_timestamp'],
#}

def find_root(start: str | Path | None = None) -> Path:
    """Busca 'Proyectos' sin imponer una ruta absoluta ni mover los CSV."""
    p = Path(start or Path.cwd()).resolve()
    for q in (p, *p.parents):
        if ((q / 'Python' / 'game_tools.py').is_file()
                and (q / 'Proyecto').is_dir()):
            return q
    raise FileNotFoundError(
        'No se encontró la raíz del proyecto con Python/games_tools.py y '
        'Proyecto/games.csv. Abra VS Code en la carpeta Proyectos.'
    )

def detect_source(root: Path, prefer_real: bool = True):
    """Lee los nueve CSV reales desde work-at-olist-data/datasets/.

    Se conserva prefer_real por compatibilidad con los notebooks originales.
    """
    folder = Path(root).resolve() / 'Proyecto' 
    missing = [name for name in FILE_NAMES.values() if not (folder / name).is_file()]
    if missing:
        raise FileNotFoundError(
            'Faltan CSV en /Proyecto: ' + ', '.join(missing)
        )
    return folder, 'CSV reales suministrados: Proyecto/games.csv'


def read_tables(root: Path|None = None, prefer_real: bool = True, include_geo: bool = False):
    root = find_root() if root is None else Path(root)
    directory, source = detect_source(root, prefer_real)
    result = {}
    return result, source

def table_inventory(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    return pd.DataFrame([{
        'tabla':name,'filas':len(df),'columnas':df.shape[1],
        'nulos_en_celdas':int(df.isna().sum().sum()),
        'memoria_MiB':round(df.memory_usage(deep=True).sum()/2**20,2)
    } for name,df in tables.items()]).sort_values('tabla', ignore_index=True)

def _sum_min_count(s):
    return s.sum(min_count=1)

def build_order_level(tables: dict[str,pd.DataFrame]) -> pd.DataFrame:
    """Una fila por pedido, sin multiplicación por ítems/pagos/reseñas.

    Importante: order_id es único en orders, pero no en items, payments ni reviews.
    Los pagos se agregan por order_id y no se deben sumar nuevamente después
    de unir a los ítems individuales.
    """
    orders=tables['orders'].copy()
    if orders['order_id'].isna().any() or orders['order_id'].duplicated().any():
        raise ValueError('orders debe tener order_id único y no nulo. Diagnostique antes de unir.')
    customers=tables['customers'][['customer_id','customer_unique_id','customer_city','customer_state','customer_zip_code_prefix']]
    if customers['customer_id'].isna().any() or customers['customer_id'].duplicated().any():
        raise ValueError('customers.customer_id debe identificar una fila (no equivale a persona única).')
    items=tables['items']
    by_item=items.groupby('order_id', dropna=False).agg(
        n_items=('order_item_id','size'),
        subtotal_productos=('price',_sum_min_count),
        total_flete=('freight_value',_sum_min_count),
        precio_item_mediano=('price','median'),
        n_vendedores=('seller_id','nunique'),
    ).reset_index()
    payments=tables['payments'].sort_values(['order_id','payment_sequential'])
    by_pay=payments.groupby('order_id',dropna=False).agg(
        n_pagos=('payment_sequential','size'),
        total_pagado=('payment_value',_sum_min_count),
        medio_pago_inicial=('payment_type','first')
    ).reset_index()
    reviews=tables['reviews'].copy()
    if 'review_creation_date' in reviews:
        reviews=reviews.sort_values(['order_id','review_creation_date'])
    by_rev=reviews.groupby('order_id',dropna=False).agg(
        n_resenas=('review_score','size'),
        puntuacion_resena=('review_score','first')
    ).reset_index()
    result=(orders
        .merge(customers,on='customer_id',how='left',validate='many_to_one',indicator='_cliente_encontrado')
        .merge(by_item,on='order_id',how='left',validate='one_to_one')
        .merge(by_pay,on='order_id',how='left',validate='one_to_one')
        .merge(by_rev,on='order_id',how='left',validate='one_to_one'))
    assert len(result)==len(orders), 'Error: la unión duplicó pedidos.'
    result['valor_items_y_flete'] = result['subtotal_productos'] + result['total_flete']
    result['mes_compra'] = result['order_purchase_timestamp'].dt.to_period('M').astype('string')
    result['dia_semana'] = result['order_purchase_timestamp'].dt.day_name()
    result['dias_hasta_entrega']=(result['order_delivered_customer_date']-result['order_purchase_timestamp']).dt.total_seconds()/86400
    result['dias_retraso']=(result['order_delivered_customer_date']-result['order_estimated_delivery_date']).dt.total_seconds()/86400
    result['entrega_tardia']=result['dias_retraso'].gt(0).astype('boolean')
    result.loc[result['dias_retraso'].isna(),'entrega_tardia']=pd.NA
    # No asignar cero a entrega que no ocurrió; faltante estructural.
    result.loc[result['order_status']!='delivered',['dias_hasta_entrega','dias_retraso','entrega_tardia']]=pd.NA
    return result

def build_item_level(tables: dict[str,pd.DataFrame]) -> pd.DataFrame:
    """Una fila por línea de pedido: NO sumar después valores por pedido."""
    prods = tables['products']
    if prods['product_id'].duplicated().any():
        raise ValueError('products.product_id duplicado: revisar dimensión.')
    names = tables['translation']
    if names['product_category_name'].duplicated().any():
        raise ValueError('Tabla de traducciones con llaves duplicadas.')
    it=tables['items'].copy()
    it=(it.merge(prods,on='product_id',how='left',validate='many_to_one')
          .merge(names,on='product_category_name',how='left',validate='many_to_one'))
    it['categoria_mostrada']=it['product_category_name_english'].fillna(it['product_category_name']).fillna('Sin categoría')
    it['valor_item_con_flete']=it['price']+it['freight_value']
    return it

def missing_profile(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({'variable':df.columns,
        'faltantes':df.isna().sum().values,
        'porcentaje':(df.isna().mean().values*100).round(2),
        'tipo':df.dtypes.astype(str).values}).sort_values('porcentaje',ascending=False, ignore_index=True)

def safe_minmax(s: pd.Series)->pd.Series:
    s=pd.to_numeric(s,errors='coerce'); lo,hi=s.min(),s.max()
    return pd.Series(np.zeros(len(s)),index=s.index,dtype='float64').where(s.notna(),np.nan) if hi==lo else (s-lo)/(hi-lo)

def safe_zscore(s: pd.Series)->pd.Series:
    s=pd.to_numeric(s,errors='coerce'); std=s.std(ddof=1)
    return pd.Series(np.zeros(len(s)),index=s.index,dtype='float64').where(s.notna(),np.nan) if pd.isna(std) or std==0 else (s-s.mean())/std
