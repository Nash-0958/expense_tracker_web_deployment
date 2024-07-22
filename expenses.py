from flask import Flask, render_template, request, redirect, url_for, send_file
import pandas as pd
import datetime

app = Flask(__name__)

entries = []
total_debited = 0
total_credited = 0

@app.route('/', methods=['GET', 'POST'])
def index():
    global total_debited, total_credited
    if request.method == 'POST':
        type = request.form.get('type')
        amount = request.form.get('amount')
        category = request.form.get('category')
        date = request.form.get('date')

        if not amount or not category or not date:
            return redirect(url_for('index'))

        try:
            amount = float(amount)
        except ValueError:
            return redirect(url_for('index'))

        if type == 'debit':
            total_debited += amount
        else:
            total_credited += amount

        entries.append({"Type": type, "Amount": amount, "Category": category, "Date": date})
        return redirect(url_for('index'))

    return render_template('index.html', entries=entries, total_debited=total_debited, total_credited=total_credited, now=datetime.datetime.now().strftime("%Y-%m-%d"))

@app.route('/export_csv')
def export_csv():
    df = pd.DataFrame(entries)
    df.to_csv('expenses.csv', index=False)
    return send_file('expenses.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
