from django.test import TestCase

from campaign.models import Campaign, Character, Faction, Item, Location
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.urls import reverse

GM_USER = 'gm'
PLAYER_USER = 'player'
NOT_PLAYER_USER = 'not_player'

TEST_PASSWORD = 'password'
TEST_USERS = [GM_USER, PLAYER_USER, NOT_PLAYER_USER]

TEST_CAMPAIGN = {
    'name': 'Public Campaign',
    'gm_id': TEST_USERS.index(GM_USER),
    'tagline': 'Test Tagline',
    'description': 'Test Description',
    'players': [TEST_USERS.index(PLAYER_USER)],
    'public': True,
}

TEST_CHARACTER = {
    'name': 'Test Character',
    'tagline': 'Test Tagline',
    'description': 'Test Description',
    'player': TEST_USERS.index(PLAYER_USER),
    'campaign_id': 1,
}

TEST_FACTION = {
    'name': 'Test Faction',
    'tagline': 'Test Tagline',
    'description': 'Test Description',
    'campaign_id': 1,
}

TEST_ITEM = {
    'name': 'Test Item',
    'tagline': 'Test Tagline',
    'description': 'Test Description',
    'campaign_id': 1,
}

TEST_LOCATION = {
    'name': 'Test Location',
    'tagline': 'Test Tagline',
    'description': 'Test Description',
    'campaign_id': 1,
}


