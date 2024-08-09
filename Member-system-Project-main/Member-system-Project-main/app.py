#初始化資料庫連線
import pymongo
from flask import *
client=pymongo.MongoClient("mongodb+srv://root:*******@cluster0.tnn7i9f.mongodb.net/?retryWrites=true&w=majority")
db=client.member_system
#將資料庫物件存入db變數。
print("資料庫連線成功")

#初始化 Flask 伺服器
#指定靜態資源的資料夾路徑為"public"。

app=Flask(
__name__,
static_folder="public",
static_url_path="/"
)

app.secret_key="any string but secret"

#加密session的資料。
#處理路由

@app.route("/")
def index():
    return render_template("index.html")

#回傳"index.html"的樣板頁面。

@app.route("/member")
def member():

#權限控管
    if "nickname" in session:
        return render_template("member.html")
    else:
#導回首頁
        return redirect("/")
#會員權限控管
#/error?msg=錯誤訊息

@app.route("/error")
def error():
    message=request.args.get("msg","發生錯誤,請聯繫客服")
    return render_template("error.html", message=message)

@app.route("/signup",methods=["POST"])
def signup():
#從前端接收資料
    nickname=request.form["nickname"]
    email=request.form["email"]
    password=request.form["password"]
#和資料庫互動
    collection=db.user
#檢查會員集中是否有相同 Email 的文件資料
    result=collection.find_one({
    "email":email
    })
    if result !=None:
        return redirect("/error?msg=信箱已經被註冊")
#把文件資料放進資料庫，完成註冊
    collection.insert_one({
    "nickname":nickname,
    "email":email,
    "password":password
    })
    return redirect("/")
#檢查資料庫中是否已經有相同email的會員資料
@app.route("/signin", methods=["POST"])
def signin():
#從前端取得使用者的輸入
    email=request.form["email"]
    password=request.form["password"]
#和資料庫作互動
    collection=db.user
#檢查信箱密碼是否正確
    result=collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })  
#找不到對應的資料
    if result is None:
      return redirect("/error?msg=帳號或密碼輸入錯誤")
#登入成功
    session["nickname"]=result["nickname"]
    return redirect("/member")

@app.route("/signout")
def signout():
#移除session中的會員資訊
    del session["nickname"]
    return redirect("/")
#啟動伺服器
app.run(port=3000)