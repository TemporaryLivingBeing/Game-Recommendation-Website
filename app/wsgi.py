
from contact import create_app as create_contact_app
from recommendations import create_rec_app
from app import create_app

contact = create_contact_app()
rec = create_rec_app()
app = create_app()

if __name__ == "__main__":
    contact.run()
    rec.run()
    app.run()