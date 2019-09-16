class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True, nullable = False)
    password = db.Column(db.String(120), nullable = False)
    isVerified = db.Column(db.Boolean,  nullable=False, default=False)
    email = db.Column(db.String(120), unique = True, nullable = False)
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email = email).first()

    @classmethod
    def find_by_username(cls, username):
        print(cls)
        print(username)
        return cls.query.filter_by(username = username).first()
    
    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    username = fields.String(required=True)
    email = fields.String(required=True)