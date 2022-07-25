from functools import wraps
from turtle import pu
from flask import Blueprint, request, jsonify
from Notes.models import User, Note
from . import db
import jwt

note= Blueprint('note',__name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify('Token is missing!'), 401

        try:
            data = jwt.decode(token, 'secret',algorithms=['HS256'])
            current_user = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            print(e)
            return jsonify('Token is invalid!'), 401

        return f(current_user, *args, **kwargs)

    return decorated

@note.route('',methods=['GET'])
@token_required
def get_all_notes(current_user):
    
    notes = Note.query.filter_by(user_id=current_user.id).all()

    output = []

    for note in notes:
        note_data = {}
        note_data['id'] = note.id
        note_data['description'] = note.description
        note_data['date'] = note.date
        output.append(note_data)
    return jsonify(output)


@note.route('',methods=['POST'])
@token_required
def create_note(current_user):
    
    if not 'description' in request.json:
        return jsonify('Please provide a Description.'),400

    description = request.json['description']

    new_note = Note(description=description, user_id=current_user.id)
    db.session.add(new_note)
    db.session.commit()

    return jsonify({ 'id' : new_note.id, 'description': new_note.description , 'date' : new_note.date }),201


@note.route('/<note_id>',methods=['GET'])
@token_required
def get_note(current_user,note_id):
    
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()

    if not note:
        return jsonify('No Note found!'),404

    note_data = {}
    note_data['id'] = note.id
    note_data['description'] = note.description
    note_data['date'] = note.date

    return jsonify(note_data)


@note.route('/<note_id>',methods=['PATCH'])
@token_required
def update_note(current_user,note_id):
    
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()

    if not note:
        return jsonify('No Note found!'),404

    if not 'description' in request.json:
        return jsonify('Please provide a Description.'),400

    note.description = request.json['description']
    db.session.commit()

    return jsonify({ 'id' : note.id, 'description': note.description , 'date' : note.date })


@note.route('/<note_id>',methods=['DELETE'])
@token_required
def delete_note(current_user,note_id):
    
    note = Note.query.filter_by(id=note_id, user_id=current_user.id).first()

    if not note:
        return jsonify('No Note found!'),404

    db.session.delete(note)
    db.session.commit()

    return '',204
    
    