from app import db, Room, app

with app.app_context():
    db.create_all()
    if Room.query.count() == 0:
        for floor in range(1,4):
            for num in range(1,4):
                r = Room(floor=floor, number=f"{floor}0{num}", tenant=None)
                db.session.add(r)
        db.session.commit()
        print("Seeded 9 rooms")
    else:
        print("Rooms already exist")
