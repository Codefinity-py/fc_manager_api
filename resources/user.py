from flask.views import MethodView
from flask_smorest import Blueprint

from models import UserModel
from schemas import UserSchema

blp = Blueprint("users", __name__, description="Operations on the users")


@blp.route("/users/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id)


@blp.route("/users/")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()
