# Import libraries
# 导入第三方库
import os
import cs50
import pytz
import datetime
from flask import Flask, render_template, request, redirect, session
from flask_mail import Mail, Message
from flask_session import Session
from flask_avatars import Avatars
from flask_script import Manager
from werkzeug.security import check_password_hash, generate_password_hash

# Import local .py file
# 导入本地的config文件
from config import login_required, encode_token, decode_token, generate_url, hash_email

# Configure application
# 配置应用
app = Flask(__name__,
            static_url_path="/static",
            static_folder="static")
app.config['SECRET_KEY'] = 'THISisAsecretKEYYYY'

# Configure mail
# 配置邮件发送
app.config['MAIL_SERVER'] = ''
app.config['MAIL_PORT'] = ''
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
app.config['MAIL_USE_TLS'] = ''
app.config['MAIL_USE_SSL'] = ''
mail = Mail(app)

MyEmailAddress = ''

# Ensure templates are auto-reloaded
# 确保模板为自动加载
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
# 配置会话使用filesystem，而不是使用cookies
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# 配置CS50库以便使用SQLite数据库
db = cs50.SQL("sqlite:///hotaru.db")

# Configure avatar
# 配置头像
app.config['UPLOAD_FOLDER'] = "/static/icons/"
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024  # 1MB
avatars = Avatars(app)

# Configure script
# 配置Flask-Script便于调试
manager = Manager(app)


@app.after_request
def after_request(response):
    """
    Ensure responses are not cached
    确保响应不被缓存
    """
    
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """
    Show default page
    显示默认页面
    """
    
    try:
        if session["user_id"]:
            return redirect("/chat/general")
    except KeyError:
        return render_template("index.html")
    
    
@app.route("/chat")
@login_required
def chat_none():
    """
    Redirect to general channel
    重定向到general频道
    """
    
    return redirect("/chat/general")


@app.route("/chat/<name>", methods=["GET", "POST"])
@login_required
def chat(name):
    """
    Show channel
    显示频道
    """
    
    # Declare error
    # 声明错误信息
    error = None
    
    if request.method == "POST":
        if not request.form.get("textArea"):
            return redirect(f"/chat/{name}")
        
        # Get username that POST
        # 获取发送信息的用户名
        username = db.execute("SELECT name FROM users WHERE id = ?",
                              session["user_id"])
        username = str(username[0]["name"])
        
        # Get current channel id
        # 获取当前频道的ID
        current_channel = db.execute("SELECT id FROM channel WHERE name = ?",
                                     name)
        current_channel = int(current_channel[0]["id"])
        
        # Get current time
        # 获取当前的时间
        current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
        datetime_format = '%Y-%m-%d %H:%M:%S'
        current_time = current_time.strftime(datetime_format)
        
        # Add new record: text, sender_id, sender_name, channel_id, and time
        # 添加新的聊天记录至数据库
        db.execute("INSERT INTO chat (text, sender_id, sender_name, channel_id, time)VALUES(?, ?, ?, ?, ?)",
                   request.form.get("textArea"),
                   session["user_id"],
                   username,
                   current_channel,
                   current_time)
        
        return redirect(f"/chat/{name}")
    
    # Display chat records
    # 显示聊天记录
    # Get channel's info
    # 获取频道的信息，例如频道名
    channels = db.execute("SELECT * FROM channel WHERE name = ?", name)
    channel_name = name
    channel_name = channel_name.capitalize()
    
    # Get profile's info
    # 获取当前用户的信息
    profile = db.execute("SELECT * FROM users WHERE id = ?",
                         session["user_id"])
    
    # Get user's profile name and icon
    # 获取当前用户的用户名和头像
    try:
        profile_name = str(profile[0]["name"])
        profile_icon = str(profile[0]["icon"])
    except IndexError:
        session.clear()
    
    # Get chat record
    # 获取聊天记录
    try:
        records = db.execute("SELECT * FROM chat WHERE channel_id = ? ORDER BY id DESC",
                              channels[0]["id"])
    except IndexError:
        records = []  
    
    # Get chat-ers' profile icons
    # 获取每条聊天记录所对应的用户的头像
    for chat_record in records:
        sender_id = chat_record["sender_id"]
        user_profile = db.execute("SELECT icon FROM users WHERE id = ?", sender_id)
        chat_record["icon"] = user_profile[0]["icon"]

    return render_template("index.html", 
                           channels=channels,
                           profile_name=profile_name,
                           profile_icon=profile_icon, 
                           channel_name=channel_name,
                           records=records,
                           name_URL=name)

    
