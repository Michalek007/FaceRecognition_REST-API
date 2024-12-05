from flask import request, url_for, redirect, render_template, jsonify, current_app
import flask_login

from app.blueprints import BlueprintSingleton
from database.schemas import user_schema, users_schema, User


class UserBp(BlueprintSingleton):
    """ Implements views related to users. """

    # views
    def register(self):
        if request.method == 'GET':
            try:
                test_id = flask_login.current_user.id
            except AttributeError:
                test_id = None
            if test_id is not None:
                return redirect(url_for('auth.logged_in'))
            login = request.args.get('login')
            password = request.args.get('password')
            if not login:
                return render_template('user/register.html')
        else:
            login = request.form.get('login')
            password = request.form.get('password')
            repeat_password = request.form.get('repeat_password')
            if password != repeat_password:
                return jsonify(message='Passwords are not the same!'), 408
            if login is None or password is None:
                return jsonify(
                    message='No value. Expected values for keys: \'login\', \'password\', \'repeat_password\''), 400

        test_user = User.query.filter_by(username=login).first()
        if test_user:
            return jsonify(message='That username is already taken!'), 409
        else:
            pw_hash = current_app.config.get('bcrypt').generate_password_hash(password)
            new_user = User(username=login, pw_hash=pw_hash)
            current_app.config.get('db').session.add(new_user)
            current_app.config.get('db').session.commit()
            return jsonify(message='User created successfully.'), 201

    def logout(self):
        flask_login.logout_user()
        return jsonify(message='Logged out.')

    def protected(self):
        try:
            user_id = flask_login.current_user.id
        except AttributeError:
            return jsonify(logged_user="Anonymous user has no id!")
        return jsonify(logged_user=user_id)

    def users(self, user_id: int = None):
        if user_id is None:
            users_list = User.query.all()
            return jsonify(users=users_schema.dump(users_list))
        user = User.query.filter_by(id=user_id).first()
        if user:
            return jsonify(user=user_schema.dump(user))
        else:
            return jsonify(message='There is no user with that id'), 404

    # gui views
    def users_table(self):
        return render_template('user/users_table.html')
