# -*- coding: utf-8 -*-
"""
End-to-end tests for Student's Profile Page.
"""


# from contextlib import contextmanager
from datetime import datetime

# import six

from common.test.acceptance.pages.common.auto_auth import AutoAuthPage
from common.test.acceptance.pages.common.logout import LogoutPage
# from common.test.acceptance.pages.lms.account_settings import AccountSettingsPage
from common.test.acceptance.pages.lms.learner_profile import LearnerProfilePage
from common.test.acceptance.tests.helpers import AcceptanceTest, EventsTestMixin


class LearnerProfileTestMixin(EventsTestMixin):
    """
    Mixin with helper methods for testing learner profile pages.
    """

    PRIVACY_PUBLIC = u'all_users'
    PRIVACY_PRIVATE = u'private'

    PUBLIC_PROFILE_FIELDS = ['username', 'country', 'language_proficiencies', 'bio']
    PRIVATE_PROFILE_FIELDS = ['username']

    PUBLIC_PROFILE_EDITABLE_FIELDS = ['country', 'language_proficiencies', 'bio']

    USER_SETTINGS_CHANGED_EVENT_NAME = u"edx.user.settings.changed"

    def log_in_as_unique_user(self):
        """
        Create a unique user and return the account's username and id.
        """
        username = "test_{uuid}".format(uuid=self.unique_id[0:6])
        auto_auth_page = AutoAuthPage(self.browser, username=username).visit()
        user_id = auto_auth_page.get_user_id()
        return username, user_id

    def set_public_profile_fields_data(self, profile_page):
        """
        Fill in the public profile fields of a user.
        """
        # These value_for_dropdown_field method calls used to include
        # focus_out = True, but a change in selenium is focusing out of the
        # drop down after selection without any more action needed.
        profile_page.value_for_dropdown_field('language_proficiencies', 'English')
        profile_page.value_for_dropdown_field('country', 'United Arab Emirates')
        profile_page.set_value_for_textarea_field('bio', 'Nothing Special')
        # Waits here for text to appear/save on bio field
        profile_page.wait_for_ajax()

    def visit_profile_page(self, username, privacy=None):
        """
        Visit a user's profile page and if a privacy is specified and
        is different from the displayed value, then set the privacy to that value.
        """
        profile_page = LearnerProfilePage(self.browser, username)

        # Change the privacy if requested by loading the page and
        # changing the drop down
        if privacy is not None:
            profile_page.visit()

            # Change the privacy setting if it is not the desired one already
            profile_page.privacy = privacy

            # Verify the current setting is as expected
            if privacy == self.PRIVACY_PUBLIC:
                self.assertEqual(profile_page.privacy, 'all_users')
            else:
                self.assertEqual(profile_page.privacy, 'private')

            if privacy == self.PRIVACY_PUBLIC:
                self.set_public_profile_fields_data(profile_page)

        # Reset event tracking so that the tests only see events from
        # loading the profile page.
        self.start_time = datetime.now()

        # Load the page
        profile_page.visit()

        return profile_page

    # def set_birth_year(self, birth_year):
    #     """
    #     Set birth year for the current user to the specified value.
    #     """
    #     account_settings_page = AccountSettingsPage(self.browser)
    #     account_settings_page.visit()
    #     account_settings_page.wait_for_page()
    #     self.assertEqual(
    #         account_settings_page.value_for_dropdown_field('year_of_birth', str(birth_year), focus_out=True),
    #         str(birth_year)
    #     )
    #
    # def verify_profile_page_is_public(self, profile_page, is_editable=True):
    #     """
    #     Verify that the profile page is currently public.
    #     """
    #     self.assertEqual(profile_page.visible_fields, self.PUBLIC_PROFILE_FIELDS)
    #     if is_editable:
    #         self.assertTrue(profile_page.privacy_field_visible)
    #         self.assertEqual(profile_page.editable_fields, self.PUBLIC_PROFILE_EDITABLE_FIELDS)
    #     else:
    #         self.assertEqual(profile_page.editable_fields, [])
    #
    # def verify_profile_page_is_private(self, profile_page, is_editable=True):
    #     """
    #     Verify that the profile page is currently private.
    #     """
    #     if is_editable:
    #         self.assertTrue(profile_page.privacy_field_visible)
    #     self.assertEqual(profile_page.visible_fields, self.PRIVATE_PROFILE_FIELDS)
    #
    # def verify_profile_page_view_event(self, requesting_username, profile_user_id, visibility=None):
    #     """
    #     Verifies that the correct view event was captured for the profile page.
    #     """
    #
    #     actual_events = self.wait_for_events(
    #         start_time=self.start_time,
    #         event_filter={'event_type': 'edx.user.settings.viewed', 'username': requesting_username},
    #         number_of_matches=1)
    #     self.assert_events_match(
    #         [
    #             {
    #                 'username': requesting_username,
    #                 'event': {
    #                     'user_id': int(profile_user_id),
    #                     'page': 'profile',
    #                     'visibility': six.text_type(visibility)
    #                 }
    #             }
    #         ],
    #         actual_events
    #     )
    #
    # @contextmanager
    # def verify_pref_change_event_during(self, username, user_id, setting, **kwargs):
    #     """Assert that a single setting changed event is emitted for the user_api_userpreference table."""
    #     expected_event = {
    #         'username': username,
    #         'event': {
    #             'setting': setting,
    #             'user_id': int(user_id),
    #             'table': 'user_api_userpreference',
    #             'truncated': []
    #         }
    #     }
    #     expected_event['event'].update(kwargs)
    #
    #     event_filter = {
    #         'event_type': self.USER_SETTINGS_CHANGED_EVENT_NAME,
    #         'username': username,
    #     }
    #     with self.assert_events_match_during(event_filter=event_filter, expected_events=[expected_event]):
    #         yield

    def initialize_different_user(self, privacy=None, birth_year=None):
        """
        Initialize the profile page for a different test user
        """
        username, user_id = self.log_in_as_unique_user()

        # Set the privacy for the new user
        if privacy is None:
            privacy = self.PRIVACY_PUBLIC
        self.visit_profile_page(username, privacy=privacy)

        # Set the user's year of birth
        if birth_year:
            self.set_birth_year(birth_year)

        # Log the user out
        LogoutPage(self.browser).visit()

        return username, user_id


