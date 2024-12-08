class NicheMasterDatabase:
    def __init__(self):
        self.niches = {
            'food_and_dining': {
                'name': '🍽️ Food & Dining',
                'sub_niches': [
                    'Restaurants', 'Food Trucks', 'Cafes', 'Bakeries', 'Bars',
                    'Fine Dining', 'Fast Food', 'Catering', 'Ghost Kitchens'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '2-3 months'
            },
            'health_and_wellness': {
                'name': '💪 Health & Wellness',
                'sub_niches': [
                    'Gyms', 'Yoga Studios', 'CrossFit', 'Personal Trainers',
                    'Nutrition Coaches', 'Wellness Centers', 'Med Spas'
                ],
                'profit_potential': '💰💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '3-4 months'
            },
            'home_services': {
                'name': '🏠 Home Services',
                'sub_niches': [
                    'Plumbers', 'Electricians', 'HVAC', 'Landscaping',
                    'Cleaning Services', 'Pest Control', 'Roofing'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '2-3 months'
            },
            'beauty_and_personal': {
                'name': '💅 Beauty & Personal Care',
                'sub_niches': [
                    'Hair Salons', 'Nail Salons', 'Spas', 'Barbershops',
                    'Beauty Supply', 'Cosmetics', 'Skincare'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '2-3 months'
            },
            'professional_services': {
                'name': '👔 Professional Services',
                'sub_niches': [
                    'Lawyers', 'Accountants', 'Financial Advisors',
                    'Insurance Agents', 'Real Estate Agents', 'Consultants'
                ],
                'profit_potential': '💰💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '3-4 months'
            },
            'automotive': {
                'name': '🚗 Automotive',
                'sub_niches': [
                    'Auto Repair', 'Car Dealerships', 'Car Wash',
                    'Auto Parts', 'Tire Shops', 'Body Shops'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '2-3 months'
            },
            'education': {
                'name': '📚 Education',
                'sub_niches': [
                    'Tutoring', 'Schools', 'Online Courses', 'Training Centers',
                    'Language Schools', 'Music Schools', 'Art Classes'
                ],
                'profit_potential': '💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '3-4 months'
            },
            'retail': {
                'name': '🛍️ Retail',
                'sub_niches': [
                    'Clothing', 'Electronics', 'Furniture', 'Jewelry',
                    'Sports Equipment', 'Pet Supplies', 'Gifts'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '3-4 months'
            },
            'entertainment': {
                'name': '🎮 Entertainment',
                'sub_niches': [
                    'Gaming Centers', 'Movie Theaters', 'Arcades',
                    'Bowling Alleys', 'Escape Rooms', 'Party Venues'
                ],
                'profit_potential': '💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '2-3 months'
            },
            'tech_services': {
                'name': '💻 Tech Services',
                'sub_niches': [
                    'IT Support', 'Web Development', 'App Development',
                    'Digital Marketing', 'SEO Services', 'Cloud Services'
                ],
                'profit_potential': '💰💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '3-4 months'
            },
            'construction': {
                'name': '🏗️ Construction & Trades',
                'sub_niches': [
                    'General Contractors', 'Home Builders', 'Remodeling', 'Painters',
                    'Flooring Specialists', 'Cabinet Makers', 'Window Installation',
                    'Fencing', 'Concrete Services', 'Drywall Contractors',
                    'Solar Installation', 'Pool Builders', 'Deck Builders'
                ],
                'profit_potential': '💰💰💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '2-3 months'
            },
            'pet_industry': {
                'name': '🐾 Pet Industry',
                'sub_niches': [
                    'Veterinarians', 'Pet Grooming', 'Pet Stores', 'Dog Training',
                    'Pet Boarding', 'Pet Daycare', 'Mobile Pet Services',
                    'Pet Photography', 'Pet Food Stores', 'Aquarium Services',
                    'Pet Waste Services', 'Pet Transportation', 'Pet Insurance'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '2-3 months'
            },
            'wedding_industry': {
                'name': '💒 Wedding Industry',
                'sub_niches': [
                    'Wedding Planners', 'Bridal Shops', 'Wedding Venues',
                    'Wedding Photography', 'Wedding Catering', 'Wedding DJs',
                    'Florists', 'Wedding Cake Makers', 'Wedding Decorators',
                    'Bridal Beauty Services', 'Wedding Transportation',
                    'Wedding Rentals', 'Wedding Bands'
                ],
                'profit_potential': '💰💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '3-4 months'
            },
            'fitness_sports': {
                'name': '🏃 Fitness & Sports',
                'sub_niches': [
                    'Fitness Centers', 'Sports Clubs', 'Martial Arts Studios',
                    'Dance Studios', 'Swimming Schools', 'Tennis Clubs',
                    'Rock Climbing Gyms', 'Golf Training', 'Sports Coaching',
                    'Athletic Training', 'Pilates Studios', 'Boxing Gyms',
                    'Indoor Sports Centers'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '2-3 months'
            },
            'child_services': {
                'name': '👶 Child Services',
                'sub_niches': [
                    'Daycare Centers', 'Preschools', 'After School Programs',
                    'Children\'s Sports', 'Music Lessons', 'Art Classes',
                    'Tutoring Services', 'Birthday Party Venues', 'Summer Camps',
                    'Child Photography', 'Kids Hair Salons', 'Child Care',
                    'Kids Entertainment'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '2-3 months'
            },
            'senior_services': {
                'name': '👴 Senior Services',
                'sub_niches': [
                    'Senior Care', 'Retirement Communities', 'Home Health Care',
                    'Medical Alert Services', 'Senior Transportation',
                    'Senior Living Advisors', 'Memory Care', 'Elder Law Services',
                    'Senior Fitness', 'Medical Equipment', 'Senior Social Services'
                ],
                'profit_potential': '💰💰💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '3-4 months'
            },
            'event_industry': {
                'name': '🎪 Event Industry',
                'sub_niches': [
                    'Event Planners', 'Corporate Events', 'Party Rentals',
                    'Event Venues', 'Catering Services', 'Event Photography',
                    'Audio Visual Services', 'Event Decorators', 'Food Trucks',
                    'Entertainment Booking', 'Event Security', 'Event Marketing'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '2-3 months'
            },
            'travel_tourism': {
                'name': '✈️ Travel & Tourism',
                'sub_niches': [
                    'Travel Agencies', 'Tour Operators', 'Hotels & Lodging',
                    'Adventure Tourism', 'Tourist Attractions', 'Transportation Services',
                    'Vacation Rentals', 'Travel Photography', 'Local Guides',
                    'Tourism Marketing', 'Travel Insurance', 'Destination Management'
                ],
                'profit_potential': '💰💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '3-4 months'
            },
            'financial_services': {
                'name': '💼 Financial Services',
                'sub_niches': [
                    'Financial Advisors', 'Tax Services', 'Bookkeeping',
                    'Investment Firms', 'Insurance Brokers', 'Mortgage Brokers',
                    'Credit Repair', 'Debt Collection', 'Payment Processing',
                    'Business Loans', 'Estate Planning', 'Financial Education'
                ],
                'profit_potential': '💰💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '3-4 months'
            },
            'manufacturing': {
                'name': '🏭 Manufacturing',
                'sub_niches': [
                    'Custom Manufacturing', 'Product Assembly', 'Metal Fabrication',
                    'Woodworking', 'Plastic Manufacturing', 'Food Manufacturing',
                    'Textile Manufacturing', 'Electronics Manufacturing',
                    'Chemical Manufacturing', 'Machinery Manufacturing'
                ],
                'profit_potential': '💰💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '4-5 months'
            },
            'agriculture': {
                'name': '🌾 Agriculture',
                'sub_niches': [
                    'Farming Operations', 'Hydroponics', 'Organic Farming',
                    'Livestock Management', 'Agricultural Consulting',
                    'Farm Equipment', 'Seed Suppliers', 'Irrigation Systems',
                    'Pest Control', 'Agricultural Technology'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'Medium',
                'takeover_time': '3-4 months'
            },
            'logistics': {
                'name': '🚛 Logistics & Transportation',
                'sub_niches': [
                    'Trucking Companies', 'Courier Services', 'Warehousing',
                    'Moving Companies', 'Freight Forwarding', 'Last Mile Delivery',
                    'Cold Chain Logistics', 'Supply Chain Management',
                    'Fleet Management', 'Logistics Technology'
                ],
                'profit_potential': '💰💰💰💰',
                'competition_level': 'High',
                'takeover_time': '3-4 months'
            }
        }
        
    def get_niche_info(self, niche_id):
        """Get detailed info about a niche"""
        return self.niches.get(niche_id, {})
    
    def get_all_niches(self):
        """Get all niches for display"""
        return {
            niche_id: {
                'name': info['name'],
                'profit_potential': info['profit_potential'],
                'sub_niches_count': len(info['sub_niches'])
            }
            for niche_id, info in self.niches.items()
        }
    
    def get_domination_strategy(self, niche_id):
        """Get perfect domination strategy for a niche"""
        niche = self.niches.get(niche_id)
        if not niche:
            return None
            
        return {
            'niche': niche['name'],
            'strategy': {
                'phase1': 'Market Research & Competition Analysis',
                'phase2': 'Aggressive Marketing Campaign',
                'phase3': 'Local Business Takeover',
                'phase4': 'Market Domination & Scaling'
            },
            'timeline': niche['takeover_time'],
            'profit_potential': niche['profit_potential'],
            'competition_level': niche['competition_level']
        }
        
    def get_revenue_estimate(self, niche_id):
        """Calculate potential revenue for a niche"""
        niche = self.niches.get(niche_id)
        if not niche:
            return 0
            
        # Base revenue potential based on 💰 count
        base_revenue = len(niche['profit_potential']) * 250000
        
        # Multiply by number of sub-niches
        total_potential = base_revenue * len(niche['sub_niches'])
        
        return total_potential
