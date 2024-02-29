from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.team import TeamModel
from schemas import TeamSchema, TeamUpdateSchema
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db


blp = Blueprint("teams", __name__, description="Operations on the teams")


@blp.route("/teams/<int:team_id>")
class Team(MethodView):
    @blp.response(200, TeamSchema)
    def get(self, team_id):
        return TeamModel.query.get_or_404(team_id)

    def delete(self, team_id):
        team = TeamModel.query.get_or_404(team_id)
        db.session.delete(team)
        db.session.commit()
        return {"message": "Team deleted"}

    @blp.arguments(TeamUpdateSchema)
    @blp.response(200, TeamSchema)
    def put(self, team_data, team_id):
        team = TeamModel.query.get(team_id)

        if team:
            team.title = team_data["title"] or team.title
            team.league = team_data["league"] or team.league
        else:
            team = TeamModel(**team_data)

            db.session.add(team)

        db.session.commit()

        return team


@blp.route("/teams/")
class TeamList(MethodView):
    @blp.response(200, TeamSchema(many=True))
    def get(self):
        return TeamModel.query.all()

    @blp.arguments(TeamSchema)
    @blp.response(201, TeamSchema)
    def post(self, team_data):
        team = TeamModel(**team_data)
        try:
            db.session.add(team)
            db.session.commit()
        except IntegrityError as er:
            abort(400, message=er)
        except SQLAlchemyError as er:
            abort(500, message=er)

        return team
