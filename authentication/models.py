from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_customer(self, name, surname, email, password):
        if name is None:
            raise TypeError('Users must have a name.')

        if surname is None:
            raise TypeError('Users must have a surname.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(name=name, surname=surname, email=self.normalize_email(email), is_staff=False,
                          is_superuser=False)
        user.set_password(password)
        user.save()

        return user

    def create_worker(self, name, surname, shop, email, password):
        if name is None:
            raise TypeError('Worker must have a name.')

        if surname is None:
            raise TypeError('Worker must have a surname.')

        if shop is None:
            raise TypeError('Worker must have a shop.')

        if email is None:
            raise TypeError('Users must have an email address.')

        user = self.model(name=name, surname=surname, email=self.normalize_email(email), shop_id=shop, is_staff=True,
                          is_superuser=False)
        user.set_password(password)
        user.save()

        return user

    def create_administrator(self, name, surname, email, shop, password):
        if name is None:
            raise TypeError('Administrator must have a name.')

        if surname is None:
            raise TypeError('Administrator must have a surname.')

        if email is None:
            raise TypeError('Administrator must have an email address.')

        if shop is None:
            raise TypeError('Administrator must have a shop.')

        user = self.model(name=name, surname=surname, email=self.normalize_email(email), shop_id=shop, is_staff=True,
                          is_superuser=True)
        user.set_password(password)
        user.user_permissions = ['auth.add_worker']
        user.save()

        return user
