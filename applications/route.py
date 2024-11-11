from main import app 
from flask import render_template,request,session,url_for,redirect,flash
from flask import session
from applications.model import *

@app.route('/')
def home():
    if 'email' not in session: 
        return redirect(url_for('youlog'))
    return render_template('dash.html')

@app.route('/youlog')
def youlog():
    return render_template('youlog.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        if not email:
            flash('Email is required')
            return redirect(url_for('login'))
        if not password:
            flash('Password is required')
            return redirect(url_for('login'))
        
        u = User.query.filter_by(email=email).first()  
        if not u:
            flash('Invalid email')
            return redirect(url_for('login'))
        
        if u.password == password:  
            session['email'] = email 
            flash('Logged in successfully')
            return redirect(url_for('home'))  
        else:
            flash('Invalid password')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None) 
    print("session after logout", session)  
    return redirect(url_for('home'))  

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)

        if not email:
            flash('Email is required')
            return redirect(url_for('register'))
        if not password:
            flash('Password is required')
            return redirect(url_for('register'))
        
        new_user = User(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully')
        return redirect(url_for('login'))  
    
@app.route('/dash')
def dash():
    return render_template('dash.html')



@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'email' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        # Validate form fields
        if not title:
            flash('Title is required')
        if not content:
            flash('Content is required')

        if not title or not content:
            flash('All fields are required')
            return redirect(url_for('add'))
        
        # Get the user from the session email
        user = User.query.filter_by(email=session['email']).first()
        
        # Create and save the journal entry with the user's ID
        addd = Journal(title=title, content=content, user_id=user.id)
        
        try:
            db.session.add(addd)
            db.session.commit()
            flash('Journal added successfully')
            return redirect(url_for('dash'))
        except Exception as e:
            db.session.rollback()
            flash(f'An error occurred: {str(e)}')
        
        return redirect(url_for('add'))
    
    return render_template('add.html')



@app.route('/view')
def view():
    if 'email' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    
    user = User.query.filter_by(email=session['email']).first()
    if user is None:
        flash("User not found. Please log in again.")
        return redirect(url_for('login'))
    
    journals = Journal.query.filter_by(user_id=user.id).all()
    return render_template('view.html', journals=journals)





@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if 'email' not in session:
        flash("Please log in first.")
        return redirect(url_for('login'))
    
    journal = Journal.query.get_or_404(id)
    
    # Check if the logged-in user is the owner of the journal
    if journal.user_email != session['email']:
        flash("You do not have permission to delete this journal.")
        return redirect(url_for('view'))

    try:
        db.session.delete(journal)
        db.session.commit()
        flash("Journal deleted successfully")
    except Exception as e:
        db.session.rollback()
        flash(f"An error occurred: {str(e)}")
    
    return redirect(url_for('view'))
