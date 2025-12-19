from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from website.models import Note
from website import db
import json



view_bp = Blueprint('view_bp', __name__)

@view_bp.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_data = request.form.get('note')
        if not note_data or len(note_data.strip()) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note_data.strip(), user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category='success')
            return redirect(url_for('view_bp.home'))

    # Fetch all notes for current user and pass to template
    user_notes = Note.query.filter_by(user_id=current_user.id).order_by(Note.date.desc()).all()
    return render_template("home.html", notes=user_notes)


@view_bp.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    flash("Note deleted successfully.", category='success')
    return jsonify({})