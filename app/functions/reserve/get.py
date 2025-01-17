from flask import render_template
from flask_login import current_user
from app.model import Reserve


def get_sales_reserve(userid: int) -> list:
    return Reserve.query.filter(Reserve.owner == userid).all()


def reserve_table_results(reserves: list) -> str:
    return render_template(
        "reserve_table_results.html", current_user=current_user, reserves=reserves
    )
