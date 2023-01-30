from flask_app import app
from flask import render_template, request, redirect, session
from flask_app.models.car_model import Car


@app.route('/cars')
def display_cars():
    if 'email' not in session:
        return redirect('/')
    list_cars = Car.get_all_with_users()
    return render_template('cars.html', list_cars = list_cars )

@app.route('/car/new')
def display_create_car():
    #validation
    if 'email' not in session:
        return redirect('/')
    #create and render
    return render_template("create_car.html")

@app.route( '/car/create', methods = ['POST'])
def create_car():
    #Validate
    if Car.validate_car( request.form ) == False:
        return redirect('/car/new')
    data = {
        **request.form,
        "user_id" : session['user_id']
    }
    Car.create(data)
    return redirect('/cars')

@app.route( '/cars/<int:id>')
def display_one( id ):
    if 'email' not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    current_car = Car.get_one_with_user( data )
    return render_template('car.html', current_car = current_car)

@app.route("/cars/<int:id>/update")
def display_update_car(id):
    if 'email' not in session:
        return redirect('/')
    data = {
        "id" : id
    }
    current_car = Car.get_one_with_user( data )
    return render_template("update_car.html", current_car= current_car)

@app.route('/car/update/<int:id>', methods = ['POST'])
def update_car( id ):
    if Car.validate_car(request.form) == False:
        return redirect(f'/cars/{id}/update')
    car_data = {
        **request.form,
        "id": id,
        "user_id": session['user_id']
    }
    Car.update_one( car_data )
    return redirect('/cars')

@app.route('/cars/<int:id>/delete')
def delete_car( id ):
    data = {
        "id": id
    }
    Car.delete_one(data)
    return redirect('/cars')
