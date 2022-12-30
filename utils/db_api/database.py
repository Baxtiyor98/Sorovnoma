from gino import Gino
from data.config import DB_HOST, DB_NAME, DB_PASS, DB_USER

db = Gino()


class Partners(db.Model):
    __tablename__ = 'partners'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.String)
    partner = db.Column(db.String)
    number = db.Column(db.Integer, default=0)


class User(db.Model):
    __tablename__ = 'user_likes'

    id = db.Column(db.Integer, primary_key=True)
    partner = db.Column(db.String)
    user_id = db.Column(db.String)


class DBcommands():

    async def create_partner(self, post_id, partner):
        partner = await Partners.create(post_id=str(post_id), partner=str(partner))
        return partner

    async def new_user_like(self, partner, user_id):
        print(await self.get_user(partner, user_id))
        if not await self.get_user(partner, user_id):
            await User.create(partner=str(partner), user_id=str(user_id))
            return True
        return False

    async def get_user(self, partner, user_id):
        user = await User.query.where(User.partner == str(partner)).where(User.user_id == str(user_id)).gino.first()
        if user:
            return True
        else:
            return False

    async def get_partners(self, post_id):
        partners = await Partners.query.where(Partners.post_id == str(post_id)).gino.all()
        return partners

    async def like_caunt(self, partner):
        likes = await User.query.where(User.partner == str(partner)).gino.all()
        return len(likes)


async def create_db():
    # await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    await db.set_bind(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}")
    await db.gino.create_all()
    # await db.gino.drop_all()
