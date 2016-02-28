#! /usr/bin/env python
# -*- coding: utf-8 -*-

from microbe.tests import MicrobeTestCase

from microbe.mods.content.models import Content, Category, Tag

__author__ = u'TROUVERIE Joachim'


class ContentTests(MicrobeTestCase):
    """Tests for Contents and Comments"""
    def setUp(self):
        super(ContentTests, self).setUp()
        with self.client.session_transaction() as session:
            session['user_id'] = self.user.id

    def test_add_content(self):
        self.client.post('/admin/content/', data=dict(
            title='Test',
            content_type='posts',
            category='Test',
            tags='Test,Test2',
            body='***Test***'
        ), follow_redirects=True)
        self.assertEquals(len(Content.query.all()), 1)
        self.assertEquals(len(Category.query.all()), 1)
        self.assertEquals(len(Tag.query.all()), 2)

    def test_upd_content(self):
        self.client.post('/admin/content/', data=dict(
            title='Test',
            content_type='posts',
            category='Test',
            tags='Test,Test2',
            body='***Test***'
        ), follow_redirects=True)
        content = Content.query.first()
        rv = self.client.post('/admin/content/' + str(content.id) + '/', data=dict(
            title='Test',
            content_type='posts',
            category='Test',
            tags='Test,Test3',
            body='***Test 3***'
        ), follow_redirects=True)
        content = Content.query.get(content.id)
        self.assertEquals(len(Content.query.all()), 1)
        self.assertEquals(len(Category.query.all()), 1)
        self.assertEquals(len(Tag.query.all()), 2)
        self.assertEquals(content.body, '***Test 3***')

    def test_del_content(self):
        self.client.post('/admin/content/', data=dict(
            title='Test',
            content_type='posts',
            category='Test',
            tags='Test,Test2',
            body='***Test***'
        ), follow_redirects=True)
        content = Content.query.first()
        self.client.post('/admin/delete_content/', data=dict(
            content=content.id
        ))
        resp = self.client.get('/admin/content/' + str(content.id) + '/',
                               follow_redirects=True)
        self.assertEquals(len(Content.query.all()), 0)
        resp = self.client.post('/admin/delete_content/', data=dict(
            content=2
        ), follow_redirects=True)
        self.assert404(resp)

    def test_comment(self):
        self.app.config['COMMENTS'] = 'YES'
        self.app.config['RECAPTCHA_PUBLIC_KEY'] = 'a' * 40
        self.app.config['RECAPTCHA_PRIVATE_KEY'] = 'b' * 40
        self.client.post('/admin/content/', data=dict(
            title='Test',
            content_type='posts',
            category='Test',
            tags='Test,Test2',
            body='***Test***'
        ), follow_redirects=True)
        # add comment
        content = Content.query.first()
        self.client.post('/' + str(content.id) + '/', data=dict(
            name='test',
            content='This is a comment',
            email='test@test.com',
            site='',
            notify=False,
            recaptcha_challenge_field='test',
            recaptcha_response_field='test'
        ), follow_redirects=True)
        self.assertEquals(len(content.comments.all()), 1)
        comment = content.comments.first()
        self.client.post('/admin/delete_comment/', data=dict(
            comment=comment.id
        ))
        self.assertEquals(len(content.comments.all()), 0)
