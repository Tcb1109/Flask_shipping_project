from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from sqlalchemy.exc import SQLAlchemyError
from app.model import Reserve, db
from datetime import datetime

from app.functions.validate import (
    is_checked_key,
    is_valid_reserve_form,
    now_or_valid_date,
    zero_or_valid_number,
)


def new_reserve_page(spc_id: int) -> str:
    return render_template(
        "shipping_reserve.html",
        mode="add",
        data=Reserve(
            spc_id=spc_id,
            sales="",
            saleprice=0,
            rsv_date=datetime.now(),
            cfm_date=datetime.now(),
            cfm_cs="",
            void=False,
            remark="",
        ),
    )


def new_populated_reserve_page(form: dict, spc_id: int) -> str:
    return render_template(
        "shipping_reserve.html",
        mode="add",
        data=Reserve(
            spc_id=spc_id,
            sales=form["sales"],
            saleprice=zero_or_valid_number(form["saleprice"]),
            rsv_date=now_or_valid_date(form["rsv_date"]),
            cfm_date=now_or_valid_date(form["cfm_date"]),
            cfm_cs=form["cfm_cs"],
            void=form.get("void", ""),
            remark=form["remark"],
        ),
    )


def create_reserve(form: dict, spc_id: int) -> int:
    if not is_valid_reserve_form(form):
        flash("Some of your changes are invalid. Please try again.", "danger")
        return new_populated_reserve_page(form, spc_id)

    try:
        new_reserve = Reserve(
            spc_id=spc_id,
            sales=form["sales"],
            saleprice=int(form["saleprice"]),
            rsv_date=datetime.strptime(form["rsv_date"], "%Y-%m-%d"),
            cfm_date=datetime.strptime(form["cfm_date"], "%Y-%m-%d"),
            cfm_cs=form["cfm_cs"],
            void=is_checked_key(form, "void"),
            remark=form["remark"],
            owner=current_user.id,
        )
        db.session.add(new_reserve)
        db.session.commit()
        flash("Reserve created successfully!", "success")
        return redirect(url_for("reserve.reserve_edit", rsv_id=new_reserve.rsv_id))
    except SQLAlchemyError as e:
        db.session.rollback()
        flash(f"Database error: {str(e)}", "danger")
        return -1
    except ValueError as e:
        flash(f"Value error: {str(e)}", "danger")
        return -1
