from package import app, db

if __name__ == "__main__":
    with app.app_context():
        # Create all tables for the main database (HealthCheckAPI.db)
        db.create_all()

    app.run(debug=True)