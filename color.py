from flask import Flask, render_template, session, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import TextField, SubmitField
import matplotlib.colors as mcolors
from numpy import mean

app = Flask(__name__)

app.config['SECRET_KEY'] = 'choose_a_color_secret_key'

class ColorForm(FlaskForm):
    color = TextField('Color')
    submit = SubmitField('Change color')


@app.route('/')
def index():
    session['color'] = color = [255,255,255]
    return redirect(url_for('update_color'))
    #return render_template('color.html', form=form, style=style)

@app.route('/color', methods=['GET','POST'])
def update_color():
    form = ColorForm()

    if session['color']:
        color = session['color']
    else:
        color = (255,255,255)

    if form.validate_on_submit():
        form_input = form.color.data
        
        input_list = form_input.split()

        if len(input_list) > 1:
            direction = input_list[-2]
            new_col = input_list[-1]
        elif input_list[0] == 'lighter':
            direction = 'more'
            new_col = 'white'
        elif input_list[0] == 'darker':
            direction = 'more'
            new_col = 'black'
        else:
            direction = 'full'
            new_col = input_list[0]
        
        new_col = tuple(255*color for color in mcolors.to_rgb(new_col))

        if direction == 'full':
            color = new_col
        elif direction == 'less':
            color = tuple([max(min(1.1*color[i]-0.1*new_col[i],255),0) for i in range(3)])
        elif direction == 'more':
            color = tuple([min(0.9*color[i]+0.1*new_col[i],255) for i in range(3)])
 
    session['color'] = color
    style = f'background-color: rgb({color[0]},{color[1]},{color[2]}); width:100px; height:100px;'

    return render_template('color.html', form=form, style=style)


if __name__ == '__main__':
    app.run(debug=True)