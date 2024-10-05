from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'  # Folder untuk menyimpan file PDF
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Pastikan folder upload ada
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Daftar buku yang akan disimpan
books = []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        file = request.files['file']

        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            books.append({'title': title, 'author': author, 'filename': filename, 'borrowed': False})
            return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/borrow_book', methods=['GET', 'POST'])
def borrow_book():
    if request.method == 'POST':
        book_title = request.form['book_title']
        borrower_name = request.form['borrower_name']

        for book in books:
            if book['title'] == book_title and not book['borrowed']:
                book['borrowed'] = True
                book['borrower_name'] = borrower_name
                break
        return redirect(url_for('index'))
    
    return render_template('borrow_book.html', books=books)

@app.route('/return_book', methods=['GET', 'POST'])
def return_book():
    if request.method == 'POST':
        book_title = request.form['book_title']

        for book in books:
            if book['title'] == book_title and book['borrowed']:
                book['borrowed'] = False
                book.pop('borrower_name', None)
                break
        return redirect(url_for('index'))

    return render_template('return_book.html', books=books)

@app.route('/view_borrowers')
def view_borrowers():
    borrowers = [{'name': book['borrower_name'], 'book': book['title']} for book in books if book.get('borrowed')]
    return render_template('view_borrowers.html', borrowers=borrowers)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
