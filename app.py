from flask import Flask, render_template, request

app = Flask(__name__)

# Function to calculate weighted score
def calculate_weighted_score(total, obtained, weight):
    return (obtained / total) * weight

# Function to determine grade
def determine_grade(total_score):
    if total_score >= 90:
        return "A"
    elif 85 <= total_score < 90:
        return "A-"
    elif 80 <= total_score < 85:
        return "B+"
    elif 75 <= total_score < 80:
        return "B"
    elif 70 <= total_score < 75:
        return "B-"
    elif 65 <= total_score < 70:
        return "C+"
    elif 60 <= total_score < 65:
        return "C"
    elif 55 <= total_score < 60:
        return "C-"
    elif 50 <= total_score < 55:
        return "D"
    else:
        return "F"

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Grade calculation route
@app.route('/calculate', methods=['POST'])
def calculate_grade():
    if request.method == 'POST':
        total_score = 0
        total_weight = 0
        
        # Iterate over posted form data to calculate total score
        for key in request.form:
            if key.startswith('total_'):
                total = float(request.form[key])
                obtained = float(request.form[key.replace('total_', 'obtained_')])
                weight = float(request.form[key.replace('total_', 'weight_')])
                
                total_weight += weight
                total_score += calculate_weighted_score(total, obtained, weight)
        
        # Calculate final grade
        if total_weight != 0:
            final_grade = total_score / total_weight * 100
            grade = determine_grade(final_grade)
            return render_template('result.html', total_score=final_grade, grade=grade)
        else:
            error_message = "Please add activities to calculate the grade."
            return render_template('index.html', error=error_message)

if __name__ == '__main__':
    app.run(debug=True)
