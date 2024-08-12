from flask import Flask, render_template, redirect, jsonify, request
from application import PDFinder

app = Flask(__name__, template_folder='templates')

@app.route('/')
async def HomePage():
    return render_template('index.html')

@app.route('/search/', methods=['POST', 'GET'])
async def SearchPDF():
    if request.method == "POST":
        query = request.json['query']
        count = request.json['count']
        if int(count) <= 0 or len(query) <= 2:
            return jsonify({
                "Sukses": False, "Message": "Jumlah harus lebih dari 0 dan pertanyaan minimal 3 karakter"
            }), 400
        else:
            try:
                PDF = await PDFinder.pdFINDER(pertanyaan=query, count=count)
                return (PDF)
            except (Exception) as e:
                return jsonify({
                    "Sukses": False, "Message": f"{str(e)}"
                }), 500
    else:
        return redirect('/')

if __name__=='__main__':
    app.run(debug=True)