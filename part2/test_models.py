from app.services.facade import HBnBFacade

# Initialiser la façade
facade = HBnBFacade()

# Créer un amenity pour le test (si ce n'est pas déjà fait)
amenity_data = {"name": "Piscine"}
amenity = facade.create_amenity(amenity_data)
print(f"Amenity créé : {amenity.id} - {amenity.name}")

# ID que tu veux tester
test_amenity_id = "416af475-78cb-4402-85db-f6079e3ce6c6"

# Essayer de récupérer l'amenity
amenity_found = facade.get_amenity(test_amenity_id)

if amenity_found:
    print(f"Amenity trouvé : {amenity_found.id} - {amenity_found.name}")
else:
    print(f"Amenity avec l'ID {test_amenity_id} n'existe pas.")