@app.route("/profile", methods=["GET", "POST"])
@login_required
def editprofile():
    """
    Edit user's profile
    编辑用户个人信息
    """
    
    warning = None
        
    # Get profile's info
    # 获取当前用户的信息
    profile = db.execute("SELECT * FROM users WHERE id = ?",
                         session["user_id"])
    
    # Get user's profile name and icon
    # 获取当前用户的用户名和头像
    try:
        profile_name = str(profile[0]["name"])
        profile_icon = str(profile[0]["icon"])
        profile_email = profile[0]['email_address']
        confirmed_time = str(profile[0]["confirmed_time"])
        confirmed_time = confirmed_time[0:10]
    except IndexError:
        session.clear()
        
    if request.method == "POST":
        # Ensure one of the radios was chosen
        # 确保用户提交前选择了任一单选框
        if request.values.get("firstRadio"):
            first_radio = request.values.get("firstRadio")
            if first_radio == "uploadRadio":
                # Ensure the user uploads a file
                # 确保用户上传了一个文件
                if not request.files.get("file"):
                    warning = 'Must upload a file'
                    
                else:
                    # Get file, and its suffix
                    # 获取用户上传的文件以及其后缀
                    file = request.files['file']
                    file_name = file.filename
                    file_name_suffix = str(os.path.splitext(file_name)[-1])
                    
                    # Ensure the file is a picture
                    # 确保用户上传的是一张图片
                    if not (file_name_suffix.lower() == ".jpeg" or file_name_suffix.lower() == ".png" or file_name_suffix.lower() == ".jpg"):
                        warning = 'File must be jpeg, png, or jpg'
                    
                    else:
                        # Save the file to the specific directory
                        # 保存图片至指定路径
                        basedir = os.path.abspath(os.path.dirname(__file__))
                        file_name_suffix = ".png"
                        file_name_new = profile_email + file_name_suffix
                        path = basedir + r"\\static\\icons\\"
                        # If the file already exists, remove it first, then save a new one
                        if os.path.exists(str(path + file_name_new)):
                            os.remove(path+ file_name_new)
                        file.save(path + file_name_new)
                        
                        # Update the icon address
                        # 更新用户头像地址
                        db.execute("UPDATE users SET icon=? WHERE id=?",
                                str("/static/icons/" + profile_email + file_name_suffix),
                                session["user_id"])
                        
                    return redirect("/profile")
            
            elif first_radio == "createRadio":
                # Ensure the user chooses one of the styles
                # 确保用户选择了任一头像风格
                if request.values.get("secondRadio"):
                    second_radio = request.values.get("secondRadio")
                    
                    # Generate hash for user's email
                    avatar_URL = f'https://www.gravatar.com/avatar/{hash_email(profile_email)}?d='

                    if second_radio == "createRadioDefault":
                        avatar_URL = avatar_URL + 'identicon'
                    elif second_radio == "createRadioMonster":
                        avatar_URL = avatar_URL + 'monsterid'
                    elif second_radio == "createRadioRobot":
                        avatar_URL = avatar_URL + 'robohash'
                    elif second_radio == "createRadioWav":
                        avatar_URL = avatar_URL + 'wavatar'
                    elif second_radio == "createRadioBit":
                        avatar_URL += 'retro'
                    avatar_URL = avatar_URL + '&s=1007'
                    
                    # Update user's profile icon address
                    # 更新用户头像链接至数据库
                    db.execute("UPDATE users SET icon=? WHERE id=?",
                               avatar_URL,
                               session["user_id"])
                    
                    return redirect("/profile")
                else:
                    warning = "Must provide style"
            else:
                warning = "Must choose one"
    
    return render_template("editprofile.html",
                           warning=warning,
                           profile_name=profile_name,
                           profile_icon=profile_icon,
                           confirmed_time=confirmed_time)


