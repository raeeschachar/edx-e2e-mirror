"""
Tests for new users using Otto
"""
import uuid

from regression.pages.common.utils import get_target_url_from_text
from regression.pages.whitelabel.const import GMAIL_USER
from regression.pages.whitelabel.home_page import HomePage
from regression.pages.whitelabel.inactive_account import InactiveAccount
from regression.pages.whitelabel.reset_password_page import (
    ResetPassword,
    ResetPasswordComplete
)
from regression.tests.helpers.user_authentication import (
    UserAuthenticationMixin
)


class TestUSerAccount(UserAuthenticationMixin):
    """
    User Accounts Tests
    """

    def setUp(self):
        """
        Initialize all page objects
        """
        super(TestUSerAccount, self).setUp()
        self.home = HomePage(self.browser)
        self.inactive_account = InactiveAccount(self.browser)

    def test_00_activate_account_and_reset_password(self):
        """
        Scenario: A user is able to activate his account
        """
        # Go to registration page and register for the course
        self.home.visit()
        self.home.go_to_registration_page()
        self.register_user(self.dashboard)
        # Check that activation message is appearing on dashboard
        self.assertTrue(self.dashboard.check_activation_message())
        self.account_activation()
        # Check that activation message is no more appearing on dashboard
        self.assertFalse(self.dashboard.check_activation_message())
        # Logout
        self.logout_user_from_lms()

    def test_01_reset_password(self):
        """
        Scenario: A user is able to reset the password
        """
        reset_password_user_email = GMAIL_USER.format("+passwordreset")
        new_password = str(uuid.uuid4().node)
        # Got to login page and use the forgot password functionality
        self.login_page.visit()
        self.login_page.send_forgot_password(reset_password_user_email)
        self.assertTrue(
            self.login_page.is_password_reset_email_message_visible()
        )
        email_text = self.mail_client.get_email_message(
            reset_password_user_email,
            'Password'
        )
        reset_password_url = get_target_url_from_text(
            'password_reset_confirm',
            email_text
        )
        self.reset_password = ResetPassword(self.browser, reset_password_url)
        self.reset_password.visit()
        self.reset_password.reset_password(new_password)
        self.reset_password_complete = ResetPasswordComplete(self.browser)
        self.reset_password_complete.go_to_login_page()
        self.login_page.authenticate_user(
            reset_password_user_email,
            new_password,
            self.dashboard
        )
        self.dashboard.is_browser_on_page()