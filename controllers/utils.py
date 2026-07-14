from models.database import db
from models.models import TributeContent

def get_or_create_section(section_key, default_title, default_content, default_image=None):
    sec = TributeContent.query.filter_by(section_key=section_key).first()
    if not sec:
        sec = TributeContent(
            section_key=section_key,
            title=default_title,
            content=default_content,
            image_filename=default_image
        )
        db.session.add(sec)
        db.session.commit()
    return sec