class CharacterViewTest(TestCase):
    """ Test cases related to the Character view. """

    def setUp(self):
        # Create Users
        for idx, user in enumerate(TEST_USERS):
            User.objects.create_user(
                id=TEST_USERS.index(user),
                password=TEST_PASSWORD,
                username=user,
            )

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        # Create Campaigns
        response = self.client.post(reverse('campaign:campaign_entry'), TEST_CAMPAIGN)
        self.assertRedirects(response, reverse('campaign:campaign_index'))
        self.campaign = Campaign.objects.get(name = 'Public Campaign')

        # Create Characters
        response = self.client.post(reverse('campaign:character_entry', kwargs={'campaign_id': self.campaign.id}), TEST_CHARACTER)
        self.assertRedirects(response, reverse('campaign:character_list', kwargs={'campaign_id': self.campaign.id}))
        self.character = Character.objects.get(name = 'Test Character')

        # Logout
        self.client.logout()


    def test_invalid_character_entry(self):
        # Missing name
        bad_character_form = {
            'tagline': 'Test tagline.',
            'description': 'Test description',
            'player': TEST_USERS.index(PLAYER_USER),
            'campaign_id': 1,
        }

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:character_entry', kwargs={'campaign_id': self.campaign.id}), bad_character_form)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_invalid_edit_character(self):
        bad_character_form = {
            'tagline': 'Test tagline.',
            'description': 'Test description',
            'player': TEST_USERS.index(PLAYER_USER),
        }

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:character_edit', kwargs={'campaign_id': self.campaign.id, 'character_id': self.character.id}), bad_character_form)
        self.assertEqual(response.status_code, 200)

        character = Character.objects.get(id=self.character.id)

        self.assertEqual(character.tagline, 'New tagline!')

        self.client.logout()


    def test_gm_edit_character(self):
        new_character = TEST_CHARACTER
        new_character['tagline'] = 'New tagline!'

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:character_edit', kwargs={'campaign_id': self.campaign.id, 'character_id': self.character.id}), new_character)
        self.assertRedirects(response, reverse('campaign:character_detail', kwargs={'campaign_id': self.campaign.id, 'character_id': self.character.id}))

        character = Character.objects.get(id=self.character.id)

        self.assertEqual(character.tagline, 'New tagline!')

        self.client.logout()


    def test_player_edit_character(self):
        new_character = TEST_CHARACTER
        new_character['tagline'] = 'New tagline!'

        self.client.login(username=PLAYER_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:character_edit', kwargs={'campaign_id': self.campaign.id, 'character_id': self.character.id}), new_character)
        self.assertRedirects(response, reverse('campaign:character_detail', kwargs={'campaign_id': self.campaign.id, 'character_id': self.character.id}))

        character = Character.objects.get(id=self.character.id)

        self.assertEqual(character.tagline, 'New tagline!')

        self.client.logout()


    def test_not_player_edit_character(self):
        new_character = TEST_CHARACTER
        new_character['tagline'] = 'New tagline!'

        self.client.login(username=NOT_PLAYER_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:character_edit', kwargs={'campaign_id': self.campaign.id, 'character_id': self.character.id}), new_character)
        self.assertEqual(response.status_code, 403)

        self.client.logout()


class FactionViewTest(TestCase):
    """ Test cases related to the Faction view. """

    def setUp(self):
        # Create Users
        for idx, user in enumerate(TEST_USERS):
            User.objects.create_user(
                id=TEST_USERS.index(user),
                password=TEST_PASSWORD,
                username=user,
            )

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        # Create Campaigns
        response = self.client.post(reverse('campaign:campaign_entry'), TEST_CAMPAIGN)
        self.assertRedirects(response, reverse('campaign:campaign_index'))
        self.campaign = Campaign.objects.get(name = 'Public Campaign')

        # Create Factions
        response = self.client.post(reverse('campaign:faction_entry', kwargs={'campaign_id': self.campaign.id}), TEST_FACTION)
        self.assertRedirects(response, reverse('campaign:faction_list', kwargs={'campaign_id': self.campaign.id}))
        self.faction = Faction.objects.get(name = 'Test Faction')

        # Logout
        self.client.logout()


    def test_invalid_faction_entry(self):
        # Missing name
        bad_faction_form = {
            'tagline': 'Test tagline.',
            'description': 'Test description',
            'campaign_id': 1,
        }

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:faction_entry', kwargs={'campaign_id': self.campaign.id}), bad_faction_form)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_invalid_edit_faction(self):
        bad_faction_form = {
            'tagline': 'Test tagline.',
            'description': 'Test description',
        }

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:faction_edit', kwargs={'campaign_id': self.campaign.id, 'faction_id': self.faction.id}), bad_faction_form)
        self.assertEqual(response.status_code, 200)

        faction = Faction.objects.get(id=self.faction.id)

        self.assertEqual(faction.tagline, 'New tagline!')

        self.client.logout()


    def test_edit_faction(self):
        new_faction = TEST_FACTION
        new_faction['tagline'] = 'New tagline!'

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:faction_edit', kwargs={'campaign_id': self.campaign.id, 'faction_id': self.faction.id}), new_faction)
        self.assertRedirects(response, reverse('campaign:faction_detail', kwargs={'campaign_id': self.campaign.id, 'faction_id': self.faction.id}))

        faction = Faction.objects.get(id=self.faction.id)

        self.assertEqual(faction.tagline, 'New tagline!')

        self.client.logout()


class ItemViewTest(TestCase):
    """ Test cases related to the Item view. """

    def setUp(self):
        # Create Users
        for idx, user in enumerate(TEST_USERS):
            User.objects.create_user(
                id=TEST_USERS.index(user),
                password=TEST_PASSWORD,
                username=user,
            )

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        # Create Campaigns
        response = self.client.post(reverse('campaign:campaign_entry'), TEST_CAMPAIGN)
        self.assertRedirects(response, reverse('campaign:campaign_index'))
        self.campaign = Campaign.objects.get(name = 'Public Campaign')

        # Create Items
        response = self.client.post(reverse('campaign:item_entry', kwargs={'campaign_id': self.campaign.id}), TEST_ITEM)
        self.assertRedirects(response, reverse('campaign:item_list', kwargs={'campaign_id': self.campaign.id}))
        self.item = Item.objects.get(name = 'Test Item')

        # Logout
        self.client.logout()


    def test_invalid_item_entry(self):
        # Missing name
        bad_item_form = {
            'tagline': 'Test tagline.',
            'description': 'Test description',
            'campaign_id': 1,
        }

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:item_entry', kwargs={'campaign_id': self.campaign.id}), bad_item_form)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_invalid_edit_item(self):
        bad_item_form = {
            'tagline': 'Test tagline.',
            'description': 'Test description',
        }

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:item_edit', kwargs={'campaign_id': self.campaign.id, 'item_id': self.item.id}), bad_item_form)
        self.assertEqual(response.status_code, 200)

        item = Item.objects.get(id=self.item.id)

        self.assertEqual(item.tagline, 'New tagline!')

        self.client.logout()


    def test_edit_item(self):
        new_item = TEST_ITEM
        new_item['tagline'] = 'New tagline!'

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:item_edit', kwargs={'campaign_id': self.campaign.id, 'item_id': self.item.id}), new_item)
        self.assertRedirects(response, reverse('campaign:item_detail', kwargs={'campaign_id': self.campaign.id, 'item_id': self.item.id}))

        item = Item.objects.get(id=self.item.id)

        self.assertEqual(item.tagline, 'New tagline!')

        self.client.logout()


class LocationViewTest(TestCase):
    """ Test cases related to the Location view. """

    def setUp(self):
        # Create Users
        for idx, user in enumerate(TEST_USERS):
            User.objects.create_user(
                id=TEST_USERS.index(user),
                password=TEST_PASSWORD,
                username=user,
            )

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        # Create Campaigns
        response = self.client.post(reverse('campaign:campaign_entry'), TEST_CAMPAIGN)
        self.assertRedirects(response, reverse('campaign:campaign_index'))
        self.campaign = Campaign.objects.get(name = 'Public Campaign')

        # Create Locations
        response = self.client.post(reverse('campaign:location_entry', kwargs={'campaign_id': self.campaign.id}), TEST_LOCATION)
        self.assertRedirects(response, reverse('campaign:location_list', kwargs={'campaign_id': self.campaign.id}))
        self.location = Location.objects.get(name = 'Test Location')

        # Logout
        self.client.logout()


    def test_invalid_location_entry(self):
        # Missing name
        bad_location_form = {
            'tagline': 'Test tagline.',
            'description': 'Test description',
            'campaign_id': 1,
        }

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:location_entry', kwargs={'campaign_id': self.campaign.id}), bad_location_form)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

    def test_invalid_edit_location(self):
        bad_location_form = {
            'tagline': 'Test tagline.',
            'description': 'Test description',
        }

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:location_edit', kwargs={'campaign_id': self.campaign.id, 'location_id': self.location.id}), bad_location_form)
        self.assertEqual(response.status_code, 200)

        location = Location.objects.get(id=self.location.id)

        self.assertEqual(location.tagline, 'New tagline!')

        self.client.logout()


    def test_edit_location(self):
        new_location = TEST_LOCATION
        new_location['tagline'] = 'New tagline!'

        self.client.login(username=GM_USER, password=TEST_PASSWORD)

        response = self.client.post(reverse('campaign:location_edit', kwargs={'campaign_id': self.campaign.id, 'location_id': self.location.id}), new_location)
        self.assertRedirects(response, reverse('campaign:location_detail', kwargs={'campaign_id': self.campaign.id, 'location_id': self.location.id}))

        location = Location.objects.get(id=self.location.id)

        self.assertEqual(location.tagline, 'New tagline!')

        self.client.logout()
