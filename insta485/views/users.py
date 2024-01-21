import flask
import insta485
from insta485 import model

@insta485.app.route('/users/<user_url_slug>/')

def show_user(user_url_slug):
    logname = "awdeorio"  # Set logname to the correct value
    connection = model.get_db()
    
    cur = connection.execute(
        "SELECT * FROM users "
        "WHERE username == ?",
        (user_url_slug,)
    ).fetchall()
    
    if len(cur) == 0:
        flask.abort(404)

    # Retrieve user details
    user_data = cur[0]
    fullname = user_data['fullname']

    # Retrieve user posts
    cur = connection.execute(
        "SELECT postid, filename FROM posts "
        "WHERE owner == ?",
        (user_url_slug,)
    )
    posts = cur.fetchall()

    # Add database info to context
    context = {
        "logname": logname,
        "username": user_url_slug,
        "logname_follows_username": follows(logname, user_url_slug),
        "fullname": fullname,
        "current_url": flask.request.path,
        "following": len(get_following_list(user_url_slug)),
        "followers": len(get_followers_list(user_url_slug)),
        "total_posts": len(posts),
        "posts": posts
    }

    return flask.render_template("user.html", **context)

# Following Users
@insta485.app.route('/users/<user_url_slug>/following/')
def following_page(user_url_slug):
    connection = model.get_db()

    # Check if the user exists in the database
    cur = connection.execute(
        "SELECT * FROM users "
        "WHERE username == ?",
        (user_url_slug,)
    ).fetchall()

    if len(cur) == 0:
        flask.abort(404)
    logname = "awdeorio"  # Replace with the logged-in user's username

    # Get the users that the specified user is following
    cur = connection.execute(
        "SELECT u.username, u.fullname "
        "FROM users u "
        "JOIN following f ON u.username = f.username2 "
        "WHERE f.username1 = ?",
        (user_url_slug,)
    )
    following_users = cur.fetchall()

    # Render the HTML template with the 'follows' function in the context
    return flask.render_template(
        "following.html",
        logname=logname,
        user_url_slug=user_url_slug,
        following_users=following_users,
        follows=follows  # Include the 'follows' function in the context
    )

# Followers Users
@insta485.app.route('/users/<user_url_slug>/followers/')
def show_followers(user_url_slug):
    logname = 'awdeorio'
        # Connect to database
    connection = insta485.model.get_db()

        # Query database for people following users user_url_slug
    cur = connection.execute(
            "SELECT username1 "
            "FROM following "
            "WHERE username2 = ?",
            (user_url_slug,)
        )
    result = cur.fetchall()    

        # get detailed profile of people following user_url_slug
    followers = []
    for profile in result:
        cur = connection.execute(
                "SELECT username, filename "
                "FROM users "
                "WHERE username = ?",
                (profile["username1"],)
            )
        result = cur.fetchall()
        followers += result

        # Query database for anyone following user
    userFollowing = []
    cur = connection.execute(
            "SELECT username2 "
            "FROM following "
            "WHERE username1 = ?",
            (logname,)
        )
    result = cur.fetchall()

    for profile in result:
        userFollowing += [profile["username2"]]

    context = {"followers":followers,
                    "userFollowing": userFollowing,
                    "logname":logname,
                    "currentPageUser":user_url_slug
                    }                    
    return flask.render_template("followers.html", **context)
    # connection = model.get_db()
    #     # Check if the user exists in the database
    # usernameCheck(user_url_slug)

    # followers = connection.execute(
    #     "SELECT following.username1, users.filename "
    #     "FROM following "
    #     "INNER JOIN users "
    #     "ON following.username1 = users.username "
    #     "Where following.username2 == ? ",
    #     ( user_url_slug,)
    # ).fetchall()
    # context = {"userFollowers": followers, "logname": logname}
    # return flask.render_template("followers.html", **context)

def get_following_list(user_url_slug):
    connection = model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE username1 == ?",
        (user_url_slug,)
    )
    following_list = [d['username2'] for d in cur.fetchall()]
    return following_list

def get_followers_list(user_url_slug):
    connection = model.get_db()
    cur = connection.execute(
        "SELECT * FROM following "
        "WHERE username2 == ?",
        (user_url_slug,)
    )
    followers_list = [d['username1'] for d in cur.fetchall()]
    return followers_list

def follows(logname, user_url_slug):
    connection = model.get_db()
    result = connection.execute(
        'SELECT COUNT(*) '
        'FROM following '
        'WHERE username1 = ? AND username2 = ?',
        (logname, user_url_slug)
    ).fetchone()

    return result

def usernameCheck(name):
    connection = model.get_db()
    userExists = connection.execute(
        "SELECT username "
        "FROM users "
        "WHERE username == ? ",
        (name,)
    ).fetchall()
    if not userExists:
        flask.abort(404)
    return userExists