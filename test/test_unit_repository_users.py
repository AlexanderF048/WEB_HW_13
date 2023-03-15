import unittest
from unittest.mock import patch, MagicMock, Mock, create_autospec

from sqlalchemy.orm import Session

from src.database.db_models import User, ContactPerson
from src.valid_schemas import UserModel

from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar,
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    def tearDown(self):
        del self.session
        del self.user

    async def test_get_user_by_email(self):
        email = 'test@mail.box'
        test_entity = ContactPerson(email=email)
        self.session.query().filter().first.return_value = test_entity
        result = await get_user_by_email(email=email, db=self.session)
        self.assertEqual(result, test_entity)

    async def test_create_user(self):
        body = UserModel(
            username='Albert',
            email='test@mail.box',
            password='XXXXXX'
        )

        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.password, body.password)
        self.assertEqual(result.email, body.email)

    async def test_update_token(self):
        token = 'TOKEN'
        result = await update_token(user=self.user, token=token, db=self.session)
        self.assertEqual(token, self.user.refresh_token)


    async def test_confirmed_email(self):
        #mock_function = create_autospec(get_user_by_email, return_value=self.user)
        email = 'test@mail.box'

        result = await confirmed_email(email=email, db=self.session)
        self.assertTrue(self.user.confirmed)




if __name__ == '__main__':
    unittest.main()
