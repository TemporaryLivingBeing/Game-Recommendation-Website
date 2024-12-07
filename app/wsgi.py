
<<<<<<< HEAD
from contact import create_app as create_contact_app
from recommendations import create_rec_app
from app import app

contact = create_contact_app()
rec = create_rec_app()
=======
# from contact import create_app as create_contact_app
# from recommendations import create_rec_app
from app import create_app

# contact = create_contact_app()
# rec = create_rec_app()
app = create_app()
>>>>>>> 28d602a (Added databases and merged all .py files into app.py Fixes:#38, Fixes:#35)

if __name__ == "__main__":
    # contact.run()
    # rec.run()
    app.run()