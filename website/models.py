from .db import db,fs
from datetime import datetime
import uuid
import codecs


# User class
class User():
    def __init__(self, username, email, password, _id=None):
        # Main initialiser
        self.username = username
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "_id": self._id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self._id)


class Post():
    def __init__(self, username, title, content, img_id=None, created_date=datetime.utcnow().strftime("%d %B %Y %H:%M:%S"), _id=None):
        self.username = username,
        self.title = title
        self.content = content
        self.img_id = img_id
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save(self):
        post_data = {
            '_id': self._id,
            'username': self.username,
            'title': self.title,
            'content': self.content,
            'created_date': self.created_date
        }
        if self.img_id:
            post_data['img_id'] = self.img_id
        db.blog_collection.insert_one(post_data)

    def json(self):
        return {
            '_id': self._id,
            'username': self.username,
            'title': self.title,
            'content': self.content,
            'img_id': self.img_id,
            'created_date': self.created_date
        }
    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data['username'],
            title=data['title'],
            content=data['content'],
            img_id=data.get('img_id'),
            created_date=data['created_date'],
            _id=data.get('_id')
        )

    def save_image(self, file):
        # Save the uploaded image to GridFS
        self.img_id = fs.put(file, filename=file.filename)

    def get_image_data(self):
        # Retrieve the image data from GridFS
        if self.img_id:
            print(self.img_id)
            image = fs.get(self.img_id)
            base64_data = codecs.encode(image.read(), 'base64')
            return base64_data.decode('utf-8')


class Enquiry():
    def __init__(self,  name, email, phone, message, created_date=datetime.utcnow().strftime("%d %B %Y %H:%M:%S"), _id=None):
        self.name = name
        self.email = email
        self.phone = phone
        self.message = message
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            '_id': self._id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'message': self.message,
            'created_date': self.created_date
        }
