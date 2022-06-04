from flask import Blueprint, request, render_template, redirect, url_for, jsonify, flash
from app.libraries.data import Dataprep
from app.models import Rating, Hotel
from app.libraries.recommender import hotels_recommender, get_user_rating
from app.libraries.helpers import addBintangHotel
import pandas as pd

dataManager = Blueprint('datamanagement', __name__)

@dataManager.route("hotel", methods=["GET"])
def hotel():
    hotels = Hotel.objects.all()
    data = [{
        "itemId":i["itemId"],
        "itemName": i["itemName"],
        "bintang": i["bintang"]
    } for i in hotels]
    return jsonify({
        "data": data
    }), 200

@dataManager.route("submit", methods=["POST"])
def submit():
    data = request.get_json()
    user = data["user"]
    hotel_id = data["hotel_id"]
    rating = data["rating"]


    detect_user = Rating.objects(user=user).first()
    if detect_user:
        return jsonify({"message": "error"}), 400
    else:
        rate = Rating(
            user=user,
            rating=rating,
            itemId=hotel_id
        )
        rate.save()
        return jsonify({"message": "ok"}), 200


@dataManager.route("dump", methods=["POST"])
def dump():
    types = request.args.get("types")
    f = request.files['file']
    f.save("temp/"+ f.filename)
    
    if types == "hotels":
        df = pd.read_csv("temp/" + f.filename)  
        data = df.to_dict("records")
        for i in data:
            hotel = Hotel(
                itemId=i["Item_id"],
                itemName=i["Item_name"],
                bintang=i["Bintang_Hotel"]
            )
            hotel.save()
    else:
        df = pd.read_csv("temp/" + f.filename, sep=";")  
        df["User_Name"] = df["User_Name"].str.lower()
        data = df.to_dict("records")
        for i in data:
            rate = Rating(
                user=i["User_Name"],
                rating=i["Rating"],
                itemId=i["Item_id"]
            )
            rate.save()

    return jsonify("ok"), 200

@dataManager.route("recommendation", methods=["GET"])
def recommendation():
    user = request.args.get("user").lower()
    try:
        ratings = Rating.objects.all()
        hotels = Hotel.objects.all()
        preps =  Dataprep(hotels, ratings)
        
        df = preps.pivot_data()
        data = hotels_recommender(df, user)
        rated_hotel = {"itemName": get_user_rating(df, user)}

        df_hotel = preps.convert_hotel()
        data = addBintangHotel(data, df_hotel)
        rated_hotel = addBintangHotel(rated_hotel, df_hotel)

        return render_template('result.html', data=data, cols=["Nama Hotel", "Bintang","Prediksi Rating"], 
            rated_hotel=rated_hotel, cols_rated=["Nama Hotel", "Bintang", "Rating"],
                user=user)
    except:
        flash('User not found', 'error')
        return redirect(url_for('datamanagement.index'))


@dataManager.route("rated_hotel", methods=["GET"])
def rated_hotel():
    user = request.args.get("user")
    ratings = Rating.objects.all()
    hotels = Hotel.objects.all()
    df = Dataprep(hotels, ratings).pivot_data()
    data = get_user_rating(df, user)
    return jsonify({"data": data})


@dataManager.route("index", methods=["GET"])
def index():
   return render_template('index.html')

@dataManager.route("registrasi", methods=["GET", "POST"])
def registrasi():
    if request.method == "GET":
        hotels = Hotel.objects.all()
        return render_template('regis.html', hotel=hotels)
    else:
        name = request.form.get("nama")
        hotel = request.form.get("hotel")
        rating = request.form.get("rating")
        
        if ((name == "" or name == None) 
            and (rating == "" or rating == None) 
            and (hotel == "" or hotel == None)):
            flash('Please fill the blank value')
            return redirect(url_for('datamanagement.registrasi'))
        else:
            existing_data = Rating.objects(user=name, itemId=hotel).first()
            if existing_data:
                flash('You wass filled for a while ago ')
                return redirect(url_for('datamanagement.registrasi'))
            else:
                rate = Rating(
                    user=name,
                    rating=rating,
                    itemId=hotel
                )
                rate.save()
                return redirect(url_for('datamanagement.recommendation', user=name))

@dataManager.route("result", methods=["GET"])
def result():
   return render_template('result.html')

@dataManager.route('/', methods=["GET"])
def home():
    return redirect(url_for("datamanagement.index"))