@app.route("/contact", methods=["GET", "POST"])
@login_required
def contact():
    """
    Have the user contact the team
    让用户与团队联系
    """

    success = None
    warning = None
    
    # Declare variables for email
    title = None
    content = None
    
    # Get profile's info
    # 获取当前用户的信息
    profile = db.execute("SELECT * FROM users WHERE id = ?",
                         session["user_id"])
    
    # Get user's profile name and icon
    # 获取当前用户的用户名和头像
    try:
        profile_name = str(profile[0]["name"])
        profile_icon = str(profile[0]["icon"])
        profile_email = profile[0]['email_address']
        confirmed_time = str(profile[0]["confirmed_time"])
        confirmed_time = confirmed_time[0:10]
    except IndexError:
        session.clear()
    
    if request.method == "POST":
        if request.form.get("selected"):
            selected_value = request.form.get("selected")
            if selected_value != "Select a topic":
                selected_value = int(selected_value)
                if selected_value == 1:
                    title = "Question"
                elif selected_value == 2:
                    title = "Function Advice"
                elif selected_value == 3:
                    title = "Design Enhancement"
                elif selected_value == 4:
                    title = "Comments"
                elif selected_value == 5:
                    title = "Others"
                    
                content = request.form.get("textArea")
                
                # Send email confirmation
                # 发送邮箱
                email = MyEmailAddress
                msg = Message(title + " | Hotaru",
                            sender=("Hotaru Team", "hotaru@cytrogen.icu"),
                            recipients=[email])
                
                msg.html = render_template("email/contact.html",
                                           profile_name=profile_name,
                                           content=content)
                mail.send(msg)
                success = "You have successfully send the message!"
            else:
                warning = "Must select a topic"
    
    return render_template("contact.html",
                           profile_name=profile_name,
                           profile_icon=profile_icon,
                           warning=warning,
                           success=success)


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Log user in
    用户登录
    """
    
    try:
        if session["user_id"]:
            return redirect("/")
    except:
        pass

    # Forget any user id
    # 失忆，清除会话
    session.clear()
    
    # Declare error
    # 声明错误信息
    error = None
    
    if request.method == "POST":
        # Ensure username was submitted
        # 确保用户名已填写
        if not request.form.get("username"):
            error = 'Invalid username'
            return render_template("login.html",
                                   error=error)
        
        # Ensure password was submitted
        # 确保用户密码已填写
        if not request.form.get("password"):
            error = 'Invalid password'
            return render_template("login.html",
                                   error=error)
        
        try:
            # Get all user infos
            # 获取所有的用户信息
            rows = db.execute("SELECT * FROM users WHERE name = ?",
                              request.form.get("username"))
            
            # Ensure username does not exist and password is correct
            # 确保用户名存在，且用户密码正确
            if len(rows) != 1 or not check_password_hash(rows[0]["password"],
                                                         request.form.get("password")):
                error = 'Invalid username/password'
                return render_template("login.html",
                                       error=error)
                
            # Ensure the user has confirmed their Email address
            # 确保用户验证了邮箱
            if rows[0]["confirmed"] != "True":
                error = 'Account not activated.'
                return render_template("login.html",
                                       error=error)
        
        except RuntimeError:
            error = 'Invalid username/password'
            return render_template("login.html",
                                   error=error)
        
        # Establish session
        # 建立会话
        session["user_id"] = rows[0]["id"]
        
        # Redirect user to home page
        # 重定向至主页面
        return redirect("/")
    
    else:
        return render_template("login.html")
    
    
@app.route("/signup", methods=["GET", "POST"])
def signup():
    """
    Sign user up
    用户注册
    """
    
    try:
        if session["user_id"]:
            return redirect("/")
    except:
        pass
    
    # Forget any user id
    # 失忆，清除会话
    session.clear()
    
    # Declare notifier
    # 声明错误和警告信息
    error = None
    warning = None
    
    if request.method == "POST":
        # Ensure email address was submitted
        # 确保邮箱地址已填写
        if not request.form.get("emailaddress"):
            error = "Missing email"
            return render_template("signup.html",
                                   error=error)
        
        # Ensure username was submitted
        # 确保用户名已填写
        if not request.form.get("username"):
            error = "Missing username"
            return render_template("signup.html",
                                   error=error)
        
        # Ensure password was submitted
        # 确保用户密码已填写
        if not request.form.get("password"):
            error = "Missing password"
            return render_template("signup.html",
                                   error=error)
        else:
            if len(request.form.get("password")) < 8:
                error = "Invalid password"
                return render_template("signup.html",
                                       error=error)
        
        # Ensure password confirmation was submitted
        # 确保密码验证已填写
        if not request.form.get("confirmation"):
            error = "Missing password"
            return render_template("signup.html",
                                   error=error)
        
        # Confirm the passwords match
        # 确保密码和密码验证相同
        if request.form.get("password") != request.form.get("confirmation"):
            error = "Passwords do not match"
            return render_template("signup.html",
                                   error=error)
        # Generate hash
        # 生成哈希
        else:
            hash = generate_password_hash(request.form.get("password"))
        
        try:
            # Check username's availability
            # 检查用户名是否可用
            check = db.execute("SELECT name FROM users WHERE name = ?",
                               request.form.get("username"))
            if len(check) > 0:
                error = "Username not available"
                return render_template("signup.html",
                                       error=error)
        except RuntimeError:
            pass
        
        # Send email confirmation
        # 发送邮箱验证
        email = request.form.get("emailaddress")
        username = request.form.get("username")
        token = encode_token(email)
        activation_URL = generate_url('confirm_email', token)
        
        msg = Message("Confirm your Email address!",
                      sender=("Hotaru Team", "hotaru@cytrogen.icu"),
                      recipients=[email])
        
        msg.html = render_template("email/index.html",
                                   username=username,
                                   activation_URL=activation_URL)
        mail.send(msg)
        
        # Insert the username and hash into the database
        # 插入用户名和哈希至数据库
        db.execute("INSERT INTO users (name, password, icon, email_address, confirmed) VALUES (?,?,?,?,?)",
                   request.form.get("username"),
                   hash,
                   '/static/icons/Hotaru.png',
                   email,
                   'False')
        
        warning = 'Please check your inbox for the link.'
        
        return render_template("login.html",
                               warning=warning)
    
    else:
        return render_template("signup.html")
    
    
@app.route("/confirm/<token>")
def confirm_email(token):
    """
    Confirm the user's Email address
    """
    
    # Declare notifer
    # 声明错误和成功信息
    warning = None
    success = None
    
    # Decode the token and get the Email address
    # 解码令牌并获取邮件地址
    email = decode_token(token)
    
    # Get current time
    # 获取当前时间
    current_time = datetime.datetime.now(pytz.timezone('US/Eastern'))
    datetime_format = '%Y-%m-%d %H:%M:%S'
    current_time = current_time.strftime(datetime_format)
    
    if not email:
        warning = 'The confirmation link is invalid or has expired.'
        return render_template("signup.html",
                               warning=warning)
        
    # Get user information
    # 获取用户信息
    try:
        user = db.execute("SELECT * FROM users WHERE email_address = ?",
                          email)
                            
    except Exception:
        warning = "You haven't sign up yet."
        return render_template("signup.html",
                               warning=warning)
        
    # Mark the user as Email address confirmed
    # 更新用户数据
    db.execute("UPDATE users SET confirmed = ?, confirmed_time = ?",
               'True',
               current_time)
    
    success = 'You have successfully activated your account.'
    
    return render_template("login.html",
                           success=success)
        
    
@app.route("/logout")
def logout():
    """
    Log user out
    """
    
    # Forget any user id
    # 失忆，清除会话
    session.clear()
    
    # Redirect user to login form
    # 重定向至登录页面
    return redirect("/login")


if __name__ == '__main__':
    app.run()