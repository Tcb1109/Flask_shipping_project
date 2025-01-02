from app.permissions import rank_required
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from app.functions.schedule.new import new_schedule, new_schedule_page
from app.functions.schedule.edit import edit_schedule, edit_schedule_page
from app.functions.schedule.delete import delete_schedule

schedule_routes = Blueprint(
    "schedule",
    __name__,
    template_folder="../../templates",
    static_folder="../../static",
)


@schedule_routes.route("/add", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def schedule_add():
    if request.method == "POST":
        new_schedule_id = new_schedule(request.form)
        if new_schedule_id != -1:
            return schedule_edit(new_schedule_id)
    return new_schedule_page()


@schedule_routes.route("/edit/<int:sch_id>", methods=["GET", "POST"])
@login_required
@rank_required(["admin"])
def schedule_edit(sch_id: int):
    if request.method == "POST":
        if edit_schedule(sch_id):
            # Returning to a new updated list
            return redirect(url_for("user.user_home"))
    return edit_schedule_page(sch_id)


@schedule_routes.route("/delete/<int:sch_id>", methods=["GET"])
@login_required
@rank_required(["admin"])
def schedule_delete(sch_id: int):
    delete_schedule(sch_id)
    return redirect(url_for("user.user_home"))
