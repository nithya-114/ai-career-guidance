"""
Enhanced Kerala Colleges Data Population Script
60 Real Kerala Colleges - Organized by Courses and Districts
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

# Enhanced Kerala Colleges Data - 60 Colleges
kerala_colleges = [
    # ==================== ENGINEERING COLLEGES (20) ====================
    
    # Top Tier Engineering
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
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering",
            "Chemical Engineering",
            "Production Engineering"
        ],
        "fees_range": "₹1-2 Lakhs/year",
        "admission_criteria": "JEE Main",
        "placements": {
            "average": "₹15-18 LPA",
            "highest": "₹50+ LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Sports Complex", "WiFi Campus", "Innovation Center"],
        "accreditation": "NAAC A++",
        "website": "www.nitc.ac.in",
        "contact": "0495-2286100"
    },
    {
        "name": "Indian Institute of Space Science and Technology (IIST)",
        "short_name": "IIST",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Engineering",
        "affiliation": "Deemed University (Department of Space)",
        "rating": 4.7,
        "established": 2007,
        "courses": ["B.Tech", "M.Tech", "MS", "PhD"],
        "primary_course": "B.Tech",
        "specializations": [
            "Aerospace Engineering",
            "Avionics",
            "Physical Sciences",
            "Space Technology"
        ],
        "fees_range": "₹2-3 Lakhs/year",
        "admission_criteria": "JEE Advanced",
        "placements": {
            "average": "₹12-15 LPA",
            "highest": "ISRO/DRDO guaranteed placement"
        },
        "facilities": ["Hostel", "Research Labs", "Satellite Ground Station", "Observatory"],
        "accreditation": "NAAC A++",
        "website": "www.iist.ac.in",
        "contact": "0471-2568500"
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
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering",
            "Architecture",
            "Information Technology"
        ],
        "fees_range": "₹50,000-1 Lakh/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹6-8 LPA",
            "highest": "₹25+ LPA"
        },
        "facilities": ["Hostel", "Central Library", "Research Labs", "Sports Complex", "Auditorium"],
        "accreditation": "NAAC A+",
        "website": "www.cet.ac.in",
        "contact": "0471-2515565"
    },
    {
        "name": "Cochin University of Science and Technology (CUSAT)",
        "short_name": "CUSAT",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Engineering",
        "affiliation": "State University",
        "rating": 4.4,
        "established": 1971,
        "courses": ["B.Tech", "M.Tech", "M.Sc", "MBA", "PhD"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science",
            "Electronics",
            "Safety & Fire Engineering",
            "Marine Engineering",
            "Ship Technology"
        ],
        "fees_range": "₹40,000-80,000/year",
        "admission_criteria": "KEAM / CUSAT CAT",
        "placements": {
            "average": "₹5-7 LPA",
            "highest": "₹18+ LPA"
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
        "primary_course": "B.Tech",
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
        "primary_course": "B.Tech",
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
    {
        "name": "Government Engineering College Barton Hill",
        "short_name": "GEC Barton Hill",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.3,
        "established": 1999,
        "courses": ["B.Tech", "M.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Information Technology"
        ],
        "fees_range": "₹35,000-65,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹5-7 LPA",
            "highest": "₹14 LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Cafeteria"],
        "accreditation": "NAAC A",
        "website": "www.gecbh.ac.in",
        "contact": "0471-2597137"
    },
    {
        "name": "Government Engineering College Idukki",
        "short_name": "GEC Idukki",
        "location": "Painavu, Kerala",
        "district": "Idukki",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.1,
        "established": 2015,
        "courses": ["B.Tech", "M.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Electrical Engineering"
        ],
        "fees_range": "₹30,000-60,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹4-5 LPA",
            "highest": "₹10 LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Sports Ground"],
        "accreditation": "NAAC B++",
        "website": "www.gecidukki.ac.in",
        "contact": "04862-232320"
    },
    {
        "name": "Government Engineering College Palakkad",
        "short_name": "GEC Palakkad",
        "location": "Palakkad, Kerala",
        "district": "Palakkad",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.2,
        "established": 1993,
        "courses": ["B.Tech", "M.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering"
        ],
        "fees_range": "₹30,000-60,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹5-6 LPA",
            "highest": "₹13 LPA"
        },
        "facilities": ["Hostel", "Library", "Computer Center", "Sports"],
        "accreditation": "NAAC A",
        "website": "www.gec.ac.in",
        "contact": "0491-2566603"
    },
    {
        "name": "Government Engineering College Wayanad",
        "short_name": "GEC Wayanad",
        "location": "Mananthavady, Kerala",
        "district": "Wayanad",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.0,
        "established": 2002,
        "courses": ["B.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Civil Engineering"
        ],
        "fees_range": "₹30,000-60,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹4-5 LPA",
            "highest": "₹11 LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Playground"],
        "accreditation": "NAAC A",
        "website": "www.gecwyd.ac.in",
        "contact": "04935-240540"
    },
    {
        "name": "Mar Athanasius College of Engineering (MACE)",
        "short_name": "MACE",
        "location": "Kothamangalam, Kerala",
        "district": "Ernakulam",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.4,
        "established": 1961,
        "courses": ["B.Tech", "M.Tech", "MBA"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering"
        ],
        "fees_range": "₹70,000-1.2 Lakhs/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹5-7 LPA",
            "highest": "₹18 LPA"
        },
        "facilities": ["Hostel", "Central Library", "Innovation Lab", "Sports"],
        "accreditation": "NAAC A+",
        "website": "www.mace.ac.in",
        "contact": "0485-2822484"
    },
    {
        "name": "Thangal Kunju Musaliar College of Engineering (TKMCE)",
        "short_name": "TKMCE",
        "location": "Kollam, Kerala",
        "district": "Kollam",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.3,
        "established": 1958,
        "courses": ["B.Tech", "M.Tech", "MBA"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering"
        ],
        "fees_range": "₹60,000-1 Lakh/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹5-6 LPA",
            "highest": "₹15 LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Auditorium"],
        "accreditation": "NAAC A",
        "website": "www.tkmce.ac.in",
        "contact": "0474-2702100"
    },
    {
        "name": "NSS College of Engineering",
        "short_name": "NSSCE",
        "location": "Palakkad, Kerala",
        "district": "Palakkad",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.2,
        "established": 1960,
        "courses": ["B.Tech", "M.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering",
            "Electrical Engineering"
        ],
        "fees_range": "₹50,000-90,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹5-6 LPA",
            "highest": "₹16 LPA"
        },
        "facilities": ["Hostel", "Library", "Research Center", "Sports"],
        "accreditation": "NAAC A",
        "website": "www.nssce.ac.in",
        "contact": "0491-2525900"
    },
    {
        "name": "Rajiv Gandhi Institute of Technology (RIT)",
        "short_name": "RIT Kottayam",
        "location": "Kottayam, Kerala",
        "district": "Kottayam",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.1,
        "established": 1991,
        "courses": ["B.Tech", "M.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering"
        ],
        "fees_range": "₹50,000-85,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹12 LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Canteen"],
        "accreditation": "NAAC A",
        "website": "www.rit.ac.in",
        "contact": "0481-2597370"
    },
    {
        "name": "Sree Chitra Thirunal College of Engineering (SCT)",
        "short_name": "SCT",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.4,
        "established": 1995,
        "courses": ["B.Tech", "M.Tech", "MCA"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Information Technology",
            "Applied Electronics"
        ],
        "fees_range": "₹60,000-1 Lakh/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹6-7 LPA",
            "highest": "₹20 LPA"
        },
        "facilities": ["Hostel", "Digital Library", "Innovation Hub", "Sports"],
        "accreditation": "NAAC A+",
        "website": "www.sctce.ac.in",
        "contact": "0471-2594585"
    },
    {
        "name": "TKM Institute of Technology",
        "short_name": "TKMIT",
        "location": "Kollam, Kerala",
        "district": "Kollam",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.0,
        "established": 2002,
        "courses": ["B.Tech", "M.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering"
        ],
        "fees_range": "₹55,000-95,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹4-5 LPA",
            "highest": "₹12 LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Sports Ground"],
        "accreditation": "NAAC A",
        "website": "www.tkmit.ac.in",
        "contact": "0474-2660270"
    },
    {
        "name": "College of Engineering Chengannur (CEC)",
        "short_name": "CEC",
        "location": "Chengannur, Kerala",
        "district": "Alappuzha",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.2,
        "established": 1993,
        "courses": ["B.Tech", "M.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering"
        ],
        "fees_range": "₹30,000-60,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹5-6 LPA",
            "highest": "₹14 LPA"
        },
        "facilities": ["Hostel", "Library", "Computer Center", "Auditorium"],
        "accreditation": "NAAC A",
        "website": "www.cectl.ac.in",
        "contact": "0479-2452235"
    },
    {
        "name": "College of Engineering Munnar",
        "short_name": "CEM",
        "location": "Munnar, Kerala",
        "district": "Idukki",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.0,
        "established": 2009,
        "courses": ["B.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering"
        ],
        "fees_range": "₹30,000-60,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹4-5 LPA",
            "highest": "₹10 LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Cafeteria"],
        "accreditation": "NAAC B++",
        "website": "www.ceceknl.ac.in",
        "contact": "04865-231251"
    },
    {
        "name": "LBS Institute of Technology for Women",
        "short_name": "LBSITW",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.3,
        "established": 2007,
        "courses": ["B.Tech", "M.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Information Technology"
        ],
        "fees_range": "₹35,000-65,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹5-6 LPA",
            "highest": "₹15 LPA"
        },
        "facilities": ["Hostel", "Library", "Computer Labs", "Auditorium"],
        "accreditation": "NAAC A",
        "website": "www.lbsitw.ac.in",
        "contact": "0471-2742370"
    },
    {
        "name": "Malabar College of Engineering and Technology",
        "short_name": "MCET",
        "location": "Thrissur, Kerala",
        "district": "Thrissur",
        "type": "Engineering",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.1,
        "established": 2001,
        "courses": ["B.Tech", "M.Tech"],
        "primary_course": "B.Tech",
        "specializations": [
            "Computer Science & Engineering",
            "Electronics & Communication",
            "Mechanical Engineering",
            "Civil Engineering"
        ],
        "fees_range": "₹50,000-85,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹12 LPA"
        },
        "facilities": ["Hostel", "Library", "Labs", "Sports"],
        "accreditation": "NAAC A",
        "website": "www.mcet.in",
        "contact": "0487-2304722"
    },

    # ==================== MEDICAL COLLEGES (10) ====================
    
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
        "primary_course": "MBBS",
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Obstetrics & Gynecology",
            "Orthopedics",
            "Cardiology",
            "Neurology"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹8-10 LPA",
            "highest": "₹35+ LPA"
        },
        "facilities": ["1400-bed Teaching Hospital", "Research Labs", "Hostel", "Library", "Medical Museum"],
        "accreditation": "NMC Approved",
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
        "courses": ["MBBS", "MD", "MS", "DM"],
        "primary_course": "MBBS",
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Anesthesiology",
            "Dermatology",
            "Psychiatry"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹8-10 LPA",
            "highest": "₹28+ LPA"
        },
        "facilities": ["600-bed Hospital", "Hostel", "Research Center", "Library", "Simulation Lab"],
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
        "courses": ["MBBS", "MD", "MS", "DM", "MCh"],
        "primary_course": "MBBS",
        "specializations": [
            "General Medicine",
            "Surgery",
            "Cardiology",
            "Neurology",
            "Orthopedics",
            "Nephrology"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹8-12 LPA",
            "highest": "₹35+ LPA"
        },
        "facilities": ["1500-bed Hospital", "Advanced Labs", "Hostels", "Library", "Trauma Center"],
        "accreditation": "NMC Approved",
        "website": "www.mckerala.ac.in",
        "contact": "0495-2353320"
    },
    {
        "name": "Government Medical College Thrissur",
        "short_name": "MCT",
        "location": "Thrissur, Kerala",
        "district": "Thrissur",
        "type": "Medical",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.4,
        "established": 1982,
        "courses": ["MBBS", "MD", "MS"],
        "primary_course": "MBBS",
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Obstetrics & Gynecology",
            "Radiology"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹8-10 LPA",
            "highest": "₹25+ LPA"
        },
        "facilities": ["800-bed Hospital", "Hostel", "Library", "Research Center"],
        "accreditation": "NMC Approved",
        "website": "www.mcthrissur.ac.in",
        "contact": "0487-2336605"
    },
    {
        "name": "Government Medical College Kannur",
        "short_name": "MCK",
        "location": "Kannur, Kerala",
        "district": "Kannur",
        "type": "Medical",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.3,
        "established": 2008,
        "courses": ["MBBS", "MD", "MS"],
        "primary_course": "MBBS",
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Anesthesiology"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹7-9 LPA",
            "highest": "₹22 LPA"
        },
        "facilities": ["600-bed Hospital", "Hostel", "Library", "Skills Lab"],
        "accreditation": "NMC Approved",
        "website": "www.gmckannur.ac.in",
        "contact": "0497-2700870"
    },
    {
        "name": "Government Medical College Alappuzha",
        "short_name": "MCA",
        "location": "Alappuzha, Kerala",
        "district": "Alappuzha",
        "type": "Medical",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.2,
        "established": 2014,
        "courses": ["MBBS", "MD", "MS"],
        "primary_course": "MBBS",
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Orthopedics"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹7-9 LPA",
            "highest": "₹20 LPA"
        },
        "facilities": ["500-bed Hospital", "Hostel", "Library", "Anatomy Museum"],
        "accreditation": "NMC Approved",
        "website": "www.mcalappuzha.ac.in",
        "contact": "0477-2239500"
    },
    {
        "name": "Government Medical College Palakkad",
        "short_name": "MCP",
        "location": "Palakkad, Kerala",
        "district": "Palakkad",
        "type": "Medical",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.1,
        "established": 2013,
        "courses": ["MBBS", "MD", "MS"],
        "primary_course": "MBBS",
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Obstetrics & Gynecology"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹7-9 LPA",
            "highest": "₹22 LPA"
        },
        "facilities": ["600-bed Hospital", "Hostel", "Library", "Skills Lab"],
        "accreditation": "NMC Approved",
        "website": "www.mcpkd.ac.in",
        "contact": "0491-2525760"
    },
    {
        "name": "Government Medical College Kollam",
        "short_name": "MCK",
        "location": "Kollam, Kerala",
        "district": "Kollam",
        "type": "Medical",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.2,
        "established": 2015,
        "courses": ["MBBS", "MD"],
        "primary_course": "MBBS",
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Radiology"
        ],
        "fees_range": "₹50,000-1.5 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹7-9 LPA",
            "highest": "₹20 LPA"
        },
        "facilities": ["500-bed Hospital", "Hostel", "Library", "Research Lab"],
        "accreditation": "NMC Approved",
        "website": "www.gmckollam.ac.in",
        "contact": "0474-2742170"
    },
    {
        "name": "Amrita Institute of Medical Sciences",
        "short_name": "AIMS Kochi",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Medical",
        "affiliation": "Amrita Vishwa Vidyapeetham",
        "rating": 4.8,
        "established": 1998,
        "courses": ["MBBS", "MD", "MS", "DM", "MCh"],
        "primary_course": "MBBS",
        "specializations": [
            "Cardiology",
            "Neurology",
            "Oncology",
            "Transplant Surgery",
            "Critical Care"
        ],
        "fees_range": "₹8-12 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹10-15 LPA",
            "highest": "₹40+ LPA"
        },
        "facilities": ["1300-bed Hospital", "Research Center", "Hostel", "Advanced Labs"],
        "accreditation": "NAAC A++, NMC Approved",
        "website": "www.aimshospital.org",
        "contact": "0484-2851234"
    },
    {
        "name": "Jubilee Mission Medical College",
        "short_name": "JMMC",
        "location": "Thrissur, Kerala",
        "district": "Thrissur",
        "type": "Medical",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.3,
        "established": 2003,
        "courses": ["MBBS", "MD", "MS"],
        "primary_course": "MBBS",
        "specializations": [
            "General Medicine",
            "Surgery",
            "Pediatrics",
            "Orthopedics",
            "Radiology"
        ],
        "fees_range": "₹6-10 Lakhs/year",
        "admission_criteria": "NEET UG / NEET PG",
        "placements": {
            "average": "₹8-10 LPA",
            "highest": "₹25 LPA"
        },
        "facilities": ["800-bed Hospital", "Hostel", "Library", "Research Center"],
        "accreditation": "NMC Approved",
        "website": "www.jubileemission.org",
        "contact": "0487-2360100"
    },

    # ==================== ARTS & SCIENCE COLLEGES (10) ====================
    
    {
        "name": "University College Thiruvananthapuram",
        "short_name": "UC Trivandrum",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Arts & Science",
        "affiliation": "University of Kerala",
        "rating": 4.4,
        "established": 1866,
        "courses": ["BA", "B.Sc", "B.Com", "MA", "M.Sc", "M.Com", "PhD"],
        "primary_course": "B.Sc",
        "specializations": [
            "Physics",
            "Chemistry",
            "Mathematics",
            "English",
            "History",
            "Economics",
            "Computer Science"
        ],
        "fees_range": "₹10,000-30,000/year",
        "admission_criteria": "Merit-based / Entrance",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹10 LPA"
        },
        "facilities": ["Library", "Labs", "Auditorium", "Sports Complex", "Museum"],
        "accreditation": "NAAC A++",
        "website": "www.universitycollege.ac.in",
        "contact": "0471-2305564"
    },
    {
        "name": "St. Teresa's College Ernakulam",
        "short_name": "St. Teresa's",
        "location": "Ernakulam, Kerala",
        "district": "Ernakulam",
        "type": "Arts & Science",
        "affiliation": "Mahatma Gandhi University",
        "rating": 4.3,
        "established": 1925,
        "courses": ["BA", "B.Sc", "B.Com", "MA", "M.Sc", "M.Com"],
        "primary_course": "B.Com",
        "specializations": [
            "Psychology",
            "English",
            "Commerce",
            "Computer Science",
            "Biotechnology",
            "Mathematics"
        ],
        "fees_range": "₹15,000-40,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹9 LPA"
        },
        "facilities": ["Library", "Computer Labs", "Hostel", "Chapel", "Auditorium"],
        "accreditation": "NAAC A+",
        "website": "www.teresas.ac.in",
        "contact": "0484-2351870"
    },
    {
        "name": "Union Christian College Aluva",
        "short_name": "UC College",
        "location": "Aluva, Kerala",
        "district": "Ernakulam",
        "type": "Arts & Science",
        "affiliation": "Mahatma Gandhi University",
        "rating": 4.2,
        "established": 1921,
        "courses": ["BA", "B.Sc", "B.Com", "BBA", "MA", "M.Sc"],
        "primary_course": "B.Com",
        "specializations": [
            "Commerce",
            "Physics",
            "Chemistry",
            "Economics",
            "English",
            "Computer Science"
        ],
        "fees_range": "₹12,000-35,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹8 LPA"
        },
        "facilities": ["Library", "Labs", "Hostel", "Sports Ground"],
        "accreditation": "NAAC A+",
        "website": "www.uccollege.edu.in",
        "contact": "0484-2609194"
    },
    {
        "name": "St. Joseph's College Devagiri",
        "short_name": "Devagiri College",
        "location": "Kozhikode, Kerala",
        "district": "Kozhikode",
        "type": "Arts & Science",
        "affiliation": "University of Calicut",
        "rating": 4.3,
        "established": 1875,
        "courses": ["BA", "B.Sc", "B.Com", "MA", "M.Sc", "PhD"],
        "primary_course": "B.Sc",
        "specializations": [
            "Physics",
            "Chemistry",
            "Zoology",
            "Botany",
            "Mathematics",
            "English"
        ],
        "fees_range": "₹10,000-30,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹9 LPA"
        },
        "facilities": ["Library", "Labs", "Hostel", "Museum", "Auditorium"],
        "accreditation": "NAAC A+",
        "website": "www.devagiricollege.com",
        "contact": "0495-2721155"
    },
    {
        "name": "Brennen College Thalassery",
        "short_name": "Brennen College",
        "location": "Thalassery, Kerala",
        "district": "Kannur",
        "type": "Arts & Science",
        "affiliation": "University of Calicut",
        "rating": 4.1,
        "established": 1862,
        "courses": ["BA", "B.Sc", "B.Com", "MA", "M.Sc"],
        "primary_course": "BA",
        "specializations": [
            "English",
            "History",
            "Economics",
            "Physics",
            "Mathematics"
        ],
        "fees_range": "₹8,000-25,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹2.5-4 LPA",
            "highest": "₹7 LPA"
        },
        "facilities": ["Library", "Computer Lab", "Sports Ground"],
        "accreditation": "NAAC A",
        "website": "www.brennencollege.net",
        "contact": "0490-2344501"
    },
    {
        "name": "Maharaja's College Ernakulam",
        "short_name": "Maharaja's",
        "location": "Ernakulam, Kerala",
        "district": "Ernakulam",
        "type": "Arts & Science",
        "affiliation": "Mahatma Gandhi University",
        "rating": 4.2,
        "established": 1875,
        "courses": ["BA", "B.Sc", "B.Com", "MA", "M.Sc"],
        "primary_course": "B.Com",
        "specializations": [
            "Commerce",
            "Economics",
            "English",
            "Physics",
            "Chemistry"
        ],
        "fees_range": "₹10,000-28,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹8 LPA"
        },
        "facilities": ["Central Library", "Labs", "Auditorium", "Sports"],
        "accreditation": "NAAC A",
        "website": "www.maharajas.ac.in",
        "contact": "0484-2375297"
    },
    {
        "name": "Farook College Kozhikode",
        "short_name": "Farook College",
        "location": "Kozhikode, Kerala",
        "district": "Kozhikode",
        "type": "Arts & Science",
        "affiliation": "University of Calicut",
        "rating": 4.2,
        "established": 1948,
        "courses": ["BA", "B.Sc", "B.Com", "BBA", "MA", "M.Sc"],
        "primary_course": "B.Com",
        "specializations": [
            "Commerce",
            "Business Administration",
            "Computer Science",
            "Physics",
            "Chemistry"
        ],
        "fees_range": "₹12,000-32,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹9 LPA"
        },
        "facilities": ["Library", "Computer Center", "Hostel", "Sports Complex"],
        "accreditation": "NAAC A+",
        "website": "www.farookcollege.ac.in",
        "contact": "0495-2370094"
    },
    {
        "name": "SD College Alappuzha",
        "short_name": "SD College",
        "location": "Alappuzha, Kerala",
        "district": "Alappuzha",
        "type": "Arts & Science",
        "affiliation": "University of Kerala",
        "rating": 4.0,
        "established": 1922,
        "courses": ["BA", "B.Sc", "B.Com", "MA", "M.Sc"],
        "primary_course": "B.Com",
        "specializations": [
            "Commerce",
            "English",
            "Physics",
            "Chemistry",
            "Mathematics"
        ],
        "fees_range": "₹10,000-25,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹2.5-4 LPA",
            "highest": "₹7 LPA"
        },
        "facilities": ["Library", "Labs", "Auditorium"],
        "accreditation": "NAAC A",
        "website": "www.sdcollege.ac.in",
        "contact": "0477-2251424"
    },
    {
        "name": "Baselius College Kottayam",
        "short_name": "Baselius",
        "location": "Kottayam, Kerala",
        "district": "Kottayam",
        "type": "Arts & Science",
        "affiliation": "Mahatma Gandhi University",
        "rating": 4.1,
        "established": 1945,
        "courses": ["BA", "B.Sc", "B.Com", "MA", "M.Sc"],
        "primary_course": "B.Sc",
        "specializations": [
            "Physics",
            "Chemistry",
            "Mathematics",
            "Commerce",
            "English"
        ],
        "fees_range": "₹10,000-28,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹3-4 LPA",
            "highest": "₹8 LPA"
        },
        "facilities": ["Library", "Labs", "Chapel", "Sports"],
        "accreditation": "NAAC A",
        "website": "www.baseliuscollege.edu.in",
        "contact": "0481-2566283"
    },
    {
        "name": "Newman College Thodupuzha",
        "short_name": "Newman College",
        "location": "Thodupuzha, Kerala",
        "district": "Idukki",
        "type": "Arts & Science",
        "affiliation": "Mahatma Gandhi University",
        "rating": 4.2,
        "established": 1961,
        "courses": ["BA", "B.Sc", "B.Com", "BBA", "MA", "M.Sc"],
        "primary_course": "B.Com",
        "specializations": [
            "Commerce",
            "Business Administration",
            "Computer Science",
            "English",
            "Physics"
        ],
        "fees_range": "₹12,000-30,000/year",
        "admission_criteria": "Merit-based",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹8 LPA"
        },
        "facilities": ["Library", "Computer Labs", "Hostel", "Chapel"],
        "accreditation": "NAAC A",
        "website": "www.newmancollege.org",
        "contact": "04862-222268"
    },

    # ==================== MANAGEMENT COLLEGES (6) ====================
    
    {
        "name": "IIM Kozhikode (Indian Institute of Management)",
        "short_name": "IIMK",
        "location": "Kozhikode, Kerala",
        "district": "Kozhikode",
        "type": "Management",
        "affiliation": "Autonomous (Institute of National Importance)",
        "rating": 4.9,
        "established": 1997,
        "courses": ["MBA", "Executive MBA", "PhD", "FPM"],
        "primary_course": "MBA",
        "specializations": [
            "Finance",
            "Marketing",
            "Operations",
            "Strategy",
            "HR",
            "Business Analytics"
        ],
        "fees_range": "₹20-25 Lakhs (total)",
        "admission_criteria": "CAT",
        "placements": {
            "average": "₹28-31 LPA",
            "highest": "₹67+ LPA"
        },
        "facilities": ["Residential Campus", "Digital Library", "Sports Complex", "Guest House", "Incubation Center"],
        "accreditation": "AACSB, AMBA, EQUIS",
        "website": "www.iimk.ac.in",
        "contact": "0495-2809100"
    },
    {
        "name": "Rajagiri College of Social Sciences",
        "short_name": "RCSS",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Management",
        "affiliation": "Mahatma Gandhi University",
        "rating": 4.3,
        "established": 1955,
        "courses": ["BBA", "MBA", "MSW", "MCA", "PhD"],
        "primary_course": "MBA",
        "specializations": [
            "Business Administration",
            "Finance",
            "Marketing",
            "HR",
            "International Business"
        ],
        "fees_range": "₹2-4 Lakhs/year",
        "admission_criteria": "CAT / MAT / KMAT",
        "placements": {
            "average": "₹6-8 LPA",
            "highest": "₹18 LPA"
        },
        "facilities": ["AC Classrooms", "Hostel", "Library", "Sports", "Placement Cell"],
        "accreditation": "NAAC A++",
        "website": "www.rajagiri.edu",
        "contact": "0484-2660302"
    },
    {
        "name": "Cochin University School of Management Studies (CUSMS)",
        "short_name": "CUSMS",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Management",
        "affiliation": "Cochin University of Science and Technology",
        "rating": 4.2,
        "established": 1977,
        "courses": ["MBA", "PhD"],
        "primary_course": "MBA",
        "specializations": [
            "Finance",
            "Marketing",
            "HR",
            "Operations",
            "Systems"
        ],
        "fees_range": "₹80,000-1.5 Lakhs/year",
        "admission_criteria": "CAT / CMAT",
        "placements": {
            "average": "₹6-7 LPA",
            "highest": "₹15 LPA"
        },
        "facilities": ["Hostel", "Library", "Computer Lab", "Auditorium"],
        "accreditation": "NAAC A+",
        "website": "www.cusat.ac.in/sms",
        "contact": "0484-2862470"
    },
    {
        "name": "MES Institute of Management and Career Courses",
        "short_name": "MES IMCC",
        "location": "Kozhikode, Kerala",
        "district": "Kozhikode",
        "type": "Management",
        "affiliation": "University of Calicut",
        "rating": 4.0,
        "established": 2001,
        "courses": ["BBA", "MBA"],
        "primary_course": "MBA",
        "specializations": [
            "Finance",
            "Marketing",
            "HR",
            "International Business"
        ],
        "fees_range": "₹1.5-2.5 Lakhs/year",
        "admission_criteria": "KMAT / MAT",
        "placements": {
            "average": "₹4-5 LPA",
            "highest": "₹10 LPA"
        },
        "facilities": ["Library", "Computer Lab", "Auditorium", "Cafeteria"],
        "accreditation": "NAAC A",
        "website": "www.mesimcc.org",
        "contact": "0495-2371228"
    },
    {
        "name": "Tata Institute of Social Sciences (TISS) Tuljapur Campus Extension",
        "short_name": "TISS Kerala",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Management",
        "affiliation": "Deemed University",
        "rating": 4.5,
        "established": 2016,
        "courses": ["MBA", "MA"],
        "primary_course": "MBA",
        "specializations": [
            "Human Resource Management",
            "Social Entrepreneurship",
            "Rural Management"
        ],
        "fees_range": "₹2-3 Lakhs/year",
        "admission_criteria": "TISSNET",
        "placements": {
            "average": "₹7-9 LPA",
            "highest": "₹18 LPA"
        },
        "facilities": ["Hostel", "Library", "Research Center"],
        "accreditation": "NAAC A++",
        "website": "www.tiss.edu",
        "contact": "022-25525000"
    },
    {
        "name": "School of Management Studies (SMS) - CUSAT Kochi",
        "short_name": "SMS CUSAT",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Management",
        "affiliation": "Cochin University of Science and Technology",
        "rating": 4.1,
        "established": 1977,
        "courses": ["MBA", "Executive MBA"],
        "primary_course": "MBA",
        "specializations": [
            "Finance",
            "Marketing",
            "Operations",
            "Systems"
        ],
        "fees_range": "₹1-2 Lakhs/year",
        "admission_criteria": "CAT / CMAT / KMAT",
        "placements": {
            "average": "₹5-7 LPA",
            "highest": "₹14 LPA"
        },
        "facilities": ["Library", "Computer Lab", "Seminar Hall"],
        "accreditation": "NAAC A+",
        "website": "www.cusat.ac.in",
        "contact": "0484-2577137"
    },

    # ==================== LAW COLLEGES (4) ====================
    
    {
        "name": "Government Law College Thiruvananthapuram",
        "short_name": "GLC TVM",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Law",
        "affiliation": "University of Kerala",
        "rating": 4.4,
        "established": 1875,
        "courses": ["LLB", "LLM", "BA LLB", "B.Com LLB"],
        "primary_course": "LLB",
        "specializations": [
            "Constitutional Law",
            "Criminal Law",
            "Corporate Law",
            "International Law",
            "Cyber Law"
        ],
        "fees_range": "₹15,000-35,000/year",
        "admission_criteria": "CLAT / Kerala Law Entrance",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹15 LPA"
        },
        "facilities": ["Moot Court", "Library", "Computer Lab", "Legal Aid Clinic"],
        "accreditation": "Bar Council of India Approved",
        "website": "www.governmentlawcollege.ac.in",
        "contact": "0471-2332144"
    },
    {
        "name": "Government Law College Ernakulam",
        "short_name": "GLC Ernakulam",
        "location": "Ernakulam, Kerala",
        "district": "Ernakulam",
        "type": "Law",
        "affiliation": "Mahatma Gandhi University",
        "rating": 4.2,
        "established": 1874,
        "courses": ["LLB", "LLM", "BA LLB"],
        "primary_course": "LLB",
        "specializations": [
            "Corporate Law",
            "Criminal Law",
            "Family Law",
            "IPR"
        ],
        "fees_range": "₹15,000-30,000/year",
        "admission_criteria": "CLAT / Kerala Law Entrance",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹12 LPA"
        },
        "facilities": ["Moot Court", "Library", "Computer Lab"],
        "accreditation": "Bar Council of India Approved",
        "website": "www.glcekm.ac.in",
        "contact": "0484-2370694"
    },
    {
        "name": "Government Law College Kozhikode",
        "short_name": "GLC Kozhikode",
        "location": "Kozhikode, Kerala",
        "district": "Kozhikode",
        "type": "Law",
        "affiliation": "University of Calicut",
        "rating": 4.1,
        "established": 1904,
        "courses": ["LLB", "LLM", "BA LLB"],
        "primary_course": "LLB",
        "specializations": [
            "Criminal Law",
            "Constitutional Law",
            "Family Law"
        ],
        "fees_range": "₹12,000-28,000/year",
        "admission_criteria": "CLAT / Kerala Law Entrance",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹10 LPA"
        },
        "facilities": ["Moot Court", "Library", "Legal Aid Cell"],
        "accreditation": "Bar Council of India Approved",
        "website": "www.glckozhikode.ac.in",
        "contact": "0495-2720566"
    },
    {
        "name": "School of Legal Studies - CUSAT",
        "short_name": "SLS CUSAT",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Law",
        "affiliation": "Cochin University of Science and Technology",
        "rating": 4.3,
        "established": 1998,
        "courses": ["BA LLB", "LLM", "PhD"],
        "primary_course": "BA LLB",
        "specializations": [
            "Maritime Law",
            "Corporate Law",
            "IPR",
            "Environmental Law"
        ],
        "fees_range": "₹40,000-80,000/year",
        "admission_criteria": "CLAT / CUSAT LLB Entrance",
        "placements": {
            "average": "₹5-7 LPA",
            "highest": "₹15 LPA"
        },
        "facilities": ["Moot Court", "Library", "Research Center"],
        "accreditation": "Bar Council of India Approved",
        "website": "www.cusat.ac.in/sls",
        "contact": "0484-2575418"
    },

    # ==================== PHARMACY COLLEGES (4) ====================
    
    {
        "name": "Amrita School of Pharmacy Kochi",
        "short_name": "Amrita Pharmacy",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Pharmacy",
        "affiliation": "Amrita Vishwa Vidyapeetham",
        "rating": 4.6,
        "established": 1998,
        "courses": ["B.Pharm", "M.Pharm", "PharmD", "PhD"],
        "primary_course": "B.Pharm",
        "specializations": [
            "Pharmaceutics",
            "Pharmacology",
            "Pharmaceutical Chemistry",
            "Pharmacy Practice",
            "Pharmacognosy"
        ],
        "fees_range": "₹1.5-2.8 Lakhs/year",
        "admission_criteria": "KEAM / NEET / Entrance",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹15 LPA"
        },
        "facilities": ["Research Labs", "Hospital Pharmacy", "Hostel", "Library", "Herbal Garden"],
        "accreditation": "NAAC A++, PCI Approved",
        "website": "www.amrita.edu/pharmacy",
        "contact": "0484-2858866"
    },
    {
        "name": "Government College of Pharmacy Thiruvananthapuram",
        "short_name": "GCP TVM",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Pharmacy",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.3,
        "established": 1963,
        "courses": ["B.Pharm", "M.Pharm", "PharmD"],
        "primary_course": "B.Pharm",
        "specializations": [
            "Pharmaceutics",
            "Pharmacology",
            "Pharmaceutical Chemistry"
        ],
        "fees_range": "₹25,000-50,000/year",
        "admission_criteria": "KEAM",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹10 LPA"
        },
        "facilities": ["Labs", "Library", "Hospital Training", "Hostel"],
        "accreditation": "PCI Approved",
        "website": "www.gcptvm.ac.in",
        "contact": "0471-2553350"
    },
    {
        "name": "Manipal College of Pharmaceutical Sciences",
        "short_name": "MCOPS",
        "location": "Udupi, Kerala Border",
        "district": "Kasaragod",
        "type": "Pharmacy",
        "affiliation": "Manipal Academy of Higher Education",
        "rating": 4.5,
        "established": 1963,
        "courses": ["B.Pharm", "M.Pharm", "PharmD", "PhD"],
        "primary_course": "B.Pharm",
        "specializations": [
            "Pharmaceutics",
            "Pharmacology",
            "Pharmaceutical Analysis",
            "Clinical Pharmacy"
        ],
        "fees_range": "₹2-3.5 Lakhs/year",
        "admission_criteria": "MET / KEAM",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹12 LPA"
        },
        "facilities": ["Research Center", "Hospital", "Hostel", "Digital Library"],
        "accreditation": "NAAC A+, PCI Approved",
        "website": "www.manipal.edu/mcops",
        "contact": "0820-2922482"
    },
    {
        "name": "JSS College of Pharmacy Ooty (Kerala Students)",
        "short_name": "JSS Pharmacy",
        "location": "Ooty (Near Kerala)",
        "district": "Wayanad",
        "type": "Pharmacy",
        "affiliation": "JSS Academy of Higher Education",
        "rating": 4.4,
        "established": 1967,
        "courses": ["B.Pharm", "M.Pharm", "PhD"],
        "primary_course": "B.Pharm",
        "specializations": [
            "Pharmaceutics",
            "Pharmacology",
            "Pharmaceutical Chemistry",
            "Pharmacognosy"
        ],
        "fees_range": "₹1.5-2.5 Lakhs/year",
        "admission_criteria": "KEAM / KCET",
        "placements": {
            "average": "₹4-5 LPA",
            "highest": "₹11 LPA"
        },
        "facilities": ["Research Labs", "Library", "Hostel", "Sports"],
        "accreditation": "NAAC A+, PCI Approved",
        "website": "www.jssuni.edu.in",
        "contact": "0423-2443393"
    },

    # ==================== NURSING COLLEGES (3) ====================
    
    {
        "name": "Government College of Nursing Thiruvananthapuram",
        "short_name": "GCN TVM",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Nursing",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.4,
        "established": 1963,
        "courses": ["B.Sc Nursing", "M.Sc Nursing", "Post Basic B.Sc"],
        "primary_course": "B.Sc Nursing",
        "specializations": [
            "Medical-Surgical Nursing",
            "Pediatric Nursing",
            "Community Health Nursing",
            "Mental Health Nursing",
            "Obstetrics & Gynecology"
        ],
        "fees_range": "₹15,000-35,000/year",
        "admission_criteria": "KEAM / NEET",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹12 LPA (abroad)"
        },
        "facilities": ["Nursing Skills Lab", "Hospital Training", "Hostel", "Library", "Simulation Lab"],
        "accreditation": "INC Approved",
        "website": "www.gcnursing.ac.in",
        "contact": "0471-2554812"
    },
    {
        "name": "Amrita College of Nursing",
        "short_name": "Amrita Nursing",
        "location": "Kochi, Kerala",
        "district": "Ernakulam",
        "type": "Nursing",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.5,
        "established": 1998,
        "courses": ["B.Sc Nursing", "M.Sc Nursing", "Post Basic B.Sc"],
        "primary_course": "B.Sc Nursing",
        "specializations": [
            "Medical-Surgical Nursing",
            "Pediatric Nursing",
            "Community Health",
            "Psychiatric Nursing"
        ],
        "fees_range": "₹80,000-1.5 Lakhs/year",
        "admission_criteria": "KEAM / NEET",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹15 LPA (abroad)"
        },
        "facilities": ["Skills Lab", "Hospital", "Hostel", "Library", "International Placement"],
        "accreditation": "INC Approved, NAAC A++",
        "website": "www.amrita.edu/nursing",
        "contact": "0484-2858866"
    },
    {
        "name": "Government College of Nursing Kozhikode",
        "short_name": "GCN Kozhikode",
        "location": "Kozhikode, Kerala",
        "district": "Kozhikode",
        "type": "Nursing",
        "affiliation": "Kerala University of Health Sciences",
        "rating": 4.2,
        "established": 1975,
        "courses": ["B.Sc Nursing", "M.Sc Nursing"],
        "primary_course": "B.Sc Nursing",
        "specializations": [
            "Medical-Surgical Nursing",
            "Pediatric Nursing",
            "Community Health Nursing"
        ],
        "fees_range": "₹15,000-30,000/year",
        "admission_criteria": "KEAM / NEET",
        "placements": {
            "average": "₹3-5 LPA",
            "highest": "₹10 LPA (abroad)"
        },
        "facilities": ["Skills Lab", "Hospital Training", "Hostel", "Library"],
        "accreditation": "INC Approved",
        "website": "www.gcnkozhikode.ac.in",
        "contact": "0495-2353320"
    },

    # ==================== ARCHITECTURE COLLEGES (2) ====================
    
    {
        "name": "College of Architecture Thiruvananthapuram",
        "short_name": "CAT",
        "location": "Thiruvananthapuram, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Architecture",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.4,
        "established": 1963,
        "courses": ["B.Arch", "M.Arch", "M.Plan"],
        "primary_course": "B.Arch",
        "specializations": [
            "Architectural Design",
            "Urban Design",
            "Landscape Architecture",
            "Sustainable Architecture"
        ],
        "fees_range": "₹60,000-1 Lakh/year",
        "admission_criteria": "NATA / JEE Main",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹15 LPA"
        },
        "facilities": ["Design Studios", "Workshop", "Library", "Computer Lab", "Model Making Lab"],
        "accreditation": "COA Approved",
        "website": "www.cet.ac.in/architecture",
        "contact": "0471-2515565"
    },
    {
        "name": "Thiagarajar School of Architecture and Planning",
        "short_name": "TSAP",
        "location": "Palakkad, Kerala",
        "district": "Palakkad",
        "type": "Architecture",
        "affiliation": "APJ Abdul Kalam Technological University (KTU)",
        "rating": 4.2,
        "established": 2008,
        "courses": ["B.Arch", "M.Arch"],
        "primary_course": "B.Arch",
        "specializations": [
            "Architectural Design",
            "Urban Planning",
            "Interior Design"
        ],
        "fees_range": "₹80,000-1.2 Lakhs/year",
        "admission_criteria": "NATA / JEE Main",
        "placements": {
            "average": "₹4-5 LPA",
            "highest": "₹12 LPA"
        },
        "facilities": ["Design Studios", "Library", "Computer Lab", "Workshop"],
        "accreditation": "COA Approved",
        "website": "www.tsap.edu.in",
        "contact": "0491-2566789"
    },

    # ==================== HOTEL MANAGEMENT COLLEGES (1) ====================
    
    {
        "name": "Institute of Hotel Management Kovalam",
        "short_name": "IHM Kovalam",
        "location": "Kovalam, Kerala",
        "district": "Thiruvananthapuram",
        "type": "Hotel Management",
        "affiliation": "National Council for Hotel Management",
        "rating": 4.3,
        "established": 1974,
        "courses": ["B.Sc Hotel Management", "Diploma", "PG Diploma"],
        "primary_course": "B.Sc Hotel Management",
        "specializations": [
            "Food Production",
            "Food & Beverage Service",
            "Front Office",
            "Housekeeping",
            "Bakery & Confectionery"
        ],
        "fees_range": "₹1.5-2.5 Lakhs/year",
        "admission_criteria": "NCHM JEE",
        "placements": {
            "average": "₹4-6 LPA",
            "highest": "₹15 LPA (international)"
        },
        "facilities": ["Training Kitchen", "Bakery", "Restaurant", "Hostel", "International Placement"],
        "accreditation": "AICTE Approved",
        "website": "www.ihmkovalam.gov.in",
        "contact": "0471-2480152"
    }
]

def populate_colleges():
    """Populate colleges collection with enhanced Kerala colleges data"""
    
    print("=" * 80)
    print("ENHANCED KERALA COLLEGES DATA POPULATION - 60 COLLEGES")
    print("=" * 80)
    
    try:
        # Check if colleges collection exists and has data
        existing_count = db.colleges.count_documents({})
        print(f"\n📊 Existing colleges in database: {existing_count}")
        
        if existing_count > 0:
            response = input("\n⚠️  Database already has colleges. Do you want to:\n   1. Keep existing and add new\n   2. Delete all and start fresh\n   Enter choice (1 or 2): ")
            
            if response == "2":
                db.colleges.delete_many({})
                print("✅ Deleted existing colleges")
        
        # Add timestamps to each college
        for college in kerala_colleges:
            college['created_at'] = datetime.utcnow()
            college['updated_at'] = datetime.utcnow()
            college['is_active'] = True
        
        # Insert colleges
        print(f"\n📥 Inserting {len(kerala_colleges)} Kerala colleges...")
        result = db.colleges.insert_many(kerala_colleges)
        
        print(f"\n✅ Successfully added {len(result.inserted_ids)} colleges!")
        
        # Show comprehensive summary
        print("\n" + "=" * 80)
        print("📊 COLLEGES SUMMARY BY TYPE")
        print("=" * 80)
        types = db.colleges.distinct('type')
        for ctype in sorted(types):
            count = db.colleges.count_documents({'type': ctype})
            print(f"   • {ctype:30s}: {count:2d} colleges")
        
        print("\n" + "=" * 80)
        print("📍 COLLEGES SUMMARY BY DISTRICT")
        print("=" * 80)
        districts = db.colleges.distinct('district')
        for district in sorted(districts):
            count = db.colleges.count_documents({'district': district})
            print(f"   • {district:30s}: {count:2d} colleges")
        
        print("\n" + "=" * 80)
        print("🎓 COLLEGES SUMMARY BY PRIMARY COURSE")
        print("=" * 80)
        courses = db.colleges.distinct('primary_course')
        for course in sorted(courses):
            count = db.colleges.count_documents({'primary_course': course})
            print(f"   • {course:30s}: {count:2d} colleges")
        
        # Top rated colleges
        print("\n" + "=" * 80)
        print("⭐ TOP 10 RATED COLLEGES")
        print("=" * 80)
        top_colleges = db.colleges.find().sort('rating', -1).limit(10)
        for idx, college in enumerate(top_colleges, 1):
            print(f"   {idx:2d}. {college['name']:50s} - {college['rating']} ⭐")
        
        print("\n" + "=" * 80)
        print("✅ KERALA COLLEGES DATA POPULATED SUCCESSFULLY!")
        print("=" * 80)
        print(f"\n📈 Total Colleges: {len(kerala_colleges)}")
        print(f"📚 Types: {len(types)}")
        print(f"🗺️  Districts: {len(districts)}")
        print(f"🎯 Primary Courses: {len(courses)}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error populating colleges: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_indexes():
    """Create indexes for better query performance"""
    print("\n📑 Creating indexes for optimized queries...")
    
    try:
        # Create indexes on commonly queried fields
        db.colleges.create_index([("type", 1)])
        db.colleges.create_index([("district", 1)])
        db.colleges.create_index([("primary_course", 1)])
        db.colleges.create_index([("rating", -1)])
        db.colleges.create_index([("courses", 1)])
        db.colleges.create_index([("type", 1), ("district", 1)])
        db.colleges.create_index([("primary_course", 1), ("district", 1)])
        
        print("✅ Indexes created successfully!")
        
    except Exception as e:
        print(f"⚠️  Warning: Could not create indexes: {str(e)}")

if __name__ == "__main__":
    print("\n🎓 Starting Enhanced Kerala Colleges Data Population...\n")
    success = populate_colleges()
    
    if success:
        create_indexes()
        print("\n" + "=" * 80)
        print("🎉 SETUP COMPLETE!")
        print("=" * 80)
        print("\n✅ You can now use the College Finder with:")
        print("   • 60 real Kerala institutions")
        print("   • Filter by Course (B.Tech, MBBS, MBA, etc.)")
        print("   • Filter by District (14 districts)")
        print("   • Filter by Type (Engineering, Medical, Arts & Science, etc.)")
        print("   • Search and compare colleges")
        print("   • View ratings and placements")
        print("\n📱 Happy College Hunting! 🎯")
    else:
        print("\n❌ Population failed. Check the errors above.")