class LearnerProfileA11yTest(LearnerProfileTestMixin, AcceptanceTest):
    """
    Class to test learner profile accessibility.
    """
    a11y = True

    def test_editable_learner_profile_a11y(self):
        """
        Test the accessibility of the editable version of the profile page
        (user viewing her own public profile).
        """
        username, _ = self.log_in_as_unique_user()

        profile_page = self.visit_profile_page(username)
        profile_page.a11y_audit.config.set_rules({
            "ignore": [
                'aria-valid-attr',  # TODO: LEARNER-6611 & LEARNER-6865
                'region',  # TODO: AC-932
            ]
        })
        profile_page.a11y_audit.check_for_accessibility_errors()

        profile_page.make_field_editable('language_proficiencies')
        profile_page.a11y_audit.check_for_accessibility_errors()

        profile_page.make_field_editable('bio')
        profile_page.a11y_audit.check_for_accessibility_errors()

    def test_read_only_learner_profile_a11y(self):
        """
        Test the accessibility of the read-only version of a public profile page
        (user viewing someone else's profile page).
        """
        # initialize_different_user should cause country, language, and bio to be filled out (since
        # privacy is public). It doesn't appear that this is happening, although the method
        # works in regular bokchoy tests. Perhaps a problem with phantomjs? So this test is currently
        # only looking at a read-only profile page with a username.
        different_username, _ = self.initialize_different_user(privacy=self.PRIVACY_PUBLIC)
        self.log_in_as_unique_user()

        profile_page = self.visit_profile_page(different_username)
        profile_page.a11y_audit.config.set_rules({
            "ignore": [
                'aria-valid-attr',  # TODO: LEARNER-6611 & LEARNER-6865
                'region',  # TODO: AC-932
            ]
        })
        profile_page.a11y_audit.check_for_accessibility_errors()

    def test_badges_accessibility(self):
        """
        Test the accessibility of the badge listings and sharing modal.
        """
        username = 'testcert'

        AutoAuthPage(self.browser, username=username).visit()
        profile_page = self.visit_profile_page(username)
        profile_page.a11y_audit.config.set_rules({
            "ignore": [
                'aria-valid-attr',  # TODO: LEARNER-6611 & LEARNER-6865
                'region',  # TODO: AC-932
                'color-contrast'  # AC-938
            ]
        })
        profile_page.display_accomplishments()
        profile_page.a11y_audit.check_for_accessibility_errors()
        profile_page.badges[0].display_modal()
        profile_page.a11y_audit.check_for_accessibility_errors()
