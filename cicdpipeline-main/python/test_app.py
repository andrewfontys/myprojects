import unittest
from flask import Flask, g
from flask_testing import TestCase
from app import app, db, Product

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()
        self.populate_test_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def populate_test_data(self):
        # Add some test data to the database
        product1 = Product(name='TestProduct1', price=10.99, category='TestCategory1')
        product2 = Product(name='TestProduct2', price=20.99, category='TestCategory2')

        db.session.add_all([product1, product2])
        db.session.commit()

    def test_get_products(self):
        response = self.client.get('/product')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)  # Assuming you added two products in the test data

    def test_get_product_by_id(self):
        product_id = 1  # Assuming this product exists in the test data
        response = self.client.get(f'/product/{product_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], product_id)

    def test_add_product(self):
        new_product_data = {'name': 'NewTestProduct', 'price': 15.99, 'category': 'NewTestCategory'}
        response = self.client.post('/product/add', json=new_product_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'the product has been added ')

        # Check if the product is added to the database
        new_product = Product.query.filter_by(name='NewTestProduct').first()
        self.assertIsNotNone(new_product)

    def test_delete_product(self):
        product_id_to_delete = 1  # Assuming this product exists in the test data
        response = self.client.post(f'/product/delete/{product_id_to_delete}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['message'], 'the product has been deleted')

        # Check if the product is deleted from the database
        deleted_product = Product.query.get(product_id_to_delete)
        self.assertIsNone(deleted_product)

if __name__ == '__main__':
    unittest.main()
