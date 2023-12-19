import flask
import insta485

@insta485.app.route('/users/<user_url_slug>/')
def show_user(user_url_slug):
    logname = awdeorio
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM users "
        "WHERE username == ?",
        (username,)
    ).fetchall()
    if len(cur) == 0:
        flask.abort(404)
        cur = connection.execute(
        "SELECT fullname FROM users "
        "WHERE username == ?",
        (user_url_slug, )
    )
    fullname = cur.fetchall()[0]['fullname']

    cur = connection.execute(
        "SELECT postid, filename FROM posts "
        "WHERE owner == ?",
        (user_url_slug, )
    )
    posts = cur.fetchall()

    # Add database info to context
    context = {"logname": logname, "username": user_url_slug,
               "logname_follows_username": follows(logname, user_url_slug),
               "fullname": fullname, "current_url": flask.request.path,
               "following": len(get_following_list(user_url_slug)),
               "followers": len(get_followers_list(user_url_slug)),
               "total_posts": len(posts), "posts": posts}
    return flask.render_template("user.html", **context)

def get_following_list(user_url_slug):
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE username1 == ?",
        (username,)
    )
    following_list = [d['username2'] for d in cur.fetchall()]
    return following_list

def get_followers_list(user_url_slug):
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE username2 == ?",
        (username,)
    )
    followers_list = [d['username1'] for d in cur.fetchall()]
    return followers_list
