
from contact import create_app as create_contact_app
from recommendations import create_rec_app

application = create_contact_app()
rec = create_rec_app()

if __name__ == "__main__":
    application.run()
    rec.run()