""" Main app """
from flask import Flask, jsonify, request
from src.domain.use_case.GetAllArtistsUseCase import GetAllArtistsUseCase

from src.domain.use_case.GetArtistUseCase import GetArtistUseCase
from src.domain.use_case.GetRecommendationUseCase import GetRecommendationUseCase

app = Flask(__name__)

@app.route('/health')
def get_health():
    """ Returns message to perform a system health check"""
    return "OK"

@app.route('/artist/<artist_id>')
def get_artist(artist_id):
    """ Returns a single artist's profile """
    description = request.args.get('description')

    use_case = GetArtistUseCase()

    response = use_case.execute(artist_id, description)

    if response:
        return jsonify(response)

    return jsonify({}), 404


@app.route('/artists')
def get_all_artists():
    """ Returns all artists names and ids """
    use_case = GetAllArtistsUseCase()

    response = use_case.execute()

    if response:
        return jsonify(response)

    return jsonify([]), 404

@app.route('/recommendations/<artist_id>')
def get_recommendation(artist_id):
    """ Returns similar artists as recommendation for the given artist """

    use_case = GetRecommendationUseCase()

    response = use_case.execute(artist_id)

    if response:
        return jsonify(response)

    return jsonify([]), 404


print("Starting Recommendation Service")
print("----------------------------------------------------")
