#!/usr/bin/python3
"""Review objects view for Airbnb Clone"""

from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review


@app_views.route(
                    '/places/<place_id>/reviews',
                    methods=['GET'],
                    strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route(
                    '/reviews/<review_id>',
                    methods=['GET'],
                    strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
                    '/reviews/<review_id>',
                    methods=['DELETE'],
                    strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route(
                    '/places/<place_id>/reviews',
                    methods=['POST'],
                    strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    user_id = data.get("user_id")
    text = data.get("text")
    if not user_id:
        abort(400, "Missing user_id")
    if not text:
        abort(400, "Missing text")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    new_review = Review(**data)
    new_review.place_id = place_id
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route(
                    '/reviews/<review_id>',
                    methods=['PUT'],
                    strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in [
                        "id", "user_id", "place_id",
                        "created_at", "updated_at"]:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
