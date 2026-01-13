"""
Kerala Colleges Data Population Script
Adds real Kerala colleges to MongoDB database
"""

from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB connection
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/career_counselling')
client = MongoClient(MONGODB_URI)
db = client.get_database()

# Kerala Colleges Data
kerala_colleges = [
    # Engineering Colleges
    {
        "name": "National Institute of Technology Calicut (NIT Calicut)",
        "short_name": "NITC",
        "location": "Calicut, Kerala",
        "district": "Kozhikode",
        "type": "Engineering",
        "affiliation": "Autonomous (Institute of National Importance)",
        "rating": 4.8,
        "established": 1961,
        "courses": ["B.Tech", "M.Tech", "MBA", "MCA", "PhD"],
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering",
            "Chemical Engineering"
        ],
        "fees_range": "₹1-2 Lakhs/year",
        "admission_criteria": "JEE Main",
        "placements": {
            "average": "₹15-18 LPA",
            "highest": "₹40+ LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Sports Complex", "WiFi Campus"],
        "accreditation": "NAAC A+",
        "website": "www.nitc.ac.in",
        "contact": "0495-2286100"
    },
    {
        "name": "College of Engineering Trivandrum (CET)",
        "short_name": "CET",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.5,
        "established": 1939,
        "courses": ["B.Tech", "M.Tech", "MBA", "MCA"],
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering",
            "Architecture"
        ],
        "fees_range": "₹50,000-1 Lakh/year",
        "admission_criteria": "KEAM (Kerala Engineering Entrance)",
        "placements": {
            "average": "₹6-8 LPA",
            "highest": "₹20+ LPA"
        },
        "facilities": ["Hostel", "Central Library", "Research Labs", "Sports", "Auditorium"],
        "accreditation": "NAAC A",
        "website": "www.cet.ac.in",
        "contact": "0471-2515565"
    },
    {
        "name": "Cochin University of Science and Technology (CUSAT)",
        "short_name": "CUSAT",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Engineering & Science",
        "affiliation": "State University",
        "rating": 4.4,
        "established": 1971,
        "courses": ["B.Tech", "M.Tech", "M.Sc", "MBA", "PhD"],
        "specializations": [
            "Computer Science",
            "Electronics",
            "Marine Sciences",
            "Biotechnology",
            "Management Studies"
        ],
        "fees_range": "₹40,000-80,000/year",
        "admission_criteria": "KEAM / CUSAT CAT",
        "placements": {
            "average": "₹5-7 LPA",
            "highest": "₹15+ LPA"
        },
        "facilities": ["Hostels", "Central Library", "Research Centers", "Marine Station"],
        "accreditation": "NAAC A+",
        "website": "www.cusat.ac.in",
        "contact": "0484-2577137"
    },
    {
        "name": "Government Engineering College Thrissur",
        "short_name": "GEC Thrissur",
        "location": "Thrissur, Kerala",
        "district": "Thrissur",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.3,
        "established": 1957,
        "courses": ["B.Tech", "M.Tech"],
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering"
        ],
        "fees_range": "₹30,000-60,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹5-6 LPA",
            "highest": "₹15 LPA"
        },
        "facilities": ["Hostel", "Library", "Computer Labs", "Sports Facilities"],
        "accreditation": "NAAC A",
        "website": "www.gectcr.ac.in",
        "contact": "0487-2333216"
    },
    {
        "name": "Government Engineering College Kannur",
        "short_name": "GEC Kannur",
        "location": "Kannur, Kerala",
        "district": "Kannur",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.2,
        "established": 1986,
        "courses": ["B.Tech", "M.Tech"],
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering"
        ],
        "fees_range": "₹30,000-60,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹12 LPA"
        },
        "facilities": ["Hostel", "Digital Library", "Labs", "Indoor Stadium"],
        "accreditation": "NAAC A",
        "website": "www.geck.ac.in",
        "contact": "0497-2700386"
    },

    # Medical Colleges
    {
        "name": "Government Medical College Thiruvananthapuram",
        "short_name": "MCT",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Medical",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.7,
        "established": 1951,
        "courses": ["MBBS", "MD", "MS", "DM", "MCh"],
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Obstetrics & Gynecology",
            "Orthopedics",
            "Cardiology"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹8-10 LPA",
            "highest": "₹30+ LPA"
        },
        "facilities": ["Teaching Hospital", "Research Labs", "Hostel", "Library"],
        "accreditation": "MCI / NMC Approved",
        "website": "www.medical.tvpm.ac.in",
        "contact": "0471-2443152"
    },
    {
        "name": "Government Medical College Kottayam",
        "short_name": "MCK",
        "location": "Kottayam, Kerala",
        "district": "Kottayam",
        "type": "Medical",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.5,
        "established": 1962,
        "courses": ["MBBS", "MD", "MS"],
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Anesthesiology",
            "Dermatology"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹8-10 LPA",
            "highest": "₹25+ LPA"
        },
        "facilities": ["450-bed Hospital", "Hostel", "Research Center", "Library"],
        "accreditation": "NMC Approved",
        "website": "www.mckottayam.ac.in",
        "contact": "0481-2597227"
    },
    {
        "name": "Government Medical College Kozhikode (Calicut Medical College)",
        "short_name": "MCK",
        "location": "Kozhikode, Kerala",
        "district": "Kozhikode",
        "type": "Medical",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.6,
        "established": 1957,
        "courses": ["MBBS", "MD", "MS", "DM"],
        "specializations": [
            "General Medicine",
            "Surgery",
            "Cardiology",
            "Neurology",
            "Orthopedics"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹8-12 LPA",
            "highest": "₹30+ LPA"
        },
        "facilities": ["1200-bed Hospital", "Advanced Labs", "Hostels", "Library"],
        "accreditation": "NMC Approved",
        "website": "www.mckerala.ac.in",
        "contact": "0495-2353320"
    },

    # Arts & Science Colleges
    {
        "name": "University College Thiruvananthapuram",
        "short_name": "UC Trivandrum",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Arts & Science",
        "affiliation": "University of Kerala",
        "rating": 4.4,
        "established": 1866,
        "courses": ["BA", "B.Sc", "MA", "M.Sc", "PhD"],
        "specializations": [
            "Physics",
            "Chemistry",
            "Mathematics",
            "English",
            "History",
            "Economics"
        ],
        "fees_range": "₹10,000-30,000/year",
        "admission_criteria": "Merit-based / Entrance",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹10 LPA"
        },
        "facilities": ["Library", "Labs", "Auditorium", "Sports Complex"],
        "accreditation": "NAAC A+",
        "website": "www.universitycollege.ac.in",
        "contact": "0471-2305564"
    },
    {
        "name": "St. Teresa's College Ernakulam",
        "short_name": "St. Teresa's",
        "location": "Ernakulam, Kerala",
        "district": "Ernakulam",
        "type": "Arts & Science (Women)",
        "affiliation": "Mahatma Gandhi University",
        "rating": 4.3,
        "established": 1925,
        "courses": ["BA", "B.Sc", "B.Com", "MA", "M.Sc", "M.Com"],
        "specializations": [
            "Psychology",
            "English",
            "Commerce",
            "Computer Science",
            "Biotechnology"
        ],
        "fees_range": "₹15,000-40,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹8 LPA"
        },
        "facilities": ["Library", "Computer Labs", "Hostel", "Chapel"],
        "accreditation": "NAAC A+",
        "website": "www.teresas.ac.in",
        "contact": "0484-2351870"
    },

    # Management Colleges
    {
        "name": "IIM Kozhikode (Indian Institute of Management)",
        "short_name": "IIMK",
        "location": "Kozhikode, Kerala",
        "district": "Kozhikode",
        "type": "Management",
        "affiliation": "Autonomous (Institute of National Importance)",
        "rating": 4.9,
        "established": 1997,
        "courses": ["MBA", "Executive MBA", "PhD"],
        "specializations": [
            "Finance",
            "Marketing",
            "Operations",
            "Strategy",
            "HR"
        ],
        "fees_range": "₹20-25 Lakhs (total)",
        "admission_criteria": "CAT",
        "placements": {
            "average": "₹25-28 LPA",
            "highest": "₹60+ LPA"
        },
        "facilities": ["Residential Campus", "Digital Library", "Sports", "Guest House"],
        "accreditation": "AACSB, AMBA",
        "website": "www.iimk.ac.in",
        "contact": "0495-2809100"
    },
    {
        "name": "Rajagiri College of Social Sciences",
        "short_name": "RCSS",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Management & Social Sciences",
        "affiliation": "Mahatma Gandhi University",
        "rating": 4.2,
        "established": 1955,
        "courses": ["BBA", "MBA", "MSW", "MCA"],
        "specializations": [
            "Business Administration",
            "Social Work",
            "Computer Applications",
            "Tourism Management"
        ],
        "fees_range": "₹1-3 Lakhs/year",
        "admission_criteria": "Entrance Test",
        "placements": {
            "average": "₹5-7 LPA",
            "highest": "₹15 LPA"
        },
        "facilities": ["AC Classrooms", "Hostel", "Library", "Sports"],
        "accreditation": "NAAC A+",
        "website": "www.rajagiri.edu",
        "contact": "0484-2660302"
    },

    # Law Colleges
    {
        "name": "Government Law College Thiruvananthapuram",
        "short_name": "GLC TVM",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Law",
        "affiliation": "University of Kerala",
        "rating": 4.4,
        "established": 1875,
        "courses": ["LLB", "LLM", "BA LLB"],
        "specializations": [
            "Constitutional Law",
            "Criminal Law",
            "Corporate Law",
            "International Law"
        ],
        "fees_range": "₹15,000-30,000/year",
        "admission_criteria": "CLAT / Kerala Law Entrance",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹12 LPA"
        },
        "facilities": ["Moot Court", "Library", "Computer Lab"],
        "accreditation": "Bar Council of India Approved",
        "website": "www.governmentlawcollege.ac.in",
        "contact": "0471-2332144"
    },

    # Pharmacy Colleges
    {
        "name": "Amrita School of Pharmacy Kochi",
        "short_name": "Amrita Pharmacy",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Pharmacy",
        "affiliation": "Amrita Vishwa Vidyapeetham",
        "rating": 4.5,
        "established": 1998,
        "courses": ["B.Pharm", "M.Pharm", "PharmD", "PhD"],
        "specializations": [
            "Pharmaceutics",
            "Pharmacology",
            "Pharmaceutical Chemistry",
            "Pharmacy Practice"
        ],
        "fees_range": "₹1.5-2.5 Lakhs/year",
        "admission_criteria": "KEAM / NEET / Entrance",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹12 LPA"
        },
        "facilities": ["Research Labs", "Hospital Pharmacy", "Hostel", "Library"],
        "accreditation": "NAAC A++",
        "website": "www.amrita.edu/pharmacy",
        "contact": "0484-2858866"
    },

    # Nursing Colleges
    {
        "name": "Government College of Nursing Thiruvananthapuram",
        "short_name": "GCN TVM",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Nursing",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.3,
        "established": 1963,
        "courses": ["B.Sc Nursing", "M.Sc Nursing", "Post Basic B.Sc"],
        "specializations": [
            "Medical-Surgical Nursing",
            "Pediatric Nursing",
            "Community Health",
            "Mental Health"
        ],
        "fees_range": "₹15,000-30,000/year",
        "admission_criteria": "KEAM / NEET",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹8 LPA (abroad)"
        },
        "facilities": ["Nursing Skills Lab", "Hospital Training", "Hostel", "Library"],
        "accreditation": "INC Approved",
        "website": "www.gcnursing.ac.in",
        "contact": "0471-2554812"
    }
]

