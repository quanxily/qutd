from flask import Flask, render_template,request
from datetime import datetime

import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route("/")
def index():
    x ="作者:楊荃喜11/23<br>"
    x +="<a href=/mis>資管導論</a><br>"
    x +="<a href=/today>日期時間</a><br>"
    x +="<a href=/about>荃喜網頁</a><br>"
    x +="<a href=/welcome?nick=荃喜>歡迎蒞臨</a><br>"
    x +="<a href=/account>mmi密碼</a><br>"
    x +="<a href=/sort>人選之人名單</a><br>"
    x +="<a href=/books>精選圖書列表</a><br>"
    x +="<a href=/search>圖書查詢</a><br>"
    return x

@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    now = datetime.now()
    return render_template("today.html",datetime = str(now))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
     user = request.values.get("nick")
     return render_template("welcome.html", name=user)

@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/sort")
def sort():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("人選之人")    
    docs = collection_ref.order_by("date",direction=firestore.Query.DESCENDING).get()   
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/books")
def books():
    Result = ""
    db = firestore.client()
    collection_ref = db.collection("圖書精選")    
    docs = collection_ref.order_by("anniversary").get()   
    for doc in docs: 
        bk = doc.to_dict()        
        Result += "書名：<a href="+ bk["url"] + ">"+ bk["title"] + "</a><br><br>"
        Result += "作者：" + bk["author"] + "<br><br>"
        Result += str(bk["anniversary"]) + "週年紀念版""<br><br>" 
        Result += "<img src=" + bk["cover"] +"></img><br><br>"        
    return Result

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        keyword = request.form["keyword"]
        Result = "您輸入的關鍵字是：" + keyword
        db = firestore.client()
        collection_ref = db.collection("圖書精選")    
        docs = collection_ref.order_by("anniversary").get()   
        for doc in docs: 
            bk = doc.to_dict() 
            if keyword in bk["title"]:       
                Result += "書名：<a href="+ bk["url"] + ">"+ bk["title"] + "</a><br><br>"
                Result += "作者：" + bk["author"] + "<br><br>"
                Result += str(bk["anniversary"]) + "週年紀念版""<br><br>" 
                Result += "<img src=" + bk["cover"] +"></img><br><br>" 
        return Result
    else:
        return render_template("searchbk.html")




if __name__ == "__main__":
    app.run()

