from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
from templates.land_registry import LandRegistry

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Initialize land registry
land_registry = LandRegistry()

@app.route('/')
def index():
    """Main dashboard"""
    stats = land_registry.get_blockchain_stats()
    recent_lands = land_registry.get_all_lands()[-5:]  # Get last 5 lands
    return render_template('index.html', stats=stats, recent_lands=recent_lands)

@app.route('/register', methods=['GET', 'POST'])
def register_land():
    """Register new land"""
    if request.method == 'POST':
        try:
            land_id = request.form['land_id']
            owner_name = request.form['owner_name']
            owner_address = request.form['owner_address']
            
            land_details = {
                'area': request.form['area'],
                'location': request.form['location'],
                'land_type': request.form['land_type'],
                'survey_number': request.form['survey_number'],
                'description': request.form.get('description', '')
            }
            
            result = land_registry.register_land(land_id, owner_name, owner_address, land_details)
            
            if result['success']:
                flash(result['message'], 'success')
                return redirect(url_for('view_land', land_id=land_id))
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f'Error registering land: {str(e)}', 'error')
    
    return render_template('register_land.html')

@app.route('/transfer', methods=['GET', 'POST'])
def transfer_land():
    """Transfer land ownership"""
    if request.method == 'POST':
        try:
            land_id = request.form['land_id']
            from_owner = request.form['from_owner']
            to_owner = request.form['to_owner']
            to_owner_name = request.form['to_owner_name']
            
            transfer_details = {
                'transfer_reason': request.form['transfer_reason'],
                'transfer_amount': request.form.get('transfer_amount', ''),
                'notes': request.form.get('notes', '')
            }
            
            result = land_registry.transfer_land(land_id, from_owner, to_owner, to_owner_name, transfer_details)
            
            if result['success']:
                flash(result['message'], 'success')
                return redirect(url_for('view_land', land_id=land_id))
            else:
                flash(result['message'], 'error')
                
        except Exception as e:
            flash(f'Error transferring land: {str(e)}', 'error')
    
    return render_template('transfer_land.html')

@app.route('/lands')
def view_all_lands():
    """View all registered lands"""
    lands = land_registry.get_all_lands()
    return render_template('view_records.html', lands=lands)

@app.route('/land/<land_id>')
def view_land(land_id):
    """View specific land details"""
    land_info = land_registry.get_land_info(land_id)
    return render_template('land_details.html', land_info=land_info)

@app.route('/api/land/<land_id>')
def api_get_land(land_id):
    """API endpoint to get land information"""
    return jsonify(land_registry.get_land_info(land_id))

@app.route('/api/lands')
def api_get_all_lands():
    """API endpoint to get all lands"""
    return jsonify(land_registry.get_all_lands())

@app.route('/api/stats')
def api_get_stats():
    """API endpoint to get blockchain statistics"""
    return jsonify(land_registry.get_blockchain_stats())

@app.route('/api/verify')
def api_verify_blockchain():
    """API endpoint to verify blockchain integrity"""
    is_valid = land_registry.verify_blockchain_integrity()
    return jsonify({
        'valid': is_valid,
        'message': 'Blockchain is valid' if is_valid else 'Blockchain integrity compromised'
    })

@app.route('/blockchain')
def view_blockchain():
    """View blockchain details"""
    stats = land_registry.get_blockchain_stats()
    all_transactions = land_registry.blockchain.get_all_transactions()
    return render_template('blockchain.html', stats=stats, transactions=all_transactions)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Create templates and static directories if they don't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
