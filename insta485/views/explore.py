import flask
import insta485

connection = insta485.model.get_db()

@insta485.app.get('/explore')
def explore():
    # if 'username' not in flask.session:
    #     flask.redirect(flask.url_for('login'))
    # logname = flask.session['username']
    #
    logname = 'awdeorio'
    not_following = connection.execute(
        "SELECT username, filename "
        "FROM users "
        "WHERE username NOT IN "
        "(SELECT username2 FROM following WHERE username1=?)",
        (logname,)
    ).fetchall()
    context = {"not_following": not_following, "logname": logname}

    return flask.render_template("explore.html", **context)