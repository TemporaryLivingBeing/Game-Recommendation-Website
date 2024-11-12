
from contact import create_app as create_contact_app
from recommendations import create_rec_app

contact = create_contact_app()
rec = create_rec_app()

if __name__ == "__main__":
    contact.run()
    rec.run()