def populate_colleges():
    """Populate colleges collection with Kerala colleges data"""
    
    print("=" * 60)
    print("KERALA COLLEGES DATA POPULATION")
    print("=" * 60)
    
    try:
        # Check if colleges collection exists and has data
        existing_count = db.colleges.count_documents({})
        print(f"\n📊 Existing colleges in database: {existing_count}")
        
        if existing_count > 0:
            response = input("\n⚠️  Database already has colleges. Do you want to:\n   1. Keep existing and add new\n   2. Delete all and start fresh\n   Enter choice (1 or 2): ")
            
            if response == "2":
                db.colleges.delete_many({})
                print("✓ Deleted existing colleges")
        
        # Add created_at and updated_at to each college
        for college in kerala_colleges:
            college['created_at'] = datetime.utcnow()
            college['updated_at'] = datetime.utcnow()
            college['is_active'] = True
        
        # Insert colleges
        print(f"\n📥 Inserting {len(kerala_colleges)} Kerala colleges...")
        result = db.colleges.insert_many(kerala_colleges)
        
        print(f"✅ Successfully added {len(result.inserted_ids)} colleges!")
        
        # Show summary by type
        print("\n📊 Colleges by Type:")
        types = db.colleges.distinct('type')
        for ctype in types:
            count = db.colleges.count_documents({'type': ctype})
            print(f"   • {ctype}: {count} colleges")
        
        # Show summary by district
        print("\n📍 Colleges by District:")
        districts = db.colleges.distinct('district')
        for district in sorted(districts):
            count = db.colleges.count_documents({'district': district})
            print(f"   • {district}: {count} colleges")
        
        print("\n" + "=" * 60)
        print("✅ KERALA COLLEGES DATA POPULATED SUCCESSFULLY!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error populating colleges: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n🎓 Starting Kerala Colleges Data Population...\n")
    success = populate_colleges()
    
    if success:
        print("\n✅ You can now use the College Finder feature!")
        print("   Total colleges: 15 real Kerala institutions")
        print("   Types: Engineering, Medical, Arts & Science, Management, Law, Pharmacy, Nursing")
    else:
        print("\n❌ Population failed. Check the errors above.")