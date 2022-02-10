from website import create_app
from flask import Flask, jsonify, request
app = create_app()


if __name__ == '__main__':

    app.run(debug=True)