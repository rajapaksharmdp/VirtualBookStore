import json
from flask import Flask, jsonify, request

# Initialize Flask app
app = Flask(__name__)

books_file = 'Storage/books.json'


def load_books_from_file():
    with open(books_file) as f:
        books_data = json.load(f)
    return books_data


def save_books_to_file(books_data):
    try:
        with open(books_file, 'w') as f:
            json.dump(books_data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        book_data = request.json
        books_data = load_books_from_file()

        existing_id = [book['id'] for book in books_data]
        if book_data['id'] in existing_id:
            return jsonify({'error': 'Book already exists'}), 400

        # Add the new book to the list
        books_data.append(book_data)

        # Save the updated book data to the file
        if save_books_to_file(books_data):
            return jsonify({'message': 'Book added successfully'}), 201
        else:
            return jsonify({'error': 'Failed to save book data'}), 500

    except Exception as e:
        return jsonify({'error': 'Failed to add book', 'details': str(e)}), 500


@app.route('/update_book/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    try:
        book_data = request.json
        books_data = load_books_from_file()

        # Find the book with the given ID
        for book in books_data:
            if book['id'] == book_id:
                # Update the book information
                book.update(book_data)

                # Save the updated book data to the file
                if save_books_to_file(books_data):
                    return jsonify({'message': 'Book updated successfully'}), 200
                else:
                    return jsonify({'error': 'Failed to save book data'}), 500

        return jsonify({'error': 'Book not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Failed to update book', 'details': str(e)}), 500


@app.route('/delete_book/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    try:
        books_data = load_books_from_file()

        # Find the book with the given ID and remove it
        for book in books_data:
            if book['id'] == book_id:
                books_data.remove(book)

                # Save the updated book data to the file
                if save_books_to_file(books_data):
                    return jsonify({'message': 'Book deleted successfully'}), 200
                else:
                    return jsonify({'error': 'Failed to save book data'}), 500

        return jsonify({'error': 'Book not found'}), 404

    except Exception as e:
        return jsonify({'error': 'Failed to delete book', 'details': str(e)}), 500


@app.route('/', methods=['GET'])
def get_books():
    books_data = load_books_from_file()
    return jsonify(books_data)


# Run the Flask app on localhost with port 8080
if __name__ == '__main__':
    app.run(port=8080)


