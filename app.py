from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import pdb
import csv
from shapely.wkt import loads
from sqlalchemy.orm import sessionmaker



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.debug = True

@app.errorhandler(Exception)
def handle_exception(e):
    pdb.post_mortem()
    # Additional error handling if needed



def load_csv_into_dict(filename):
    result = []
    
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            result.append(dict(row))
    
    return result


class Citation(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    citation_number = db.Column(db.String(255))
    citation_issued_datetime = db.Column(db.DateTime)
    violation = db.Column(db.String(255))
    violation_desc = db.Column(db.String(255))
    citation_location = db.Column(db.String(255))
    vehicle_plate_state = db.Column(db.String(255))
    vehicle_plate = db.Column(db.String(255))
    fine_amount = db.Column(db.Integer)
    date_added = db.Column(db.DateTime)
    type_of_citation = db.Column(db.String(255))
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    computed_region_jwn9_ihcz = db.Column(db.String(255))
    computed_region_6qbp_sg9q = db.Column(db.String(255))
    computed_region_qgnn_b9vv = db.Column(db.String(255))
    computed_region_26cr_cadq = db.Column(db.String(255))
    computed_region_ajp5_b2md = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return "Citation(id={}, citation_number={})".format(self.id, self.citation_number)


    @classmethod
    def seed_citations(self, filename):     
        data = load_csv_into_dict(filename)     
        for citation in data:
            coordinates_str = citation['geom']
            if coordinates_str:
                # Parse the WKT representation into a geometry object
                geometry = loads(coordinates_str)
                # Extract the latitude and longitude values
                calculated_latitude = geometry.x
                calculated_longitude = geometry.y
            else:                
                calculated_latitude = 0
                calculated_longitude = 0

            calculated_citation_issued_datetime = datetime.strptime(citation['Citation Issued DateTime'], "%m/%d/%Y %I:%M:%S %p")
            calculated_date_added = datetime.strptime(citation['Date Added'], "%m/%d/%Y %I:%M:%S %p")            
            new_citation = Citation(
                citation_number=citation['Citation Number'],
                citation_issued_datetime=calculated_citation_issued_datetime,
                violation=citation['Violation'],
                violation_desc=citation['Violation Description'],
                citation_location=citation['Citation Location'],
                vehicle_plate_state=citation['Vehicle Plate State'],
                vehicle_plate=citation['Vehicle Plate'],
                fine_amount=citation['Fine Amount'],
                date_added=calculated_date_added,
                latitude=calculated_latitude,
                longitude=calculated_longitude,
                computed_region_jwn9_ihcz=citation['Neighborhoods'],
                computed_region_6qbp_sg9q=citation['SF Find Neighborhoods'],
                computed_region_qgnn_b9vv=citation['Current Police Districts'],
                computed_region_26cr_cadq=citation['Current Supervisor Districts'],
                computed_region_ajp5_b2md=citation['Analysis Neighborhoods'],                
            )
            db.session.add(new_citation)
            db.session.commit()

        
        

@app.route('/', methods=['GET', 'POST'])

def index():
    return "hello"

if __name__ == "__main__":
    app.run(debug=True)