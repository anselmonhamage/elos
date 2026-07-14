import json
from datetime import datetime
from models.database import db

class TributeContent(db.Model):
    __tablename__ = 'tribute_contents'

    id = db.Column(db.Integer, primary_key=True)
    section_key = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    image_filename = db.Column(db.String(255), nullable=True)
    image_filenames = db.Column(db.Text, nullable=True) # JSON list of images
    image_fit = db.Column(db.String(20), default='contain') # 'contain', 'cover', 'scale-down'
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_by_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True)

    updated_by = db.relationship('User')

    def get_images_list(self):
        import os
        from flask import current_app

        valid_exts = ('.jpg', '.jpeg', '.png', '.webp', '.gif', '.svg')

        try:
            upload_dir = current_app.config.get('UPLOAD_FOLDER')
            if upload_dir and os.path.exists(upload_dir):
                all_disk_files = [
                    f for f in os.listdir(upload_dir)
                    if f.lower().endswith(valid_exts)
                ]

                if self.image_filenames:
                    try:
                        lst = json.loads(self.image_filenames)
                        if isinstance(lst, list) and len(lst) > 0:
                            existing_in_uploads = []
                            for f in lst:
                                if f in all_disk_files and f not in existing_in_uploads:
                                    existing_in_uploads.append(f)
                            if existing_in_uploads:
                                return existing_in_uploads
                    except Exception:
                        pass

                if self.image_filename and self.image_filename in all_disk_files:
                    return [self.image_filename]

                if all_disk_files:
                    result = []
                    for f in sorted(all_disk_files):
                        if f not in result:
                            result.append(f)
                    return result
        except Exception:
            pass

        return []

    def to_dict(self):
        return {
            "id": self.id,
            "section_key": self.section_key,
            "title": self.title,
            "content": self.content,
            "image_filename": self.image_filename,
            "images_list": self.get_images_list(),
            "updated_at": self.updated_at.strftime("%d/%m/%Y %H:%M") if self.updated_at else ""
        }
