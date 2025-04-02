from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
},strict = True)

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Crear un nuevo amenity (Solo admins)"""
        current_user = get_jwt_identity()  #obtiene el usuario actual
        
        if not current_user['is_admin']: #si el usuario no es admin
            return {'error': 'Admin privileges required'}, 403

        data = api.payload #obtiene los datos del amenity a crear
        if not data or 'name' not in data: #si no hay datos o no hay nombre
            return {'message': 'Invalid input data'}, 400

        amenity = facade.create_amenity(data) #crea un nuevo amenity
        return {'id': amenity.id, 'name': amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        from app.services import facade
        """Retrieve a list of all amenities"""
        list_amenity = facade.get_all_amenities()
        return [{'id': amenity.id, 'name': amenity.name} for amenity in list_amenity], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        from app.services import facade
        """Get amenity details by ID"""
        amenity = facade.amenity_repo.get(amenity_id)
        
        if not amenity_id:
            return {"error": "Amenity not found"}, 404
        
        return {'id': amenity.id, 'name': amenity.name}, 200

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information (Admins only)"""
        current_user = get_jwt_identity()  #Obtener usuario autenticado

        if not current_user['is_admin']: #si el usuario no es admin
            return {'error': 'Admin privileges required'}, 403

        data = api.payload #obtiene los datos del amenity a modificar
        amenity = facade.amenity_repo.get(amenity_id) #obtiene el amenity
        if not amenity: #si el amenity no existe
            return {'error': 'Amenity not found'}, 404

        updated_amenity = facade.amenity_repo.update(amenity_id, data) #modifica el amenity
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200
@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        from app.services import facade
        """Admin modifies an amenity"""
        current_user = get_jwt_identity() #obtiene el usuario actual
        if not current_user['is_admin']: #si el usuario no es admin
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json #obtiene los datos del amenity a modificar
        updated_amenity = facade.update_amenity(amenity_id, amenity_data) #modifica el amenity
        return {'message': 'Amenity updated successfully'}, 200

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        from app.services import facade
        """Admin creates an amenity"""
        current_user = get_jwt_identity() #obtiene el usuario actual
        if not current_user['is_admin']: #si el usuario no es admin
            return {'error': 'Admin privileges required'}, 403

        amenity_data = request.json #obtiene los datos del amenity a crear
        new_amenity = facade.create_amenity(amenity_data) #crea un nuevo amenity
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201
