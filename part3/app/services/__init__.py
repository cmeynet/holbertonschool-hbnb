from .facade import HBnBFacade

facade = HBnBFacade()

# Création d'un admin à chaque lancement de l'API
facade.create_user({'first_name': 'Vivi', 'last_name': 'Boubou', 'email': 'admin@gmail.com', 'password': 'admin', 'is_admin': True})
