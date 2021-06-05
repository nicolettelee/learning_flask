import functools

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from scripts.database import get_db

bp = Blueprint('auth', __name__)

@bp.route("/register", methods=["GET", "POST"])
def register():
	if request.method == "POST":
		username = request.form["username"]
		password = request.form["password"]


		db = get_db()
		error = None

		invalid_chars = ["!", "?", "#", "$", "%", "&", "^", "*"]

		if not username:
			error = "Registration error: Username is required."
		elif not password:
			error = "Registration error: Password is required."
		elif any(invalid_char in username for invalid_char in invalid_chars):
			error = f"Username cannot contain any of the following characters: {','.join(invalid_chars)}"
		elif db.execute(
			"SELECT id from users WHERE username = ?", (username,)
		).fetchone() is not None:
			error = f"User '{username}' is already taken."

		if error is None:
			db.execute(
				"INSERT INTO users (username, password) VALUES (?, ?)",
				(username, generate_password_hash(password))
			)
			db.commit()

			flash(f"Registration for user {username} successful.")
			return redirect(url_for("auth.register"))
		else:
			flash(error)

	return render_template("register.html")